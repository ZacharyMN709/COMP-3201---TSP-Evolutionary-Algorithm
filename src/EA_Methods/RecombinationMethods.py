# TODO - Incorporate the mutation chance into this module

# TODO - Make pivot, and declare from outside.
def recombination_cut_crossover(parent1, parent2, pivot):
    offspring1 = parent1[:pivot] + [x for x in parent2[pivot:] + parent2[:pivot] if x not in parent1[:pivot]]
    offspring2 = parent2[:pivot] + [x for x in parent1[pivot:] + parent1[:pivot] if x not in parent2[:pivot]]
    return offspring1, offspring2


def recombination_pmx_crossover(parent1, parent2):
    print('Stub Method!')
    return parent1, parent2


def recombination_edge_crossover(parent1, parent2):
    print('Stub Method!')
    return parent1, parent2


def recombination_order_crossover(parent1, parent2):
    print('Stub Method!')
    return parent1, parent2
