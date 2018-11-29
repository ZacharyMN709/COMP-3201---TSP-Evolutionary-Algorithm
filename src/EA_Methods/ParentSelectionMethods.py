from random import sample, random, shuffle


class ParentSelectionHelper:
    def __init__(self, var_helper, method):
        self.vars = var_helper
        self.method = method
        self.PARENT_METHODS = [('MPS', self.mps),
                               ('Tourney', self.tournament),
                               ('Random', self.random_uniform)
                               ]
        self.PARENT_DICT = {self.PARENT_METHODS[x][0]: x for x in range(len(self.PARENT_METHODS))}

    def get_func_from_index(self, i):
        return self.PARENT_METHODS[i][1]

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
        selected_to_mate = []           # a list of indices of picked parents in population
        total_fitness = sum(fitness)
        increment = 1/mating_pool_size  # The pointer 'angle'
        seed = random()/len(fitness)    # The pointer start position
        a = 0                           # The rolling probability sum

        # makes a list with normalized cumulatively summed fitnesses, and indexes
        fit_indexes = [[x, fitness[x]/total_fitness] for x in range(len(fitness))]
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
        return [self.vars.op(sample(fit_indexes, self.vars.tournament_size), key=lambda x: x[1])[0] for _ in range(mating_pool_size)]

    @randomize_output
    def random_uniform(self, fitness, mating_pool_size):
        # Return a number of parent indices selected at random.
        return sample([x for x in range(len(fitness))], mating_pool_size)
    # endregion
