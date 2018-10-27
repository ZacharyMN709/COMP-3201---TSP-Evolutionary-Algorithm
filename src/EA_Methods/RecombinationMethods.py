from random import random


# region Globals and Setters
pivot = None
crossover_rate = None


def set_crossover_point(i):
    global pivot
    pivot = i


def set_crossover_rate(i):
    global crossover_rate
    crossover_rate = i
# endregion


def method_iterator(func):
    def method_appicator(population, parents_index):
        offspring = []
        for i in range(0, len(parents_index), 2):
            if random() < crossover_rate:
                off1, off2 = func(population[parents_index[i]], population[parents_index[i + 1]])
            else:
                off1, off2 = population[parents_index[i]].copy(), population[parents_index[i + 1]].copy()
            offspring.append(off1)
            offspring.append(off2)
        return offspring
    return method_appicator


def method_randomizer(func):
    def select_method(population, parents_index):
        offspring = []
        for i in range(0, len(parents_index), 2):
            if random() < crossover_rate:
                off1, off2 = func(population[parents_index[i]], population[parents_index[i + 1]])
            else:
                off1, off2 = population[parents_index[i]].copy(), population[parents_index[i + 1]].copy()
            offspring.append(off1)
            offspring.append(off2)
        return offspring
    return select_method


@method_randomizer
def recombination_cut_crossover(parent1, parent2):
    offspring1 = parent1[:pivot] + [x for x in parent2[pivot:] + parent2[:pivot] if x not in parent1[:pivot]]
    offspring2 = parent2[:pivot] + [x for x in parent1[pivot:] + parent1[:pivot] if x not in parent2[:pivot]]
    return offspring1, offspring2


@method_randomizer
def recombination_pmx_crossover(parent1, parent2):
    print('Stub Method!')
    return parent1, parent2


@method_randomizer
def recombination_edge_crossover(parent1, parent2):
    print('Stub Method!')
    return parent1, parent2


@method_randomizer
def recombination_order_crossover(parent1, parent2):
    print('Stub Method!')
    return parent1, parent2
