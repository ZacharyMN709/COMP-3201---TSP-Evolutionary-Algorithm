from random import randint, choice
from time import clock


# region Globals and Setters
op = None


def set_op(i):
    global op
    op = i
# endregion


# region Survivor Selection Methods
def mu_plus_lambda(parents, parent_fitness, offspring, offspring_fitness):
    loc_op = min if op == max else max
    max_size = len(parents)

    population = parents + offspring
    fitness = parent_fitness + offspring_fitness

    # remove the weakest until the population is trimmed to size
    while len(population) > max_size:
        i = fitness.index(loc_op(fitness))
        population.pop(i)
        fitness.pop(i)

    return population, fitness


def replacement(parents, parent_fitness, offspring, offspring_fitness):
    loc_op = min if op == max else max
    max_size = len(parents) - len(offspring)

    # remove the weakest parents to make room for children
    while len(parents) > max_size:
        i = parent_fitness.index(loc_op(parent_fitness))
        parents.pop(i)
        parent_fitness.pop(i)

    # add the children
    population = parents + offspring
    fitness = parent_fitness + offspring_fitness

    return population, fitness

    
def random_uniform(parents, parent_fitness, offspring, offspring_fitness):
    max_size = len(parents)

    # merge the populations
    population = parents + offspring
    fitness = parent_fitness + offspring_fitness

    # randomly remove members until the population is trimmed to size
    while len(population) > max_size:
        x = randint(0, len(population)-1)
        population.pop(x)
        fitness.pop(x)

    return population, fitness
# endregion

if __name__ == '__main__':
    test_count = 1000
    parent = []
    parent_fitness = []
    offspring = []
    offspring_fitness = []

    for _ in range(test_count):
        parent.append(list(range(10)))
        offspring.append(list(range(10)))
        parent_fitness.append(15)
        offspring_fitness.append(15)

    start_time = clock()
    for i in range(test_count):
        random_uniform(parent, parent_fitness, offspring, offspring_fitness)
    print(clock() - start_time)
