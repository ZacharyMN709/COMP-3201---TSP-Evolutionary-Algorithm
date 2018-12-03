from src.EA_Methods.HelperTemplate import BaseHelper
from numpy import array as np_array
from array import array as c_array
from random import sample, shuffle
from src.Setups.TSP.Cluster_Heuristics import ClusterBuilder
from src.Setups.TSP.Christofide_Heuristic import EulerTourBuilder


def list_wrapper(indiv):
    return indiv


def np_wrapper(indiv):
    return np_array(indiv)


def c_wrapper(indiv):
    return c_array('i', indiv)


class PopulationInitializationGenerator:
    """
    A class which is meant to prevent the duplicaion of large amounts of data,
    particularly when trying to multi-thread various function combinations. It does this
    by giving each PopInitHelper a reference to static data, rather than a full copy. From
    this static data, i is then able to synthesise any mutable data when it needs to. Doing
    this also reduces the amount of computation required, as redundant calculations are avoided.
    """

    def __init__(self, data, filenum):
        self.locs = data.locs
        self.dists = data.dists
        self.cluster_builder = ClusterBuilder(self.locs, self.dists)
        self.euler_builder = EulerTourBuilder(self.dists, filenum)

    def make_pop_helper(self, var_helper, data_type):
        return PopulationInitializationHelper(var_helper, data_type, self.cluster_builder, self.euler_builder)


'''
class PopulationInitializationHelper(BaseHelper):
    def __init__(self, var_helper, data_type, cluster_builder, euler_builder):
        name_method_pairs = [('Random', self.random_initialization),
                             ('Cluster', self.heuristic_cluster_initialization),
                             ('Euler', self.heuristic_euler_initialization)
                             ]
        indiv_extras = [('Random', self.single_random_individual),
                        ('Cluster', self.single_cluster_individual),
                        ('Euler', self.single_euler_individual)
                        ]
        super().__init__(var_helper, data_type, name_method_pairs)
        self.indiv_methods = indiv_extras
        self.wrappers = [list_wrapper, np_wrapper, c_wrapper]
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

    def generate_population(self, func):
        population = [self.wrapper(func()) for _ in range(self.vars.pop_size)]
        return population, [self.vars.eval_fitness(i) for i in population]

    def refresh_clusters(self):
        self.cluster = self.cluster_builder.generate_nested_clusters(self.vars.dist_mod)

    @representation_wrapper
    def single_random_individual(self):
        return sample([c for c in range(self.vars.genome_length)], self.vars.genome_lengthgenome_length)

    @representation_wrapper
    def single_cluster_individual(self):
        shuffle(self.cluster)
        indiv = []
        for x in self.cluster:
            shuffle(x)
            for y in x:
                shuffle(y)
                indiv += y
        return indiv

    @representation_wrapper
    def single_euler_individual(self):
        return self.euler_builder.make_new_circuit()

    # TODO - Dynamically change the indiv creation function.
    @fitness_applicator
    def random_initialization(self, pop_size, genome_length):
        return [self.single_random_individual(genome_length) for _ in range(pop_size)]

    @fitness_applicator
    def heuristic_cluster_initialization(self, pop_size, genome_length):
        return [self.single_cluster_individual(genome_length) for _ in range(pop_size)]

    @fitness_applicator
    def heuristic_grid_initialization(self, pop_size, genome_length):
        return [self.single_cluster_individual(genome_length) for _ in range(pop_size)]

    @fitness_applicator
    def heuristic_euler_initialization(self, pop_size, genome_length):
        self.euler_builder.gen_mst_and_vertices()
        return [self.single_euler_individual(genome_length) for _ in range(pop_size)]
'''


class PopulationInitializationHelper(BaseHelper):
    def __init__(self, var_helper, data_type, cluster_builder, euler_builder):
        name_method_pairs = [('Random', self.generate_population_using(self.single_random_individual)),
                             ('Cluster', self.generate_population_using(self.single_cluster_individual)),
                             ('Euler', self.generate_population_using(self.single_euler_individual))
                             ]
        super().__init__(var_helper, data_type, name_method_pairs)
        self.wrappers = [list_wrapper, np_wrapper, c_wrapper]
        self.wrapper = self.wrappers[data_type]
        self.cluster_builder = cluster_builder
        self.euler_builder = euler_builder
        self.cluster = self.cluster_builder.generate_nested_clusters(var_helper.dist_mod)

    def __str__(self):
        return super().__str__().format('PopulationInitializationHelper')

    # region Population Seeding
    def generate_population_using(self, func):
        def fitness_applicator():
            population = [self.wrapper(func()) for _ in range(self.vars.pop_size)]
            return population, [self.vars.eval_fitness(i) for i in population]

        fitness_applicator.__name__ = func.__name__
        return fitness_applicator

    def refresh_clusters(self):
        self.cluster = self.cluster_builder.generate_nested_clusters(self.vars.dist_mod)

    def single_random_individual(self):
        return sample([c for c in range(self.vars.genome_length)], self.vars.genome_lengthgenome_length)

    def single_cluster_individual(self):
        shuffle(self.cluster)
        indiv = []
        for x in self.cluster:
            shuffle(x)
            for y in x:
                shuffle(y)
                indiv += y
        return indiv

    def single_euler_individual(self):
        return self.euler_builder.make_new_circuit()
