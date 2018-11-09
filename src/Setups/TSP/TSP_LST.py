import csv
from random import sample, shuffle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from src.Setups.TSP.TSP_Inputs.Optimums import get_best_path

# region Globals and Setters
FILENUM = None
LOCATIONS = dict()
CITIES = None
DISTANCES = None
DATAFRAME_COLUMNS = ['Longitude (Range shifted)', 'Latitude (Range shifted)']
MEMOIZED = dict()
eval_fitness = None


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


# region Display Methods
def start_up_display():
    # TODO - Improve Graphs
    CITIES.plot.scatter(x=DATAFRAME_COLUMNS[0], y=DATAFRAME_COLUMNS[1], c=CITIES.index.get_values(), colormap='winter')
    plt.title('City Locations (Normalized to origin of 0)')


def generation_display(population):
    # TODO - Improve Graphs
    CITIES.plot.scatter(x=DATAFRAME_COLUMNS[0], y=DATAFRAME_COLUMNS[1], c=CITIES.index.get_values(), colormap='winter')
    plt.title('City Locations (Normalized to origin of 0)')
# endregion


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

    import os
    script_dir = os.path.dirname(__file__)  # absolute path for directory/folder this script is in
    abs_file_path = os.path.join(script_dir, 'TSP_Inputs', fname)
    print(abs_file_path)

    with open(abs_file_path, 'r') as f:
        # Read and parse the file
        file = csv.reader(f, delimiter=' ')
        locations = [(float(i[1]), float(i[2])) for i in file]

        # Shift the numbers, so they are smaller and centered
        max_x, max_y = max(locations, key=lambda i: i[0])[0], max(locations, key=lambda i: i[1])[1]
        min_x, min_y = min(locations, key=lambda i: i[0])[0], min(locations, key=lambda i: i[1])[1]
        shift_x, shift_y = min_x + ((max_x - min_x)/2), min_y + ((max_y - min_y)/2)

        # NOTE: Locations are slightly odd. Original (x, y) mapped to normalized (-y, x) to produce
        # identifiable population map of Canada.
        locations = [(shift_y - i[1], i[0] - shift_x) for i in locations]

        # Save each location relative to an index for future use.
        global LOCATIONS
        LOCATIONS = {key: locations[key] for key in range(len(locations))}

    global CITIES
    # Uses indexing from 0, rather than 1, by skipping the first column in the data.
    CITIES = pd.read_csv(abs_file_path, usecols=[1, 2], header=None, delimiter=' ')
    CITIES.columns = ['Lat', 'Lon']
    CITIES.index.names = ['City']

    global DISTANCES
    Lats = CITIES['Lat'].transpose()
    Lons = CITIES['Lon'].transpose()
    DISTANCES = pd.DataFrame([((Lats - Lats[i])**2 + (Lons - Lons[i])**2)**0.5 for i in range(Lons.size)])

    # Translate and invert the x values, and translate the y values
    CITIES['Lat'] = CITIES['Lat'] - (CITIES['Lat'].min() + (CITIES['Lat'].max() - CITIES['Lat'].min()) / 2)
    CITIES['Lon'] = (CITIES['Lon'].min() + (CITIES['Lon'].max() - CITIES['Lon'].min()) / 2) - CITIES['Lon']
    CITIES.columns = DATAFRAME_COLUMNS

    global MEMOIZED
    MEMOIZED = {key: dict() for key in range(len(LOCATIONS))}

    return len(LOCATIONS)


@fitness_applicator
def random_initialization(pop_size, genome_length):
    return [sample([c for c in range(genome_length)], genome_length) for _ in range(pop_size)]


@fitness_applicator
def heurisitic_initialization(pop_size, genome_length):
    print('heurisitic_initialization() is a stub Method! Returning random_initialization()')
    return random_initialization(pop_size, genome_length)
# endregion


