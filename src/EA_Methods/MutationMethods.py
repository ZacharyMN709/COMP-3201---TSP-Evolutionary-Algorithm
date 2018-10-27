from random import randint, random


# region Globals and Setters
mutation_rate = None


def set_mutation_rate(i):
    global mutation_rate
    mutation_rate = i
# endregion


def select_randomize(func):
    def select_method(offspring):
        if random() < mutation_rate:
            return func(offspring)
        else:
            return offspring
    return select_method


@select_randomize
def permutation_swap(individual):
    l = len(individual)
    x = randint(0, l - 1)
    y = (x + randint(1, l - 1)) % l
    individual[x], individual[y] = individual[y], individual[x]
    return individual


@select_randomize
def permutation_insert(individual):
    print('Stub Method!')
    return individual


@select_randomize
def permutation_inversion(individual):
    print('Stub Method!')
    return individual


@select_randomize
def permutation_scramble(individual):
    print('Stub Method!')
    return individual

