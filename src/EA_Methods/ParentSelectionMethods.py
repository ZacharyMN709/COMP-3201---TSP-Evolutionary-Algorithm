from src.EA_Methods.HelperTemplate import BaseHelper
from random import sample, random, shuffle


class ParentSelectionHelper(BaseHelper):
    """
    This class should be safe for all representations, as it mainly relies on integer or float
    representations of fitness, and manages the population on the whole, rather than modifying
    any individuals directly.
    """
    def __init__(self, var_helper):
        name_method_pairs = [('MPS', self.select_parents_using(self.mps)),
                             ('Tourney', self.select_parents_using(self.tournament)),
                             ('Random', self.select_parents_using(self.random_uniform))
                             ]
        super().__init__(var_helper, name_method_pairs)

    def __str__(self):
        return super().__str__().format('ParentSelectionHelper')

    # region Parent Selection Methods
    # Takes in a method, and then 'injects' the code to shuffle the output.
    def select_parents_using(self, func):
        def shuffle_output(fitness):
            # Find the parents,
            selected_to_mate = func(fitness)
            # And then shuffle their indices.
            shuffle(selected_to_mate)
            return selected_to_mate

        shuffle_output.__name__ = func.__name__
        return shuffle_output

    def mps(self, fitness):
        selected_to_mate = [None] * self.vars.mating_pool_size  # a list of indices of picked parents in population
        total_fitness = sum(fitness)
        increment = 1 / self.vars.mating_pool_size  # The pointer 'angle'
        seed = random() / self.vars.population_size  # The pointer start position
        a = 0  # The rolling probability sum

        # makes a list with normalized cumulatively summed fitnesses, and indexes
        fit_indexes = [[x, fitness[x] / total_fitness] for x in range(self.vars.population_size)]
        for x in fit_indexes:
            a += x[1]
            x[1] = a

        # Iterates over the pointers/individuals to add parents to the list.
        to_fill = 0
        for x in fit_indexes:
            while seed < x[1]:
                seed += increment
                selected_to_mate[to_fill] = x[0]
                to_fill += 1

        return selected_to_mate

    def tournament(self, fitness):
        # Generate tuples of index-fitness pairs.
        fit_indexes = [(x, fitness[x]) for x in range(self.vars.population_size)]

        # Return a list of parents indices based of the winners of the tournaments.
        return [self.vars.best_of(sample(fit_indexes, self.vars.tournament_size), key=lambda x: x[1])[0] for _ in
                range(self.vars.mating_pool_size)]

    def random_uniform(self, fitness):
        # Return a number of parent indices selected at random.
        return sample([x for x in range(self.vars.population_size)], self.vars.mating_pool_size)
    # endregion


if __name__ == '__main__':
    from src.EA_Methods.EAVarHelper import EAVarHelper
    from time import time

    eavars = EAVarHelper(20, False)
    eavars.population_size = 20
    eavars.tournament_size = 4
    eavars.mating_pool_size = 10
    ps = ParentSelectionHelper(eavars, 0)

    methods = [ps.random_uniform,
               ps.tournament,
               ps.mps
               ]

    for x in methods:
        start = time()
        for y in range(10000):
            indiv = [x for x in range(20)]
            x(indiv)
        print(time() - start)
