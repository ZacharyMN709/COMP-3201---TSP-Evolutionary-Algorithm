from numpy.random import rand
import numpy as np


# region Globals and Setters
genome_length = 0
pivot = 10
crossover_rate = 0.9


def set_genome_length(i):
    global genome_length
    genome_length = i


def set_crossover_point(i):
    global pivot
    pivot = i


def set_crossover_rate(i):
    global crossover_rate
    crossover_rate = i
# endregion


# region Recombination Methods
def method_mapper(func):
    def recombinator(parents):
        def method_randomizer(individual):
            if rand() < crossover_rate:
                index = parents.index.get_loc(individual.name)
                if index % 2 == 0: mate = parents.iloc[index + 1]
                else: mate = parents.iloc[index - 1]
                return func(individual, mate)
            else:
                return individual

        parents = parents.apply(method_randomizer, axis=1)
        return parents

    return recombinator


@method_mapper
def recombination_cut_crossover(individual, mate):
    temp = np.roll(mate['individuals'], genome_length - pivot)
    mask = np.isin(temp, individual['individuals'][:pivot], invert=True)
    return np.concatenate((individual['individuals'][:pivot], temp[mask]), axis=None), individual['fitnesses']


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
