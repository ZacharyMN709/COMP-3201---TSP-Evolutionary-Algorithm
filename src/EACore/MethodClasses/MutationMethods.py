from src.EACore.MethodClasses.HelperTemplate import BaseHelper
from random import randint, random


class MutatorHelper(BaseHelper):
    """
    The mutation methods which are presently implemented are all simple enough that using clever
    indexing makes the functions fast due to not requiring much memory reallocation, and more
    importantly, makes the functions work for all supported data types.
    """
    def __init__(self, var_helper):
        """
        :param var_helper:  A reference to an EAVarHelper instance.
        """
        name_method_pairs = [('Swap', self.apply_mutation_using(self.permutation_swap)),
                             ('Insert', self.apply_mutation_using(self.permutation_insert)),
                             ('Inversion', self.apply_mutation_using(self.permutation_inversion)),
                             ('Shift', self.apply_mutation_using(self.permutation_shift)),
                             ('Scramble', self.apply_mutation_using(self.permutation_scramble))
                             ]
        super().__init__(var_helper, name_method_pairs)

    def __str__(self):
        return super().__str__().format('MutatorHelper')

    # region Mutation Methods
    # Takes in a method, and then 'injects' the random chance of running into the function
    def apply_mutation_using(self, func):
        def fitness_applicator(offspring):
            def randomize_method(individual):
                # Apply the mutation X% of the time,
                if random() < self.vars.mutation_rate:
                    return func(individual)
                # and return the original if the mutation is not applied.
                else:
                    return individual

            # Apply the mutation to each individual, and get the new fitnesses.
            offspring = list(map(randomize_method, offspring))
            return offspring, list(map(self.vars.eval_fitness, offspring))

        fitness_applicator.__name__ = func.__name__
        return fitness_applicator

    def gen_two_nums(self):
        # Generate two random integers x and y
        x = randint(0, self.vars.genome_length - 1)
        y = randint(0, self.vars.genome_length - 1)
        return x, y

    def gen_two_nums_ascending(self):
        # Generate two integers such that x > y
        x = randint(0, self.vars.genome_length - 2)
        y = randint(x+1, self.vars.genome_length - 1)
        return x, y

    def gen_two_ranges(self):
        # Generate two integers such that x > y
        x = randint(0, self.vars.genome_length - 2)
        y = randint(x + 1, self.vars.genome_length - 1)

        # Generate a third integer such that a slice starting at that location with
        # size (y-x) would fit in genome_length
        w = randint(0, self.vars.genome_length - (y - x) - 1)

        return x, y, w

    def permutation_swap(self, individual):
        """
        Swap the position of two genes.
        :param individual: An individual from the population list
        :return: The mutated individual.
        """
        # Generate two random indices
        x, y = self.gen_two_nums()

        # Swap the values at those indices
        individual[x], individual[y] = individual[y], individual[x]

        return individual

    def permutation_insert(self, individual):
        """
        Move a gene into another location.
        :param individual: An individual from the population list
        :return: The mutated individual.
        """
        # Generate two random indices
        x, y = self.gen_two_nums_ascending()

        # Insert the value at y in the position after x
        for i in range(y - x):
            individual[y-i-1], individual[y-i] = individual[y-i], individual[y-i-1]

        return individual

    def permutation_inversion(self, individual):
        """
        Invert a sequence of genes.
        :param individual: An individual from the population list
        :return: The mutated individual.
        """
        # Generate two random indices in ascending order
        x, y = self.gen_two_nums_ascending()

        # Reverse the contents from x to y
        individual[x:y] = individual[x:y][::-1]

        '''
        ALT METHOD
        for i in range((y-x)//2):
            individual[x+i], individual[y-i] = individual[y-i], individual[x+i]
        '''
        return individual

    def permutation_scramble(self, individual):
        """
        Randomly rearrange a sequence of genes.
        :param individual: An individual from the population list
        :return: The mutated individual.
        """
        # Generate two random indices in ascending order
        x, y = self.gen_two_nums_ascending()

        # Randomize the order of indices from x to y
        w = y - x
        for i in range(w):
            z = randint(0, w)
            individual[x + i], individual[x + z] = individual[x + z], individual[x + i]

        return individual

    def permutation_shift(self, individual):
        """
        Shift a sequence of genes down, moving the rest of the genes up.
        :param individual: An individual from the population list
        :return: The mutated individual.
        """
        # Generate two random ranges
        x, y, w = self.gen_two_ranges()

        # Then shift one range down, while moving the other range up.
        for i in range(y - x):
            individual[x + i], individual[w + i] = individual[w + i], individual[x + i]

        return individual
    # endregion


if __name__ == '__main__':
    from src.EACore.EAVarHelper import EAVarHelper
    from time import time

    mu = MutatorHelper(EAVarHelper(20, False))

    methods = [mu.permutation_swap,
     mu.permutation_insert,
     mu.permutation_inversion,
     mu.permutation_shift,
     mu.permutation_scramble
     ]

    for x in methods:
        start = time()
        for y in range(10000):
            indiv = [x for x in range(20)]
            x(indiv)
        print(time() - start)
