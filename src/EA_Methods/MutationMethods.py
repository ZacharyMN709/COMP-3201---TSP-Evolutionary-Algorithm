from src.EA_Methods.HelperTemplate import BaseHelper
from random import randint, random, shuffle


class MutatorHelper(BaseHelper):
    """
    The mutation methods which are presently implemented are all simple enough that using clever
    indexing makes the functions fast d,ue to not requiring much memory reallocation, and more
    importantly, makes the functions work for all supported data types.
    """
    def __init__(self, var_helper):
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
                # If apply the mutation X% of the time,
                if random() < self.vars.mutation_rate:
                    return func(individual)
                # and the original if the mutation is not applied.
                else:
                    return individual

            offspring = list(map(randomize_method, offspring))
            return offspring, list(map(self.vars.eval_fitness, offspring))

        fitness_applicator.__name__ = func.__name__
        return fitness_applicator

    def gen_two_nums(self):
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
        # DONE
        # Generate two random indices
        x, y = self.gen_two_nums()

        # Swap the values at those indices
        individual[x], individual[y] = individual[y], individual[x]

        return individual

    def permutation_insert(self, individual):
        # DONE
        # Generate two random indices
        x, y = self.gen_two_nums_ascending()

        # Insert the value at y in the position after x
        for i in range(y - x):
            individual[y-i-1], individual[y-i] = individual[y-i], individual[y-i-1]

        return individual

    def permutation_inversion(self, individual):
        # DONE
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
        # TODO - Implement based on representation
        # Generate two random indices in ascending order
        x, y = self.gen_two_nums_ascending()

        # Randomize the order of indices from x to y
        w = y - x
        for i in range(w):
            z = randint(0, w)
            individual[x + i], individual[x + z] = individual[x + z], individual[x + i]

        return individual

    def permutation_shift(self, individual):
        # Generate two random ranges
        x, y, w = self.gen_two_ranges()

        for i in range(y - x):
            individual[x + i], individual[w + i] = individual[w + i], individual[x + i]

        return individual
    # endregion


if __name__ == '__main__':
    from src.EA_Methods.EAVarHelper import EAVarHelper
    from time import time

    mu = MutatorHelper(EAVarHelper(20, False), 0)

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
