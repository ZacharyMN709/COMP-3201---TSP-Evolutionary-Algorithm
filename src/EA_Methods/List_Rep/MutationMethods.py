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


def gen_two_nums():
    x = randint(0, genome_length - 1)
    y = (x + randint(1, genome_length - 1)) % genome_length
    if x > y: x, y = y, x
    return x, y


@method_randomizer
def permutation_swap(individual):
    x, y = gen_two_nums()
    individual[x], individual[y] = individual[y], individual[x]
    return individual


@method_randomizer
def permutation_insert(individual):
    x, y = gen_two_nums()
    ele = individual.pop(y)
    individual.insert(x, ele)
    return individual


@method_randomizer
def permutation_inversion(individual):
    x, y = gen_two_nums()
    if y - x == 1: y += 1
    return individual[:x] + individual[y-1:x-1:-1] + individual[y:]


@method_randomizer
def permutation_scramble(individual):
    x, y = gen_two_nums()
    if y - x == 1: y += 1
    temp = individual[x:y]
    shuffle(temp)
    return individual[:x] + temp + individual[y:]
# endregion


if __name__ == '__main__':
    genome_length = 10
    mutation_rate = 1
    test = [sample([c for c in range(genome_length)], genome_length) for _ in range(genome_length)]
    for x in test:
        print(x)
        print(permutation_scramble(x))
        print('- - -')
