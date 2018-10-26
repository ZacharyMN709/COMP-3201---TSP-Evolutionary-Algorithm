from random import shuffle, random

from EightQueenSetup import random_initialization as initialize
from EightQueenSetup import fitness_8queen as eval_fitness
from EightQueenSetup import permutation_cut_and_crossfill as recombine
import MutationMethods as mutation
import ParentSelectionMethods as parentSelection
import SurvivorSelectionMethods as survivorSelection


PARENTS = 0
SURVIVOR = 0
PARENT_STRINGS = ['MPS', 'Tourney', 'Random']
SURVIVOR_STRINGS = ['Mu + Lambda', 'Replace', 'Random']


def main(generation_limit):
    genome_length = 8
    population_size = 60
    mating_pool_size = population_size//2 if (population_size//2) % 2 == 0 else (population_size//2)+1 # has to be even
    tournament_size = 3
    mutation_rate = 0.2
    crossover_rate = 0.9

    population = initialize(population_size, genome_length)
    fitness = [eval_fitness(i) for i in population]

    for generation in range(generation_limit):
        print("Generation: {}\n  Best fitness: {}\n  Avg. fitness: {}".format(
            generation+1, max(fitness), sum(fitness)/len(fitness))
        )

        # TODO - Use module abilities to dynamically
        if PARENTS == 0:
            parents_index = parentSelection.MPS(fitness, mating_pool_size)
        elif PARENTS == 1:
            parents_index = parentSelection.tournament(fitness, mating_pool_size, tournament_size)
        elif PARENTS == 2:
            parents_index = parentSelection.random_uniform(population_size, mating_pool_size)
        else:
            parents_index = population
            print('Parent method not selected. Defaulting to original population.')
        shuffle(parents_index)

        offspring = []
        for i in range(0, mating_pool_size, 2):
            if random.random() < crossover_rate:
                off1, off2 = recombine(population[parents_index[i]], population[parents_index[i+1]])
            else:
                off1 = population[parents_index[i]].copy()
                off2 = population[parents_index[i+1]].copy()
            offspring.append(off1)
            offspring.append(off2)

        offspring = [mutation.permutation_swap(i) if random.random() < mutation_rate else i for i in offspring]
        offspring_fitness = [eval_fitness(i) for i in offspring]

        # TODO - Use module abilities to dynamically
        if SURVIVOR == 0:
            population, fitness = survivorSelection.mu_plus_lambda(population, fitness, offspring, offspring_fitness)
        elif SURVIVOR == 1:
            population, fitness = survivorSelection.replacement(population, fitness, offspring, offspring_fitness)
        elif SURVIVOR == 2:
            population, fitness = survivorSelection.random_uniform(population, fitness, offspring, offspring_fitness)
        else:
            print('Survivor method not selected. Defaulting to original population and fitness.')

    max_fit = max(fitness)
    optimal_solutions = [i + 1 for i in range(population_size) if fitness[i] == max_fit]
    print("Best solution indexes:", optimal_solutions)


if __name__ == '__main__':
    generation_limit = 50

    for x in range(3):
        for y in range(3):
            PARENTS = x
            SURVIVOR = y

            print("Parent selection {}, and survivor selection {}".format(PARENT_STRINGS[x], SURVIVOR_STRINGS[y]))
            main(generation_limit)
            print("\n -------- \n")
