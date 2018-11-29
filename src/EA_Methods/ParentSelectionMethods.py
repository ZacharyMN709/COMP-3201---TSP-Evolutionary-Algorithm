from src.EA_Methods.HelperTemplate import BaseHelper
from random import sample, random, shuffle


class ParentSelectionHelper(BaseHelper):
    def __init__(self, var_helper, method):
        name_method_pairs = [('MPS', self.mps),
                             ('Tourney', self.tournament),
                             ('Random', self.random_uniform)
                             ]
        super().__init__(var_helper, method, name_method_pairs)

    def __str__(self):
        return super().__str__().format('ParentSelectionHelper')

    def get_func_from_index(self, i):
        return self.name_method_pairs[i][1]

    # region Parent Selection Methods
    # Takes in a method, and then 'injects' the code to shuffle the output.
    @staticmethod
    def randomize_output(func):
        def generate_output(fitness, mating_pool_size):
            # Find the parents,
            selected_to_mate = func(fitness, mating_pool_size)
            # And then shuffle their indices.
            shuffle(selected_to_mate)
            return selected_to_mate

        return generate_output

    @randomize_output
    def mps(self, fitness, mating_pool_size):
        selected_to_mate = []  # a list of indices of picked parents in population
        total_fitness = sum(fitness)
        increment = 1 / mating_pool_size  # The pointer 'angle'
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

    @randomize_output
    def tournament(self, fitness, mating_pool_size):
        # Generate tuples of index-fitness pairs.
        fit_indexes = [(x, fitness[x]) for x in range(len(fitness))]

        # Return a list of parents indices based of the winners of the tournaments.
        return [self.vars.op(sample(fit_indexes, self.vars.tournament_size), key=lambda x: x[1])[0] for _ in
                range(mating_pool_size)]

    @randomize_output
    def random_uniform(self, fitness, mating_pool_size):
        # Return a number of parent indices selected at random.
        return sample([x for x in range(len(fitness))], mating_pool_size)
    # endregion
