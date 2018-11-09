from random import randint, random, sample, shuffle


# region Globals and Setters
genome_length = 0
mutation_rate = 0.2


def set_genome_length(i):
    global genome_length
    genome_length = i


def set_mutation_rate(i):
    global mutation_rate
    mutation_rate = i
# endregion


# region Mutation Methods
def method_randomizer(func):
    def select_method(offspring):
        if random() < mutation_rate:
            return func(offspring)
        else:
            return offspring
    return select_method


def gen_two_nums(substring):
    x = randint(0, genome_length - 1)
    y = (x + randint(1, genome_length - 1)) % genome_length
    if x > y: x, y = y, x
    if substring and y - x == 1:
        if y != genome_length - 1: return x, y + 1
        else: return x - 1, y
    else: return x, y


@method_randomizer
def permutation_swap(individual):
    # Generate two random indices
    x = randint(0, genome_length-1)
    y = (x + randint(1, genome_length-1)) % genome_length

    # Swap the values at those indices
    individual[x], individual[y] = individual[y], individual[x]

    return individual


@method_randomizer
def permutation_insert(individual):
    # Generate two random indices
    x = randint(0, genome_length-1)
    y = (x + randint(1, genome_length-1)) % genome_length

    # Insert the value at y in the position after x
    value = individual.pop(y)
    individual.insert(x, value)

    return individual


@method_randomizer
def permutation_inversion(individual):
    # Generate two random indices in ascending order
    x, y = gen_two_nums(True)

    # Reverse the contents from x to y
    return individual[:x] + individual[x:y][::-1] + individual[y:]


@method_randomizer
def permutation_scramble(individual):
    # Generate two random indices in ascending order
    x, y = gen_two_nums(True)

    # Randomize the order of indices from x to y
    temp = shuffle(individual[x:y])
    
    return individual[:x] + temp + individual[y:]
# endregion


if __name__ == '__main__':
    genome_length = 10
    mutation_rate = 1
    test = [sample([c for c in range(genome_length)], genome_length) for _ in range(genome_length)]
    for i in test:
        print(i)
        print(permutation_inversion(i))
        print('- - -')
