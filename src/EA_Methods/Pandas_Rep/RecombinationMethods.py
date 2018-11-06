from numpy.random import rand
import numpy as np


# region Globals and Setters
genome_length = 0
pivot = 10
shift = 5
crossover_rate = 0.9


def set_genome_length(i):
    global genome_length
    genome_length = i
    global shift
    shift = i - pivot


def set_crossover_point(i):
    global pivot
    pivot = i
    global shift
    shift = genome_length - i


def set_crossover_rate(i):
    global crossover_rate
    crossover_rate = i
# endregion


# region Recombination Methods
def method_mapper(func):
    def recombinator(parents):
        # TODO - This is having trouble saving the numpy array as an element.
        def method_randomizer(individual):
            if rand() < crossover_rate:
                if individual.name % 2 == 0: mate = parents.iloc[individual.name + 1]
                else: mate = parents.iloc[individual.name - 1]
                return tuple(func(individual['individuals'], mate['individuals']))
            else:
                return tuple(individual['individuals'])

        parents['individuals'] = parents.apply(method_randomizer, axis=1).apply(np.array)
        return parents

    return recombinator


@method_mapper
def recombination_cut_crossover(individual, mate):
    temp = np.roll(mate, shift)
    mask = np.isin(temp, individual[:pivot], invert=True)
    return np.concatenate((individual[:pivot], temp[mask]), axis=None)


@method_mapper
def recombination_pmx_crossover(individual, mate):
    print('Stub Method!')
    return individual


@method_mapper
def recombination_edge_crossover(individual, mate):
    print('Stub Method!')
    return individual


@method_mapper
def recombination_order_crossover(individual, mate):
    print('Stub Method!')
    return individual
# endregion
