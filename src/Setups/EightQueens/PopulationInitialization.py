from src.EACore.MethodClasses.HelperTemplate import BaseHelper
from numpy import array as np_array
from array import array as c_array
from random import sample


def list_wrapper(indiv):
    return indiv


def np_wrapper(indiv):
    return np_array(indiv)


def c_wrapper(indiv):
    return c_array('i', indiv)


class PopulationInitializationHelper(BaseHelper):
    def __init__(self, var_helper, data_type):
        name_method_pairs = [('Random', self.generate_population_using(self.single_random_individual))
                             ]
        super().__init__(var_helper, name_method_pairs)
        self.wrappers = [list_wrapper, np_wrapper, c_wrapper]
        self.wrapper = self.wrappers[data_type]

    def __str__(self):
        return super().__str__().format('PopulationInitializationHelper')

    # region Population Seeding
    def generate_population_using(self, func):
        def fitness_applicator():
            population = [self.wrapper(func()) for _ in range(self.vars.population_size)]
            return population, [self.vars.eval_fitness(i) for i in population]

        fitness_applicator.__name__ = func.__name__
        return fitness_applicator

    def single_random_individual(self):
        return sample([c for c in range(self.vars.genome_length)], self.vars.genome_length)

