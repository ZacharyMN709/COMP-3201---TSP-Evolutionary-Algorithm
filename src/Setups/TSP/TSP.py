import csv
from random import sample, shuffle
import pandas as pd
import time

# Graphing helpers
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure as Figure
import seaborn as sns

FILENUM = None
LOCATIONS = dict()
DATAFRAME = None
DATAFRAME_COLUMNS = ['Longitude (Range shifted)', 'Latitude (Range shifted)']
MEMOIZED = dict()


# region Display Helpers
def point_display():
    # TODO - Improve Graphs
    DATAFRAME.plot.scatter(x=DATAFRAME_COLUMNS[0], y=DATAFRAME_COLUMNS[1], c=DATAFRAME.index.get_values(), colormap='winter')
    plt.title('City Locations (Normalized to origin of 0)')


def path_display(path):
    # TODO - Improve Graphs
    DATAFRAME.plot.scatter(x=DATAFRAME_COLUMNS[0], y=DATAFRAME_COLUMNS[1], c=DATAFRAME.index.get_values(), colormap='winter')
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
        print('Warning! Invalid seletion. Defaulting to 1')
        fname = "TSP_WesternSahara_29.txt"

    fname = 'C:\\Users\\Zachary\\Documents\\GitHub\\COMP 3201 - TSP Evolutionary Algorithm\\src\\Setups\\TSP\\TSP_Inputs\\' + fname
    with open(fname, 'r') as f:
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

    global DATAFRAME, MEMOIZED
    DATAFRAME = pd.DataFrame.from_dict(LOCATIONS, orient='index')
    DATAFRAME.columns = DATAFRAME_COLUMNS
    MEMOIZED = {key: dict() for key in range(len(LOCATIONS))}

    return len(LOCATIONS)


def random_initialization(pop_size, genome_length):
    return [sample([c for c in range(genome_length)], genome_length) for _ in range(pop_size)]


def heurisitic_initialization(pop_size, genome_length):
    print('TSP.heurisitic_initialization() is a stub Method! Returning random_initialization()')
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


def euclidean_distance(individual):
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


def random_search(BEST_SO_FAR):
    print('Starting best:', BEST_SO_FAR)
    nodes = [i for i in range(len(LOCATIONS))]
    counter = 0
    print_break = 100
    while True:
        counter += 1
        if counter % print_break == 0: print('.', end='')
        if counter % (print_break * 100) == 0: print()
        shuffle(nodes)
        fit = euclidean_distance(nodes)
        if fit < BEST_SO_FAR:
            BEST_SO_FAR = fit
            print('\nNew best:', fit)


def brute_force_solver(fnum=None):
    def depth_first_eval(start_list, to_add, BEST_SO_FAR, top_layer=False):
        if not to_add:
            fitness = euclidean_distance(start_list)
            if fitness <= BEST_SO_FAR:
                if fitness == BEST_SO_FAR: print('Equal fitness found.')
                else: print('New best fitness found: {}'.format(fitness))
                print(start_list)
            return fitness

        ele = to_add.pop(0)
        for i in range(1, len(start_list)+1):
            temp = start_list.copy()
            temp.insert(i, ele)
            if euclidean_distance(temp) <= BEST_SO_FAR:
                best = depth_first_eval(temp, to_add, BEST_SO_FAR)
                if best < BEST_SO_FAR:
                    BEST_SO_FAR = best
            # else: print('Skipping subtree:', temp)  # Warning! Produces copious output
            if top_layer: print('{}/3rd way through at: {} seconds'.format(i, (time.time() - start_time)))
        to_add.insert(0, ele)
        return BEST_SO_FAR

    if fnum: read_tsp_file(fnum)
    if FILENUM == 1:
        print('WARNING! The number of digits in 28! is 30')
        BEST_SO_FAR = 27620.778129222075
    elif FILENUM == 2:
        print('WARNING! The number of digits in 733! is 1784')
        BEST_SO_FAR = 843853.0137981402
    elif FILENUM == 3:
        print('WARNING! The number of digits in 4662! is 15081')
        from sys import setrecursionlimit
        print('Increasing recursion limit...')
        setrecursionlimit(4700)
        BEST_SO_FAR = 47838772.09969168
    else:
        BEST_SO_FAR = 47838772.09969168

    start_time = time.time()
    nodes = [i for i in range(len(LOCATIONS))]
    optimum = depth_first_eval(nodes[:3], nodes[3:], BEST_SO_FAR)
    print("Brute force search took a total of: %s seconds" % (time.time() - start_time))
    print('Optimal fitness: ', optimum)
# endregion


if __name__ == '__main__':
    # read_tsp_file(1)
    brute_force_solver(1)

