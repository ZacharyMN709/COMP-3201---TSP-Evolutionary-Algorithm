import random

#mu+lambda selection to pick survivors
def mu_plus_lambda(parents, parent_fitness, offspring, offspring_fitness):
    
    #student code begin

    max_size = len(parents)

    # merge the populations
    population = parents + offspring
    fitness = parent_fitness + offspring_fitness

    # remove the weakest until the population is trimmed to size
    while len(population) > max_size:
        i = fitness.index(min(fitness))
        population.pop(i)
        fitness.pop(i)

    #student code end
   
    return population, fitness


#use offspring to replace the same number of worst parents
def replacement(parents, parent_fitness, offspring, offspring_fitness):
    
    #student code begin

    max_size = len(parents) - len(offspring)

    # remove the weakest parents to make room for children
    while len(parents) > max_size:
        i = parent_fitness.index(min(parent_fitness))
        parents.pop(i)
        parent_fitness.pop(i)

    # add the children
    population = parents + offspring
    fitness = parent_fitness + offspring_fitness

    #student code end
   
    return population, fitness

    
#randomly uniformly pick survivors from parents and offspring
def random_uniform(parents, parent_fitness, offspring, offspring_fitness):

    #student code begin

    max_size = len(parents)

    # merge the populations
    population = parents + offspring
    fitness = parent_fitness + offspring_fitness

    # randomly remove members until the population is trimmed to size
    while len(population) > max_size:
        x = random.randint(0, len(population)-1)
        population.pop(x)
        fitness.pop(x)

    #student code end
   
    return population, fitness
    


