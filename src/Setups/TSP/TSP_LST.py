import os
import csv
from random import sample, shuffle
from copy import deepcopy
import numpy as np
from array import array
from Pickle_Helper import get_pickled_euler, get_pickled_memo, pickle_memo_obj

# region Globals and Setters
MAX = False
FILENUM = None
REP = None
LOCATIONS = dict()
MEMOIZED = dict()
CLUSTERS = []
MSTREE = []
ODDVERTEXES = []
eval_fitness = None
dist_mod = 0.10


def set_fitness_function(i):
    global eval_fitness
    eval_fitness = i
# endregion


# region Initialization
def read_tsp_file(fnum):
    global FILENUM
    FILENUM = fnum

    city_dict = get_pickled_memo(fnum)
    global MEMOIZED, LOCATIONS
    if city_dict:
        MEMOIZED, LOCATIONS = city_dict['Locs'], city_dict['Dists']
    else:
        if fnum == 1:
            fname = "TSP_WesternSahara_29.txt"
        elif fnum == 2:
            fname = "TSP_Uruguay_734.txt"
        elif fnum == 3:
            fname = "TSP_Canada_4663.txt"
        else:
            print('Warning! Invalid seletion. Defaulting to test')
            fname = "TSP_Testbed_10.txt"

        script_dir = os.path.dirname(__file__)  # absolute path for directory/folder this script is in
        abs_file_path = os.path.join(script_dir, 'Inputs', fname)

        with open(abs_file_path, 'r') as f:
            # Read and parse the file
            file = csv.reader(f, delimiter=' ')
            locations = [(float(i[1]), float(i[2])) for i in file]

            # Shift the numbers, so they are smaller and centered
            max_x, max_y = max(locations, key=lambda i: i[0])[0], max(locations, key=lambda i: i[1])[1]
            min_x, min_y = min(locations, key=lambda i: i[0])[0], min(locations, key=lambda i: i[1])[1]
            shift_x, shift_y = min_x + ((max_x - min_x)/2), min_y + ((max_y - min_y)/2)

            # NOTE: Locations are slightly odd. Original (x, y) mapped to normalized (-y, x) to produce
            # identifiable map of Canada.
            LOCATIONS = [(shift_y - i[1], i[0] - shift_x) for i in locations]

        MEMOIZED = [[((L1[0]-L2[0])**2 + (L1[1] - L2[1])**2)**0.5 for L2 in LOCATIONS] for L1 in LOCATIONS]

        to_save = {'Locs': LOCATIONS, 'Dists': MEMOIZED}
        pickle_memo_obj(to_save, fnum)

    return len(LOCATIONS)
# endregion


# region Population Seeding
# region Decorators
def fitness_applicator(func):
    def generate_population(pop_size, genome_length):
        population = func(pop_size, genome_length)
        global eval_fitness
        return population, [eval_fitness(i) for i in population]
    return generate_population


def representation_wrapper(func):
    def wrap_output(genome_length):
        if REP == 2:
            return array('i', func(genome_length))
        elif REP == 1:
            return np.array(func(genome_length))
        else:
            return list(func(genome_length))
    return wrap_output
# endregion

# region Random


def single_random_individual(genome_length):
    return sample([c for c in range(genome_length)], genome_length)


@fitness_applicator
def random_initialization(pop_size, genome_length):
    return [single_random_individual(genome_length) for _ in range(pop_size)]


# endregion
# region Cluster Heuristic


def get_map_range():
    max_lat = max(LOCATIONS, key=lambda x: x[0])[0]
    max_lon = max(LOCATIONS, key=lambda x: x[1])[1]
    min_lat = min(LOCATIONS, key=lambda x: x[0])[0]
    min_lon = min(LOCATIONS, key=lambda x: x[1])[1]
    return (max_lat - min_lat), (max_lon - min_lon)


def cities_in_radius(city, radius, cities):
    x, y = [(c[1]-city[1])**2 for c in cities], [(c[0]-city[0])**2 for c in cities]
    indexes = {i for i in range(len(cities)) if (x[i] + y[i])**0.5 <= radius}
    return indexes


def create_clusters(cities, city_indexes, mod_mod):
    height, width = get_map_range()
    if height > width: dist = height * dist_mod * mod_mod
    else: dist = width * dist_mod * mod_mod
    city_clusters = []

    cities_left = set(city_indexes)
    while len(cities_left) != 0:
        city = sample(cities_left, 1)[0]
        cluster = (cities_left & cities_in_radius(LOCATIONS[city], dist, cities)) | {city}
        cities_left = cities_left - cluster
        city_clusters.append(list(cluster))

    return city_clusters


def single_cluster_individual(genome_length):
    shuffle(CLUSTERS)
    indiv = []
    for x in CLUSTERS:
        shuffle(x)
        for y in x:
            shuffle(y)
            indiv += y
    return indiv


@fitness_applicator
def heuristic_cluster_initialization(pop_size, genome_length):
    global CLUSTERS
    CLUSTERS = create_clusters(LOCATIONS, [x for x in range(len(LOCATIONS))], 1)
    for i in range(len(CLUSTERS)):
        CLUSTERS[i] = create_clusters([LOCATIONS[x] for x in CLUSTERS[i]], CLUSTERS[i], 0.5)
    return [single_cluster_individual(genome_length) for _ in range(pop_size)]


# endregion
# region Grid Heuristic


@fitness_applicator
def heuristic_grid_initialization(pop_size, genome_length):
    global CLUSTERS
    CLUSTERS = create_clusters(LOCATIONS, [x for x in range(len(LOCATIONS))], 1)
    return [single_cluster_individual(genome_length) for _ in range(pop_size)]


# endregion
# region Euler Heuristic


def single_euler_individual(genome_length):
    return remove_duplicates(EULERTOUR)


@fitness_applicator
def heuristic_euler_initialization(pop_size, genome_length):
    global MSTREE, ODDVERTEXES, EULERTOUR, DUPE_DICT
    euler_dict = get_pickled_euler(FILENUM, fast=True)
    if euler_dict:
        EULERTOUR = euler_dict['Euler']
    else:
        MSTREE = minimum_spanning_tree()
        ODDVERTEXES = find_odd_vertexes(MSTREE)
        new_tree = deepcopy(MSTREE)
        minimum_weight_matching(new_tree, deepcopy(ODDVERTEXES))
        EULERTOUR = euler_tour(new_tree)
    DUPE_DICT = {i: [] for i in range(len(MEMOIZED))}
    for i in range(len(EULERTOUR)): DUPE_DICT[EULERTOUR[i]].append(i)
    return [single_euler_individual(genome_length) for _ in range(pop_size)]
# endregion
# endregion


# region Fitness
def euclidean_distance(individual):  # Minimization
    return sum([calc_distance(individual[i-1], individual[i]) for i in range(len(individual))])


def calc_distance(loc1, loc2):
    return MEMOIZED[loc1][loc2]
# endregion


if __name__ == '__main__':
    genome_length = read_tsp_file(3)
    import time

    start_time = time.time()

    set_fitness_function(euclidean_distance)
    pop, fitmesses = heuristic_cluster_initialization(60, genome_length)
    print(CLUSTERS)
    #for x in CLUSTERS: print(x)
    print()
    for x in pop: print(x)
    print(time.time() - start_time)
