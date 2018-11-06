import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from src.Setups.TSP.TSP_Inputs.Optimums import get_best_path

# region Globals and Setters
FILENUM = None
CITIES = None
DATAFRAME_COLUMNS = ['Longitude (Range shifted)', 'Latitude (Range shifted)']
MEMOIZED = dict()
genome_length = 0
eval_fitness = None
op = None


def set_fitness_function(i):
    global eval_fitness
    eval_fitness = i


def set_op(i):
    global op
    op = i
# endregion


# region Display Methods
def start_up_display():
    # TODO - Improve Graphs
    CITIES.plot.scatter(x=DATAFRAME_COLUMNS[0], y=DATAFRAME_COLUMNS[1], c=CITIES.index.get_values(), colormap='winter')
    plt.title('City Locations (Normalized to origin of 0)')


def generation_display(population, generation):
    # TODO - Improve Graphs

    op_fit = population['fitnesses'].max()
    num_sols = population[population['fitnesses'] == op_fit]
    CITIES.plot.scatter(x=DATAFRAME_COLUMNS[0], y=DATAFRAME_COLUMNS[1], c=CITIES.index.get_values(), colormap='winter')
    plt.title('City Locations (Normalized to origin of 0)')

    print("Generation: {}\n - Best fitness: {}\n - Avg. fitness: {}\n - Number of optimal solutions: {}/{}\n".format(
        generation, op_fit, population.mean(), len(num_sols), len(population))
    )


def final_display(population):
    op_fit = population['fitnesses'].max()
    num_sols = population[population['fitnesses'] == op_fit]
    print("\nBest solution fitness:", op_fit, "\nNumber of optimal solutions: ", len(num_sols), '/', len(population))
    print("Best solution indexes:\n", num_sols)
    print('\n\n\n\n\n\n')
# endregion


# region Initialization
def read_tsp_file(fnum):
    global FILENUM
    FILENUM = fnum
    if fnum == 1:
        fname = "TSP_WesternSahara_29.txt"
    elif fnum == 2:
        #print('Warning! Takes approximately 1.5 seconds per decade')
        fname = "TSP_Uruguay_734.txt"
    elif fnum == 3:
        #print('Warning! Takes approximately 45 seconds per decade')
        fname = "TSP_Canada_4663.txt"
    else:
        print('Warning! Invalid seletion. Defaulting to 1')
        fname = "TSP_WesternSahara_29.txt"

    fname = 'Setups/TSP/TSP_Inputs/' + fname

    global CITIES
    # Uses indexing from 0, rather than 1, by skipping the first column in the data.
    CITIES = pd.read_csv(fname, usecols=[1, 2], header=None, delimiter=' ')
    CITIES.columns = ['Lat', 'Lon']
    CITIES.index.names = ['City']

    # Translate and invert the x values, and translate the y values
    CITIES['Lat'] = CITIES['Lat'] - (CITIES['Lat'].min() + (CITIES['Lat'].max() - CITIES['Lat'].min()) / 2)
    CITIES['Lon'] = (CITIES['Lon'].min() + (CITIES['Lon'].max() - CITIES['Lon'].min()) / 2) - CITIES['Lon']
    CITIES.columns = DATAFRAME_COLUMNS

    # TODO - Get the height of df columns
    global genome_length
    genome_length = len(CITIES)
    global MEMOIZED
    MEMOIZED = {key: dict() for key in range(genome_length)}

    return genome_length


def fitness_applicator(func):
    def generate_population(pop_size, genome_length):
        population = func(pop_size, genome_length)
        population['fitnesses'] = population['individuals'].apply(eval_fitness)
        return population
    return generate_population


@fitness_applicator
def random_initialization(pop_size, genome_length):
    df = pd.DataFrame([(np.random.permutation(genome_length), ) for _ in range(pop_size)], columns=['individuals'])
    df.index.names = ['indexes']
    return df


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
    return sum([calc_distance(individual[i-1], individual[i]) for i in range(genome_length)])


@euclid_memoize
def calc_distance(loc1, loc2):
    x1, y1 = CITIES.loc[loc1]
    x2, y2 = CITIES.loc[loc2]
    return ((x1-x2)**2 + (y1 - y2)**2)**0.5
# endregion


# region Brute Force Solver
def brute_force_solver(fnum=None):
    def depth_first_eval(start_list, to_add, opt_dist, opt_path):
        if not to_add:
            fitness = euclidean_distance(start_list)
            if fitness <= opt_dist:
                if fitness == opt_dist: print('Equal fitness found.')
                else: print('New best fitness found: {}'.format(fitness))
                opt_path = start_list.copy()
                print(opt_path)
            return fitness, opt_path

        ele = to_add.pop(0)
        for i in range(1, len(start_list)+1):
            temp = start_list.copy()
            temp.insert(i, ele)
            if euclidean_distance(temp) <= opt_dist:
                best, opt_path = depth_first_eval(temp, to_add, opt_dist, opt_path)
                if best < opt_dist:
                    opt_dist = best
        to_add.insert(0, ele)
        return opt_dist, opt_path

    if fnum: read_tsp_file(fnum)
    opt_dist, opt_path, _ = get_best_path(FILENUM, brute_search=True)

    start_time = time.time()
    # TODO - Get the height of df columns
    nodes = [i for i in range(len(LOCATIONS))]
    opt_dist, opt_path = depth_first_eval(nodes[:3], nodes[3:], opt_dist, opt_path)
    print("Heuristic aided brute force search took a total of: %s seconds" % (time.time() - start_time))
    print('Optimal fitness: ', opt_dist)
    print(opt_path)
# endregion


if __name__ == '__main__':
    # read_tsp_file(1)
    brute_force_solver(2)

