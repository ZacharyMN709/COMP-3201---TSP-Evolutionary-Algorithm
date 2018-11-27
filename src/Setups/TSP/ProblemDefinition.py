from random import sample, shuffle
from src.Setups.TSP.FileLoader import LoadHelper
from src.Setups.TSP.Cluster_Heuristics import create_clusters, generate_nested_clusters, parse_cluster
from src.Setups.TSP.Christofide_Heuristic import generate_euler_tour, rand_dupe_removal

# region Globals and Setters
MAX = False
FILENUM = 0
METHODNUM = 0
EULERTOUR = []
FILEDATA = None
dist_mod = 0.1
FILE_DICT = {0: '8-Queens',
             1: 'Sahara',
             2: 'Uruguay',
             3: 'Canada',
             4: 'TestWorld'}


def set_method_mode(i):
    global METHODNUM
    METHODNUM = i


def set_file_num(i):
    global FILEDATA, FILENUM
    FILENUM = i
    FILEDATA = LoadHelper(i)


def set_dist_mod(i):
    global dist_mod
    dist_mod = i
# endregion


# region Population Seeding
def fitness_applicator(func):
    def generate_population(pop_size, genome_length):
        population = func(pop_size, genome_length)
        global eval_fitness
        return population, [eval_fitness(i) for i in population]
    return generate_population


def representation_wrapper(func):
    def wrap_output(genome_length):
        if METHODNUM == 2:
            from array import array
            return array('i', func(genome_length))
        elif METHODNUM == 1:
            from numpy import array
            return array(func(genome_length))
        else:
            return list(func(genome_length))

    return wrap_output


# region Random
@representation_wrapper
def single_random_individual(genome_length):
    return sample([c for c in range(genome_length)], genome_length)


@fitness_applicator
def random_initialization(pop_size, genome_length):
    return [single_random_individual(genome_length) for _ in range(pop_size)]


# endregion
# region Cluster Heuristic


@representation_wrapper
def single_cluster_individual(genome_length):
    return parse_cluster(genome_length)


@fitness_applicator
def heuristic_cluster_initialization(pop_size, genome_length):
    generate_nested_clusters(FILEDATA.locs, dist_mod)
    return [single_cluster_individual(genome_length) for _ in range(pop_size)]


# endregion
# region Grid Heuristic


@fitness_applicator
def heuristic_grid_initialization(pop_size, genome_length):
    return [single_cluster_individual(genome_length) for _ in range(pop_size)]


# endregion

def single_euler_individual(genome_length):
    return rand_dupe_removal(EULERTOUR)


@fitness_applicator
def heuristic_euler_initialization(pop_size, genome_length):
    global EULERTOUR
    EULERTOUR = generate_euler_tour(FILEDATA.locs, FILENUM, True)
    return [single_euler_individual(genome_length) for _ in range(pop_size)]
# endregion
# endregion





if __name__ == '__main__':
    pass