# region Fitness
def euclid_memoize(f):
    def memoize(loc1, loc2):
        if loc1 < loc2:  # Make sure loc1 is the bigger of the two. Removes memoization redundancy.
            loc1, loc2 = loc2, loc1
        if loc2 not in MEMOIZED[loc1]:
            MEMOIZED[loc1][loc2] = f(loc1, loc2)
        return MEMOIZED[loc1][loc2]
    return memoize


def euclidean_distance(individual):  # Minimization
    return sum([calc_distance(individual[i-1], individual[i]) for i in range(len(individual))])


@euclid_memoize
def calc_distance(loc1, loc2):
    x1, y1 = LOCATIONS[loc1]
    x2, y2 = LOCATIONS[loc2]
    return ((x1-x2)**2 + (y1 - y2)**2)**0.5
# endregion


# region Brute Force Solver
def generate_hamiltonian_circuits(lst_instance):
    """
    ERROR: Runs out of memory!
    A hamiltonian circuit is a loop around a graph. Of note, [1,2,3] would be
    equivalent to [3,2,1] and [3,1,2] as they travel the same path, simply in
    a different order - which is irrelevant to the problem.
    :param lst_instance: Takes a list, which is an instance of the set's hamiltonian circuit.
    :return: A list of all unique hamiltonian circuits.
    """
    def recursive_element_injector(lsts, to_add):
        if len(to_add) == 0:
            return lsts
        else:
            new_lsts = []
            ele = to_add.pop(0)
            for i in lsts:
                for j in range(len(i), 0, -1):
                    temp = i.copy()
                    temp.insert(j, ele)
                    new_lsts.append(temp)
            del lsts  # To free memory
            return recursive_element_injector(new_lsts, to_add)

    def iterative_element_injector(lsts, to_add):
        while len(to_add) != 0:
            new_lsts = []
            ele = to_add.pop(0)
            for i in lsts:
                for j in range(len(i), 0, -1):
                    temp = i.copy()
                    temp.insert(j, ele)
                    new_lsts.append(temp)
            lsts = new_lsts

    if len(lst_instance) <= 3:
        return lst_instance
    else:
        return iterative_element_injector([lst_instance[:3]], lst_instance[3:])


def random_search(opt_dist):
    print('Starting best:', opt_dist)
    nodes = [i for i in range(len(LOCATIONS))]
    counter = 0
    print_break = 100
    while True:
        counter += 1
        if counter % print_break == 0: print('.', end='')
        if counter % (print_break * 100) == 0: print()
        shuffle(nodes)
        fit = euclidean_distance(nodes)
        if fit < opt_dist:
            opt_dist = fit
            print('\nNew best:', fit)


def brute_force_solver(fnum=None):
    def depth_first_eval(start_list, to_add, opt_dist, opt_path):
        if not to_add:
            fitness = euclidean_distance(start_list)
            if fitness <= opt_dist:
                if fitness == opt_dist: print('Equal fitness found.   -  ', time.asctime(time.localtime(time.time())))
                else: print('New best fitness found: {}   -   '.format(fitness, time.asctime(time.localtime(time.time()))))
                opt_dist = fitness
                opt_path = start_list.copy()
                print(opt_path)
            return opt_dist, opt_path

        ele = to_add.pop(0)
        for i in range(1, len(start_list)+1):
            start_list.insert(i, ele)
            if euclidean_distance(start_list) <= opt_dist:
                opt_dist, opt_path = depth_first_eval(start_list, to_add, opt_dist, opt_path)
            del start_list[i]
        to_add.insert(0, ele)
        return opt_dist, opt_path

    if fnum: read_tsp_file(fnum)
    opt_dist, opt_path, _ = get_best_path(FILENUM, brute_search=True)

    start_time = time.time()
    nodes = [i for i in range(len(LOCATIONS))]
    opt_dist, opt_path = depth_first_eval(nodes[:3], nodes[3:], opt_dist, opt_path)
    print("Heuristic aided brute force search took a total of: %s seconds" % (time.time() - start_time))
    print('Optimal fitness: ', opt_dist)
    print(opt_path)
# endregion


if __name__ == '__main__':
    # read_tsp_file(1)
    brute_force_solver(1)

