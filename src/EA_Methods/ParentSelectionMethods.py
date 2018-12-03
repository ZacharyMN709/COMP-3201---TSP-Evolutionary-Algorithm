from src.EA_Methods.HelperTemplate import BaseHelper
from random import sample, random, shuffle


class ParentSelectionHelper(BaseHelper):
    def __init__(self, var_helper, data_type):
        name_method_pairs = [('MPS', self.select_parents_using(self.mps)),
                             ('Tourney', self.select_parents_using(self.tournament)),
                             ('Random', self.select_parents_using(self.random_uniform))
                             ]
        super().__init__(var_helper, data_type, name_method_pairs)

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
        selected_to_mate = []  # a list of indices of picked parents in population
        total_fitness = sum(fitness)
        increment = 1 / self.vars.mating_pool_size  # The pointer 'angle'
        seed = random() / len(fitness)  # The pointer start position
        a = 0  # The rolling probability sum

        # makes a list with normalized cumulatively summed fitnesses, and indexes
        fit_indexes = [[x, fitness[x] / total_fitness] for x in range(len(fitness))]
        for x in fit_indexes:
            a += x[1]
            x[1] = a

        # Iterates over the pointers/individuals to add parents to the list.
        for x in fit_indexes:
            while seed < x[1]:
                seed += increment
                selected_to_mate.append(x[0])

        return selected_to_mate

    def tournament(self, fitness):
        # Generate tuples of index-fitness pairs.
        fit_indexes = [(x, fitness[x]) for x in range(len(fitness))]

        # Return a list of parents indices based of the winners of the tournaments.
        return [self.vars.best_of(sample(fit_indexes, self.vars.tournament_size), key=lambda x: x[1])[0] for _ in
                range(self.vars.mating_pool_size)]

    def random_uniform(self, fitness):
        # Return a number of parent indices selected at random.
        return sample([x for x in range(len(fitness))], self.vars.mating_pool_size)
    # endregion
