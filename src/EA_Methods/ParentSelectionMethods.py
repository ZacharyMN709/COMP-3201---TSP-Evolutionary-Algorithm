from random import sample, random, shuffle


# region Globals and Setters
tournament_size = None
op = None


def set_tournament_size(i):
    global tournament_size
    tournament_size = i


def set_op(i):
    global op
    op = i
# endregion


def randomize_output(func):
    def generate_output(fitness, mating_pool_size):
        selected_to_mate = func(fitness, mating_pool_size)
        shuffle(selected_to_mate)
        return selected_to_mate
    return generate_output


@randomize_output
def mps(fitness, mating_pool_size):
    selected_to_mate = []           # a list of indices of picked parents in population
    total_fitness = sum(fitness)
    increment = 1/mating_pool_size  # The pointer 'angle'
    seed = random()/len(fitness)    # The pointer start position
    a = 0                           # The rolling probability sum

    # makes a list with normalized cumulatively summed fitnesses, and indexes
    fit_indexes = [[x, fitness[x]/total_fitness] for x in range(len(fitness))]
    for x in fit_indexes:
        a += x[1]
        x[1] = a

    for x in fit_indexes:
        while seed < x[1]:
            seed += increment
            selected_to_mate.append(x[0])

    return selected_to_mate


@randomize_output
def tournament(fitness, mating_pool_size):
    fit_indexes = [(x, fitness[x]) for x in range(len(fitness))]
    return [op(sample(fit_indexes, tournament_size), key=lambda x: x[1])[0] for _ in range(mating_pool_size)]


@randomize_output
def random_uniform(fitness, mating_pool_size):
    return sample([x for x in range(len(fitness))], mating_pool_size)

