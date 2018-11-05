from random import randint


# region Globals and Setters
population_size = 60
mating_pool_size = 20
op = None


def set_population_size(i):
    global population_size
    population_size = i


def set_mating_pool_size(i):
    global mating_pool_size
    mating_pool_size = i


def set_op(i):
    global op
    op = i
# endregion


# region Survivor Selection Methods
def reset_indices(func):
    def generate_output(parents, offspring):
        new_population = func(parents, offspring)
        # Select 100% of the new_population, and shuffle them, while resetting their indices
        return new_population.sample(frac=1).reset_index(drop=True)
    return generate_output


@reset_indices
def mu_plus_lambda(parents, offspring):
    # Merge the two dataframes, sort by optimality, and take the best population_size
    return parents.append(offspring).sort_values(by=['fitnesses'], ascending=(op != max)).iloc[:population_size]


@reset_indices
def replacement(parents, offspring):
    # Sort the parents by optimality, remove mating_pool_size, and append the offspring
    return parents.sort_values(by=['fitnesses'], ascending=(op != max)).iloc[:population_size-mating_pool_size].append(offspring)

    
@reset_indices
def random_uniform(parents, offspring):
    # Merge the two dataframes, and randomly select population_size
    return parents.append(offspring).sample(n=population_size)
# endregion
