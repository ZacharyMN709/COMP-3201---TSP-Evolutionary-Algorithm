from random import randint


def permutation_swap(individual):
    mutant = individual.copy()
    x = randint(0, len(individual) - 1)
    y = (x + randint(1, len(individual) - 1)) % len(individual)
    mutant[x], mutant[y] = mutant[y], mutant[x]

    return mutant
