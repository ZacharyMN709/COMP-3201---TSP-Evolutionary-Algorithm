import os
import csv
from random import sample, shuffle

# region Globals and Setters
MAX = False
FILENUM = None
LOCATIONS = dict()
MEMOIZED = dict()
CLUSTERS = []
eval_fitness = None
dist_mod = 0.10


def set_fitness_function(i):
    global eval_fitness
    eval_fitness = i
# endregion


def fitness_applicator(func):
    def generate_population(pop_size, genome_length):
        population = func(pop_size, genome_length)
        global eval_fitness
        return population, [eval_fitness(i) for i in population]
    return generate_population


# region Initialization
def read_tsp_file(fnum):
    global FILENUM
    FILENUM = fnum
    if fnum == 1:
        fname = "TSP_WesternSahara_29.txt"
    elif fnum == 2:
        print('Warning! Takes approximately 1.5 seconds per decade')
        fname = "TSP_Uruguay_734.txt"
    elif fnum == 3:
        print('Warning! Takes approximately 45 seconds per decade')
        fname = "TSP_Canada_4663.txt"
    else:
        print('Warning! Invalid seletion. Defaulting to test')
        fname = "TSP_Testbed_10.txt"

    script_dir = os.path.dirname(__file__)  # absolute path for directory/folder this script is in
    abs_file_path = os.path.join(script_dir, 'TSP_Inputs', fname)

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
        global LOCATIONS
        LOCATIONS = [(shift_y - i[1], i[0] - shift_x) for i in locations]

    global MEMOIZED
    MEMOIZED = [[((L1[0]-L2[0])**2 + (L1[1] - L2[1])**2)**0.5 for L2 in LOCATIONS] for L1 in LOCATIONS]

    return len(LOCATIONS)
# endregion


# region Population Seeding
def get_map_range():
    max_lat = max(LOCATIONS, key=lambda x: x[0])[0]
    max_lon = min(LOCATIONS, key=lambda x: x[1])[1]
    min_lat = max(LOCATIONS, key=lambda x: x[0])[0]
    min_lon = min(LOCATIONS, key=lambda x: x[1])[1]
    return (max_lat - min_lat), (max_lon - min_lon)


def cities_in_radius(city, radius):
    city = LOCATIONS[city]
    x, y = [(c[1]-city[1])**2 for c in LOCATIONS], [(c[0]-city[0])**2 for c in LOCATIONS]

    indexes = {i for i in range(len(LOCATIONS)) if (x[i] + y[i])**0.5 <= radius}
    return indexes


def find_clusters():
    height, width = get_map_range()
    if height > width: dist = height
    else: dist = width
    city_clusters = []

    cities_left = {x for x in range(len(LOCATIONS))}
    while len(cities_left) != 0:
        city = sample(cities_left, 1)[0]
        cluster = cities_left & cities_in_radius(city, dist*dist_mod)
        cities_left = cities_left - cluster
        city_clusters.append(list(cluster))

    return city_clusters


def single_random_individual(genome_length):
    return sample([c for c in range(genome_length)], genome_length)


def single_heuristic_individual(genome_length):
    shuffle(CLUSTERS)
    indiv = []
    for x in CLUSTERS:
        shuffle(x)
        indiv += x
    return indiv


@fitness_applicator
def random_initialization(pop_size, genome_length):
    return [single_random_individual(genome_length) for _ in range(pop_size)]


@fitness_applicator
def heurisitic_cluster_initialization(pop_size, genome_length):
    global CLUSTERS
    CLUSTERS = find_clusters()
    return [single_heuristic_individual(genome_length) for _ in range(pop_size)]


@fitness_applicator
def heurisitic_grid_initialization(pop_size, genome_length):
    global CLUSTERS
    CLUSTERS = find_clusters()
    return [single_heuristic_individual(genome_length) for _ in range(pop_size)]
# endregion


# region Fitness
def euclidean_distance(individual):  # Minimization
    return sum([calc_distance(individual[i-1], individual[i]) for i in range(len(individual))])


def calc_distance(loc1, loc2):
    return MEMOIZED[loc1][loc2]
# endregion


if __name__ == '__main__':
    read_tsp_file(1)
    # brute_force_solver(1)

