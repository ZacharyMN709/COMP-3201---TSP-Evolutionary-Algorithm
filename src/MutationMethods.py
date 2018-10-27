from random import randint


def permutation_swap(individual):
    l = len(individual)
    x = randint(0, l - 1)
    y = (x + randint(1, l - 1)) % l
    individual[x], individual[y] = individual[y], individual[x]
    return individual


def permutation_insert(individual):
    pass
    return individual


def permutation_inversion(individual):
    pass
    return individual


def permutation_scramble(individual):
    pass
    return individual

