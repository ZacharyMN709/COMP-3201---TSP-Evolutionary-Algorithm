from src.EA_Methods.HelperTemplate import BaseHelper
from random import randint


class SurvivorSelectionHelper(BaseHelper):
    """
    This class should be safe for all representations, as it mainly relies on integer or float
    representations of fitness, and manages the population on the whole, rather than modifying
    any individuals directly.
    """
    def __init__(self, var_helper):
        name_method_pairs = [('Mu + Lambda', self.mu_plus_lambda),
                                  ('Replace', self.replacement)
                                  ]
        super().__init__(var_helper, name_method_pairs)

    def __str__(self):
        return super().__str__().format('SurvivorSelectionHelper')

    # region Survivor Selection Methods
    def mu_plus_lambda(self, parents, parent_fitness, offspring, offspring_fitness):
        tuples = zip(parents + offspring, parent_fitness + offspring_fitness)
        tuples = sorted(tuples, key=lambda x: x[1], reverse=self.vars.maximize)

        population = [tuples[i][0] for i in range(self.vars.population_size)]
        fitness = [tuples[i][1] for i in range(self.vars.population_size)]
        return population, fitness

    def replacement(self, parents, parent_fitness, offspring, offspring_fitness):
        tuples = zip(parents, parent_fitness)
        tuples = sorted(tuples, key=lambda x: x[1], reverse=self.vars.maximize)

        population = [tuples[i][0] for i in range(self.vars.population_size - self.vars.mating_pool_size)] + offspring
        fitness = [tuples[i][1] for i in range(self.vars.population_size - self.vars.mating_pool_size)] + offspring_fitness
        return population, fitness

    def random_uniform(self, parents, parent_fitness, offspring, offspring_fitness):
        # merge the populations
        population = parents + offspring
        fitness = parent_fitness + offspring_fitness

        # randomly remove members until the population is trimmed to size
        while len(population) > self.vars.population_size:
            x = randint(0, len(population)-1)
            population.pop(x)
            fitness.pop(x)

        return population, fitness
    # endregion
