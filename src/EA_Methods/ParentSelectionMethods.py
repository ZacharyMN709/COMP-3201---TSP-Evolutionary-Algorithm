from random import sample, random

tournament_size = None  # Set to an integer value from the outside
op = None               # Set to max() or min() from the outside


def mps(fitness, mating_pool_size):
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

    for x in fit_indexes:
        while seed < x[1]:
            seed += increment
            selected_to_mate.append(x[0])

    return selected_to_mate


# TODO - Make tournament_size and op global, and declare from outside.
def tournament(fitness, mating_pool_size):
    fit_indexes = [(x, fitness[x]) for x in range(len(fitness))]
    return [op(sample(fit_indexes, tournament_size), key=lambda x: x[1])[0] for _ in range(mating_pool_size)]


def random_uniform(fitness, mating_pool_size):
    return sample([x for x in range(len(fitness))], mating_pool_size)

