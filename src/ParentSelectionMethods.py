import random

#multi-pointer selection (MPS)
def MPS(fitness, mating_pool_size):

    selected_to_mate = []  # a list of indices of picked parents in population

    #student code begin

    total_fitness = sum(fitness)
    increment = 1/mating_pool_size  # The pointer 'angle'
    seed = random.random()/len(fitness)  # The pointer start position
    a = 0  # The rolling probability sum

    # makes a list with normalized cumulatively summed fitnesses, and indexes
    fit_indexes = [[x, fitness[x]/total_fitness] for x in range(len(fitness))]
    for x in fit_indexes: a += x[1]; x[1] = a;

    # Add members based on where the pointers land
    for x in fit_indexes:
        while seed < x[1]:
            seed += increment
            selected_to_mate.append(x[0])

    #student code end

    return selected_to_mate


#tournament selection
def tournament(fitness, mating_pool_size, tournament_size):

    selected_to_mate = []  # a list of indices of picked parents in population

    #student code begin

    # makes a list of indexes and fitnesses
    fit_indexes = [(x, fitness[x]) for x in range(len(fitness))]

    for x in range(mating_pool_size):
        # randomly shuffles the list, and picks the max of the first x, and adds it
        random.shuffle(fit_indexes)
        selected_to_mate.append(max(fit_indexes[:tournament_size], key=lambda x: x[1])[0])

    #student code end

    return selected_to_mate


#randomly uniformly pick parents regardless of their fitness 
def random_uniform(population_size, mating_pool_size):

    #student code begin

    # Make a list of indexes, shuffle it, and take the first x.
    selected_to_mate = [x for x in range(population_size)]
    random.shuffle(selected_to_mate)
    selected_to_mate = selected_to_mate[:mating_pool_size]

    #student code end

    #selected_to_mate = random.sample([x for x in range(population_size)], mating_pool_size)

    return selected_to_mate

