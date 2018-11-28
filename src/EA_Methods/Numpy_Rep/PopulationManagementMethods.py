from random import random, sample, shuffle, randint


def gte(x, y):
    return x >= y


def lte(x, y):
    return x <= y


def gt(x, y):
    return x > y


def lt(x, y):
    return x < y


# region Globals and Setters
genome_length = 0
population_method = None
eval_fitness = None
distances = None
op = None
cmp_eq = None
cmp_ne = None
start_temp = 10000
cooling_rate = 0.99
population_threshold = 20


def make_indiv(genome_length):
    sample([c for c in range(genome_length)], genome_length)
population_method = make_indiv


def set_genome_length(i):
    global genome_length
    genome_length = i


def set_population_method(i):
    global population_method
    population_method = i


def set_fitness_function(i):
    global eval_fitness
    eval_fitness = i


def set_distances(i):
    global distances
    distances = i


def set_op(i):
    global op, cmp_eq, cmp_ne
    cmp_eq = gte if op == max else lte
    cmp_ne = gt if op == max else lt
    op = i


def set_start_temp(i):
    global start_temp
    start_temp = i


def set_cooling_rate(i):
    global cooling_rate
    cooling_rate = i


def set_population_threshold(i):
    global population_threshold
    population_threshold = i
# endregion


# region Population Management Methods
def static_return(population, fitness):
    """
    Makes no changes to the population
    """
    return population, fitness


def metallurgic_annealing(population, fitness):
    """
    A function based on the principle of 'Annealing' in metalworking. While the algorithm is in
    its youth, we allow optimal answers to be replaced with new individuals based on a threshold
    probability which is gauged by the 'temperature' and 'cooling rate'
    """

    global start_temp
    start_temp *= cooling_rate

    new_pop = [sample([c for c in range(genome_length)], genome_length) for _ in range(len(population))]
    new_fit = [eval_fitness(x) for x in new_pop]

    for x in range(len(population)):
        if cmp_ne(new_fit[x], fitness[x]) or random() < 2.7182818**((fitness[x] - new_fit[x])/start_temp):
            population[x] = new_pop[x]

    return population, fitness


def entropic_stabilizing(population, fitness):
    """
    A process where the more individuals of the current best fitness there
    that exist, the more likely it is that the individuals are randomly
    replaced with new individuals,
    """

    best_fit = op(fitness)
    num_best = fitness.count(best_fit)

    if num_best > population_threshold:
        threshold = 0.8*((num_best - population_threshold) / (len(population) - population_threshold))
        for x in range(len(population)):
            if fitness[x] == best_fit and random() < threshold:
                shuffle(population[x])
                fitness[x] = eval_fitness(population[x])

    return population, fitness


def ouroboric_culling(population, fitness):
    """
    Like the snake of legend, as the algorithm grows and stabilizes,
    it ends up 'eating' itself. It does this by limiting the percent
    of individuals which can share the maximum fitness.
    """

    best_fit = op(fitness)
    num_best = fitness.count(best_fit)
    if num_best > population_threshold:
        num_to_remove = num_best - population_threshold
        for x in range(genome_length):
            if fitness[x] == best_fit:
                shuffle(population[x])
                fitness[x] = eval_fitness(population[x])
                num_to_remove -= 1
                if num_to_remove == 0:
                    break

    return population, fitness


def genetic_engineering(population, fitness):
    """
    Shuffle all of the genes next to each other, and see if it improves.
    If not, revert that change. Super charges a single fittest individual.
    """

    best_fit = op(fitness)
    num_best = fitness.count(best_fit)

    if num_best > population_threshold:
        x = randint(1, 10)
        index = fitness.index(best_fit)
        indiv = population[index]
        for i in range(len(indiv)):
            indiv[i - x], indiv[i] = indiv[i], indiv[i - x]
            new_fit = eval_fitness(indiv)
            if new_fit == op(new_fit, best_fit):
                best_fit = new_fit
            else:
                indiv[i - x], indiv[i] = indiv[i], indiv[i - x]

    return population, fitness
# endregion
