from random import randint, random


# region Globals and Setters
genome_length = 0
mutation_rate = 0.2


def set_genome_length(i):
    global genome_length
    genome_length = i


def set_mutation_rate(i):
    global mutation_rate
    mutation_rate = i
# endregion


# region Mutation Methods
def method_randomizer(func):
    def select_method(offspring):
        if random() < mutation_rate:
            return func(offspring)
        else:
            return offspring
    return select_method


@method_randomizer
def permutation_swap(individual):
    x = randint(0, genome_length - 1)
    y = (x + randint(1, genome_length - 1)) % genome_length
    individual[x], individual[y] = individual[y], individual[x]
    return individual


@method_randomizer
def permutation_insert(individual):
    print('Stub Method!')
    return individual


@method_randomizer
def permutation_inversion(individual):
    print('Stub Method!')
    return individual


@method_randomizer
def permutation_scramble(individual):
    print('Stub Method!')
    return individual
# endregion
