from src.EA_Methods.HelperTemplate import BaseHelper
from random import randint, random, shuffle
'''
# region Globals and Setters
genome_length = 0
mutation_rate = 0.2
eval_fitness = None


def set_genome_length(i):
    global genome_length
    genome_length = i


def set_mutation_rate(i):
    global mutation_rate
    mutation_rate = i


def set_fitness_function(i):
    global eval_fitness
    eval_fitness = i
# endregion
'''


class MutatorHelper(BaseHelper):
    def __init__(self, var_helper, method):
        name_method_pairs = [('Swap', self.permutation_swap),
                             ('Insert', self.permutation_insert),
                             ('Inversion', self.permutation_inversion),
                             ('Shift', self.permutation_shift)
                             ]
        super().__init__(var_helper, method, name_method_pairs)

    def __str__(self):
        return super().__str__().format('MutatorHelper')

    def get_func_from_index(self, i):
        return self.name_method_pairs[i][1]

    # region Mutation Methods
    # Takes in a method, and then 'injects' the random chance of running into the function
    def method_mapper(self, func):
        def mutator(offspring):
            def method_randomizer(individual):
                # If apply the mutation X% of the time,
                if random() < self.vars.mutation_rate:
                    return func(individual)
                # and the original if the mutation is not applied.
                else:
                    return individual

            offspring = list(map(method_randomizer, offspring))
            return offspring, list(map(self.vars.eval_fitness, offspring))
        return mutator

    def gen_two_nums(self):
        x = randint(0, self.vars.genome_length - 1)
        y = randint(0, self.vars.genome_length - 1)
        return x, y

    def gen_two_nums_ascending(self):
        # Generate two integers such that x > y
        x = randint(0, self.vars.genome_length - 2)
        y = randint(x, self.vars.genome_length - 1)
        return x, y

    def gen_two_ranges(self):
        # Generate two integers such that x > y
        x = randint(0, self.vars.genome_length - 2)
        y = randint(x+1, self.vars.genome_length - 1)

        # Generate a third integer such that a slice starting at that location with
        # size (y-x) would fit in genome_length
        w = randint(0, self.vars.genome_length - (y-x)-1)

        return x, y, w

    @method_mapper
    def permutation_swap(self, individual):
        # DONE
        # Generate two random indices
        x, y = self.gen_two_nums()

        # Swap the values at those indices
        individual[x], individual[y] = individual[y], individual[x]

        return individual

    @method_mapper
    def permutation_insert(self, individual):
        # TODO - Implement based on representation
        # Generate two random indices
        x, y = self.gen_two_nums()

        # Insert the value at y in the position after x
        value = individual.pop(y)
        individual.insert(x+1, value)

        return individual

    @method_mapper
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

    @method_mapper
    def permutation_scramble(self, individual):
        # TODO - Implement based on representation
        # Generate two random indices in ascending order
        x, y = self.gen_two_nums_ascending()

        # Randomize the order of indices from x to y
        temp = individual[x:y]
        shuffle(temp)
        individual[x:y] = temp

        return individual

    @method_mapper
    def permutation_shift(self, individual):
        # TODO - Double Check
        # Generate two random ranges
        x, y, w = self.gen_two_ranges()

        for i in range(y-x):
            individual[x+i], individual[w+i] = individual[w+i], individual[x+i]

        return individual
    # endregion

if __name__ == '__main__':
    mu = MutatorHelper(0, 5)
