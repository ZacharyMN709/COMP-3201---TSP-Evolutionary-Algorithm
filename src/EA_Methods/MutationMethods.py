from random import randint, random


# region Globals and Setters
mutation_rate = None


def set_mutation_rate(i):
    global mutation_rate
    mutation_rate = i
# endregion


def method_randomizer(func):
    def select_method(offspring):
        if random() < mutation_rate:
            return func(offspring)
        else:
            return offspring
    return select_method


@method_randomizer
def permutation_swap(individual):
    l = len(individual)
    x = randint(0, l - 1)
    y = (x + randint(1, l - 1)) % l
    individual[x], individual[y] = individual[y], individual[x]
    return individual


@method_randomizer
def permutation_insert(individual):
    print('Stub Method!')
    return individual


@method_randomizer
def permutation_inversion(individual):
    print('Stub Method!')
    return individual


@method_randomizer
def permutation_scramble(individual):
    print('Stub Method!')
    return individual

