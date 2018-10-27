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


def select_randomize(func):
    def select_method(parent1, parent2):
        if random() < crossover_rate:
            return func(parent1, parent2)
        else:
            return parent1.copy(), parent2.copy()
    return select_method


@select_randomize
def recombination_cut_crossover(parent1, parent2):
    offspring1 = parent1[:pivot] + [x for x in parent2[pivot:] + parent2[:pivot] if x not in parent1[:pivot]]
    offspring2 = parent2[:pivot] + [x for x in parent1[pivot:] + parent1[:pivot] if x not in parent2[:pivot]]
    return offspring1, offspring2


@select_randomize
def recombination_pmx_crossover(parent1, parent2):
    print('Stub Method!')
    return parent1, parent2


@select_randomize
def recombination_edge_crossover(parent1, parent2):
    print('Stub Method!')
    return parent1, parent2


@select_randomize
def recombination_order_crossover(parent1, parent2):
    print('Stub Method!')
    return parent1, parent2
