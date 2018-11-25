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

        offspring = list(map(method_randomizer, offspring))
        return offspring, list(map(eval_fitness, offspring))
    return mutator


def gen_two_nums():
    x = randint(0, genome_length - 1)
    y = randint(0, genome_length - 1)
    return x, y


def gen_two_nums_ascending():
    # Generate two integers such that x > y
    x = randint(0, genome_length - 2)
    y = randint(x+1, genome_length - 1)
    return x, y


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
    value = individual.pop(y)
    individual.insert(x+1, value)

    return individual


@method_mapper
def permutation_inversion(individual):
    # Generate two random indices in ascending order
    x, y = gen_two_nums_ascending()

    # Reverse the contents from x to y
    individual[x:y] = individual[x:y][::-1]
    return individual


@method_mapper
def permutation_scramble(individual):
x, y = gen_two_nums_ascending()
    for i in range((y-x)//2):
        individual[x+i], individual[y-i] = individual[y-i], individual[x+i]

    return individual
# endregion


if __name__ == '__main__':
    import time
    from random import sample
    genome_length = 100
    mutation_rate = 1

    mutate = permutation_insert

    start_time = time.time()
    test = [sample([c for c in range(genome_length)], genome_length) for _ in range(genome_length)]
    for i in test:
        print(i)
        print(mutate(i))
        print('- - -')

    runtime = time.time() - start_time
    print("--- %s seconds ---" % runtime)
