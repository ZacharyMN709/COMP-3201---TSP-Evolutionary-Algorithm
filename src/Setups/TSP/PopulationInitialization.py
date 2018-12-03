from src.EA_Methods.HelperTemplate import BaseHelper
from numpy import array as np_array
from array import array as c_array
from random import sample, shuffle
from src.Setups.TSP.Cluster_Heuristics import ClusterBuilder
from src.Setups.TSP.Christofide_Heuristic import EulerTourBuilder


def list_wapper(indiv):
    return indiv


def np_warpper(indiv):
    return np_array(indiv)


def c_wrapper(indiv):
    return c_array('i', indiv)


class PopulationInitializationGenerator:
    def __init__(self, data, filenum):
        self.locs = data.locs
        self.dists = data.dists
        self.cluster_builder = ClusterBuilder(self.locs, self.dists)
        self.euler_builder = EulerTourBuilder(self.dists, filenum)

    def make_pop_helper(self, var_helper, data_type):
        return PopulationInitializationHelper(var_helper, data_type, self.cluster_builder, self.euler_builder)


class PopulationInitializationHelper(BaseHelper):
    def __init__(self, var_helper, data_type, cluster_builder, euler_builder):
        name_method_pairs = [('Random', self.random_initialization),
                             ('Cluster', self.heuristic_cluster_initialization),
                             ('Euler', self.heuristic_euler_initialization)
                             ]
        super().__init__(var_helper, data_type, name_method_pairs)
        self.wrappers = [list_wapper, np_warpper, c_wrapper]
        self.wrapper = self.wrappers[data_type]
        self.cluster_builder = cluster_builder
        self.euler_builder = euler_builder
        self.cluster = self.cluster_builder.generate_nested_clusters(var_helper.dist_mod)

    def __str__(self):
        return super().__str__().format('PopulationInitializationHelper')

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

    def refresh_clusters(self):
        self.cluster = self.cluster_builder.generate_nested_clusters(self.vars.dist_mod)

    @representation_wrapper
    def single_random_individual(self, genome_length):
        return sample([c for c in range(genome_length)], genome_length)

    @fitness_applicator
    def random_initialization(self, pop_size, genome_length):
        return [self.single_random_individual(genome_length) for _ in range(pop_size)]

    @representation_wrapper
    def single_cluster_individual(self, genome_length):
        shuffle(self.cluster)
        indiv = []
        for x in self.cluster:
            shuffle(x)
            for y in x:
                shuffle(y)
                indiv += y
        return indiv

    @fitness_applicator
    def heuristic_cluster_initialization(self, pop_size, genome_length):
        return [self.single_cluster_individual(genome_length) for _ in range(pop_size)]

    @fitness_applicator
    def heuristic_grid_initialization(self, pop_size, genome_length):
        return [self.single_cluster_individual(genome_length) for _ in range(pop_size)]

    @representation_wrapper
    def single_euler_individual(self, genome_length):
        return self.euler_builder.make_new_circuit()

    @fitness_applicator
    def heuristic_euler_initialization(self, pop_size, genome_length):
        self.euler_builder.gen_tree_and_tour()
        return [self.single_euler_individual(genome_length) for _ in range(pop_size)]
