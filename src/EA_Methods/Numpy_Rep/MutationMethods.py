import numpy as np
from random import randint, random, shuffle


# region Globals and Setters
genome_length = 0
mutation_rate = 0.2
eval_fitness = None


def set_genome_length(i):
    global genome_length
    genome_length = i


def set_mutation_rate(i):
    global mutation_rate
    mutation_rate = i


def set_fitness_function(i):
    global eval_fitness
    eval_fitness = i
# endregion


# region Mutation Methods

# Takes in a method, and then 'injects' the random chance of running into the function
def method_mapper(func):
    def mutator(offspring):
        def method_randomizer(individual):
            # If apply the mutation X% of the time,
            if random() < mutation_rate:
                return func(individual)
            # and the original if the mutation is not applied.
            else:
                return individual

        offspring = [method_randomizer(i) for i in offspring]
        return offspring, [eval_fitness(i) for i in offspring]
    return mutator


def gen_two_nums():
    x = randint(0, genome_length-1)
    y = randint(0, genome_length-1)
    return x, y


def gen_two_nums_ascending():
    x = randint(0, genome_length-2)
    y = randint(x, genome_length-1)
    return x, y


def gen_two_ranges():
    # Generate two integers such that x > y
    x = randint(0, genome_length - 2)
    y = randint(x+1, genome_length - 1)

    # Generate a third integer such that a slice starting at that location with
    # size (y-x) would fit in genome_length
    w = randint(0, genome_length - (y-x)-1)

    return x, y, w


@method_mapper
def permutation_swap(individual):
    # Generate two random indices
    x, y = gen_two_nums()

    # Swap the values at those indices
    individual[x], individual[y] = individual[y], individual[x]

    return individual


@method_mapper
def permutation_insert(individual):
    # Generate two random indices
    x, y = gen_two_nums()

    # Insert the value at y in the position after x
    #a = np.asarray([1, 2, 3, 4])
    #np.insert(a, 2, 66)
    # >>> array([1, 2, 66, 3, 4])
    value = individual.pop(y)
    individual.insert(x+1, value)

    return individual


@method_mapper
def permutation_inversion(individual):
    # Generate two random indices in ascending order
    x, y = gen_two_nums_ascending()

    # Reverse the contents from x to y, and concatenate
    individual[x:y] = individual[x:y][::-1]
    return individual


@method_mapper
def permutation_scramble(individual):
    # Generate two random indices in ascending order
    x, y = gen_two_nums()

    # Randomize the order of indices from x to y, and concatenate
    individual[x:y] = np.shuffle(individual[x:y])
    return np.concatenate((individual[:x], individual[x:y].sample(frac=1), individual[y:]), axis=None)


@method_mapper
def permutation_shift(individual):
    # Generate two random indices in ascending order
    x, y, w = gen_two_ranges()

    for i in range(y-x):
        individual[x+i], individual[w+i] = individual[w+i], individual[x+i]

    return individual
# endregion


if __name__ == '__main__':
    import time
    from random import sample
    genome_length = 100
    test_count = 1000000
    mutation_rate = 1

    test = [np.random.permutation(genome_length) for _ in range(test_count)]

    start_time = time.time()
    for i in test:
        permutation_inversion(i)
    runtime = time.time() - start_time
    print("--- %s seconds ---" % runtime)
