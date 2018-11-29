from numpy import array as np_array
from array import array as c_array
from random import sample
from src.Setups.TSP.FileLoader import LoadHelper
from src.Setups.TSP.Cluster_Heuristics import create_clusters, generate_nested_clusters, parse_cluster
from src.Setups.TSP.Christofide_Heuristic import generate_euler_tour, rand_dupe_removal


def list_wapper(indiv):
    return indiv


def np_warpper(indiv):
    return np_array(indiv)


def c_wrapper(indiv):
    return c_array('i', indiv)


class PopulationInitializationHelper:
    def __init__(self, var_helper, method):
        self.vars = var_helper
        self.method = method
        self.wrappers = [list_wapper, np_warpper, c_wrapper]
        self.wrapper = self.wrappers[method]

    # region Population Seeding
    def fitness_applicator(self, func):
        def generate_population(pop_size, genome_length):
            population = func(pop_size, genome_length)
            return population, [self.vars.eval_fitness(i) for i in population]
        return generate_population

    def representation_wrapper(self, func):
        def wrap_output(genome_length):
            return self.wrapper(func(genome_length))
        return wrap_output

    @representation_wrapper
    def single_random_individual(self, genome_length):
        return sample([c for c in range(genome_length)], genome_length)

    @fitness_applicator
    def random_initialization(self, pop_size, genome_length):
        return [self.single_random_individual(genome_length) for _ in range(pop_size)]

    @representation_wrapper
    def single_cluster_individual(self, genome_length):
        return parse_cluster(genome_length)

    @fitness_applicator
    def heuristic_cluster_initialization(self, pop_size, genome_length):
        generate_nested_clusters(FILEDATA.locs, self.vars.dist_mod)
        return [self.single_cluster_individual(genome_length) for _ in range(pop_size)]

    @fitness_applicator
    def heuristic_grid_initialization(self, pop_size, genome_length):
        return [self.single_cluster_individual(genome_length) for _ in range(pop_size)]

    @representation_wrapper
    def single_euler_individual(self, genome_length):
        return rand_dupe_removal(EULERTOUR)

    @fitness_applicator
    def heuristic_euler_initialization(self, pop_size, genome_length):
        EULERTOUR = generate_euler_tour(FILEDATA.locs, FILENUM, True)
        return [self.single_euler_individual(genome_length) for _ in range(pop_size)]
