from random import shuffle, sample, random

#multi-pointer selection (MPS)
def MPS(fitness, mating_pool_size):

    selected_to_mate = []  # a list of indices of picked parents in population
    total_fitness = sum(fitness)
    increment = 1/mating_pool_size  # The pointer 'angle'
    seed = random()/len(fitness)  # The pointer start position
    a = 0  # The rolling probability sum

    # makes a list with normalized cumulatively summed fitnesses, and indexes
    fit_indexes = [[x, fitness[x]/total_fitness] for x in range(len(fitness))]
    for x in fit_indexes: a += x[1]; x[1] = a;

    for x in fit_indexes:
        while seed < x[1]:
            seed += increment
            selected_to_mate.append(x[0])

    return selected_to_mate


def tournament(fitness, mating_pool_size, tournament_size, op):
    fit_indexes = [(x, fitness[x]) for x in range(len(fitness))]
    return [op(sample(fit_indexes, tournament_size), key=lambda x: x[1])[0] for _ in range(mating_pool_size)]


def random_uniform(population_size, mating_pool_size):
    return sample([x for x in range(population_size)], mating_pool_size)

