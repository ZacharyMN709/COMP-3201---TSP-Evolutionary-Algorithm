from numpy.random import rand


# region Globals and Setters
tournament_size = 10
op = None


def set_tournament_size(i):
    global tournament_size
    tournament_size = i


def set_op(i):
    global op
    op = i
# endregion


# region Parent Selection Methods
def mps(population, mating_pool_size):
    selected_to_mate = []           # a list of indices of picked parents in population
    increment = 1 / mating_pool_size        # The pointer 'angle'
    seed = rand()/population.shape[0]     # The pointer start position

    population = population.assign(cumprob=(1 / population['fitnesses']) / (1 / population['fitnesses']).sum())
    population['cumprob'] = population['cumprob'].cumsum()
    # TODO - Finish. The above creates a column of the cumulative probability, leaving only selection left.

    for x in population:
        while seed < x['cumprob']:
            seed += increment
            selected_to_mate.append(x['indexes'])

    return selected_to_mate.sample(frac=1)


def tournament(population, mating_pool_size):
    population.sample(n=mating_pool_size, replace=True).sort_values(by=['fitnesses'], ascending=(op != max))
    # TODO - Finish. The above gets a single tournament, and sorts it so the top row is the winner.
    # Set below to use the n number of tournament winners
    return population.sample(n=mating_pool_size, replace=True).sort_values(by=['fitnesses'], ascending=(op != max))


def roulette(population, mating_pool_size):
    # TODO - Occasionally causes a list of booleans to appear. Unsure why.
    return population.sample(n=mating_pool_size, replace=True, weights=(1/population['fitnesses']))


def random_uniform(population, mating_pool_size):
    # TODO - Occasionally causes a list of booleans to appear. Unsure why.
    return population.sample(n=mating_pool_size, replace=True)
# endregion