import numpy as np
from numpy.random import randint, rand


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


# region Mutation Methods
def method_mapper(func):
    def mutator(offspring):
        def method_randomizer(individual):
            if rand() < mutation_rate:
                return tuple(func(individual))
            else:
                return tuple(individual)

        offspring['individuals'] = offspring['individuals'].apply(method_randomizer).apply(np.array)
        offspring['fitnesses'] = offspring['individuals'].apply(eval_fitness)
        return offspring

    return mutator


@method_mapper
def permutation_swap(individual):
    x = randint(0, genome_length)
    y = (x + randint(1, genome_length)) % genome_length
    individual[x], individual[y] = individual[y], individual[x]
    return individual


@method_mapper
def permutation_insert(individual):
    print('Stub Method!')
    return individual


@method_mapper
def permutation_inversion(individual):
    print('Stub Method!')
    return individual


@method_mapper
def permutation_scramble(individual):
    print('Stub Method!')
    return individual
# endregion
