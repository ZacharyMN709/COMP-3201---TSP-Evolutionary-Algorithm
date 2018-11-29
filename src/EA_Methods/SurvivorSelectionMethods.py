from random import randint


class RecombinationHelper:
    def __init__(self, var_helper, method):
        self.vars = var_helper
        self.method = method

    # region Survivor Selection Methods
    def mu_plus_lambda(self, parents, parent_fitness, offspring, offspring_fitness):
        loc_op = min if self.vars.best == max else max
        max_size = len(parents)

        population = parents + offspring
        fitness = parent_fitness + offspring_fitness

        # remove the weakest until the population is trimmed to size
        while len(population) > max_size:
            i = fitness.index(loc_op(fitness))
            population.pop(i)
            fitness.pop(i)

        return population, fitness

    def replacement(self, parents, parent_fitness, offspring, offspring_fitness):
        loc_op = min if self.vars.best == max else max
        max_size = len(parents) - len(offspring)

        # remove the weakest parents to make room for children
        while len(parents) > max_size:
            i = parent_fitness.index(loc_op(parent_fitness))
            parents.pop(i)
            parent_fitness.pop(i)

        # add the children
        population = parents + offspring
        fitness = parent_fitness + offspring_fitness

        return population, fitness

    @staticmethod
    def random_uniform(parents, parent_fitness, offspring, offspring_fitness):
        max_size = len(parents)

        # merge the populations
        population = parents + offspring
        fitness = parent_fitness + offspring_fitness

        # randomly remove members until the population is trimmed to size
        while len(population) > max_size:
            x = randint(0, len(population)-1)
            population.pop(x)
            fitness.pop(x)

        return population, fitness
    # endregion
