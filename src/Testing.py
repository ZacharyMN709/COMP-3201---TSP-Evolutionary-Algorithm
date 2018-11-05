from random import shuffle
import time

from src.EA_Methods.List_Rep import ParentSelectionMethods as PSM
from src.EA_Methods.List_Rep import MutationMethods as MM
from src.EA_Methods.List_Rep import RecombinationMethods as RM
from src.EA_Methods.List_Rep import SurvivorSelectionMethods as SSM

PARENTS = 0
SURVIVORS = 0
MUTATIONS = 0
RECOMBINATIONS = 0
PARENT_STRINGS = ['MPS', 'Tourney']
SURVIVOR_STRINGS = ['Mu + Lambda', 'Replace']
MUTATION_STRINGS = ['Swap']
RECOMBINATION_STRINGS = ['Cut & Cross']

TEST = True
FILENUM = 1


if TEST:
    from src.Setups.EightQueens import EightQueen as DEF
    from src.Setups.EightQueens.EightQueen import random_initialization as initialize
    from src.Setups.EightQueens.EightQueen import fitness_8queen as eval_fitness
    genome_length = 8
else:
    from src.Setups.TSP import TSP_PDS as DEF
    from src.Setups.TSP.TSP_PDS import read_tsp_file as parse_file
    from src.Setups.TSP.TSP_PDS import random_initialization as initialize
    from src.Setups.TSP.TSP_PDS import euclidean_distance as eval_fitness
    from src.Setups.TSP.TSP_Inputs.Optimums import get_best_path
    genome_length = parse_file(FILENUM)


def queens():
    op_fit, optimal_solutions, generation = main(False, known_optimum=16, true_opt=True)
    return op_fit, len(optimal_solutions), generation


def tsp():
    global TEST, FILENUM
    opt_dist, opt_path, true_opt = get_best_path(FILENUM)
    op_fit, optimal_solutions, generation = main(False, known_optimum=opt_dist, true_opt=true_opt)
    print("Best individual is:")
    print(optimal_solutions[0])
    return op_fit, len(optimal_solutions), generation


def main(maximize, known_optimum=None, true_opt=False, print_gens=False):
    global TEST, FILENUM

    generation_limit = 500
    population_size = 60
    mating_pool_size = population_size//2 if (population_size//2) % 2 == 0 else (population_size//2)+1  # has to be even
    tournament_size = population_size//10
    mutation_rate = 0.2
    crossover_rate = 0.9
    crossover_point = genome_length//3

    PSM.set_tournament_size(tournament_size)
    RM.set_crossover_point(crossover_point)
    RM.set_crossover_rate(crossover_rate)
    MM.set_mutation_rate(mutation_rate)
    DEF.set_fitness_function(eval_fitness)

    # Modular function declarations
    def gte(x, y): return x >= y
    def lte(x, y): return x <= y
    op = max if maximize else min
    cmp = gte if maximize else lte
    PSM.set_op(op)
    SSM.set_op(op)

    # Initialize Population
    population, fitness = initialize(population_size, genome_length)

    for generation in range(generation_limit):

        # Generation Info
        if print_gens:
            print("Generation: {}\n  Best fitness: {}\n  Avg. fitness: {}".format(
                generation+1, op(fitness), sum(fitness)/len(fitness))
            )

        # Parent Selection
        if PARENTS == 0:
            parents_index = PSM.mps(fitness, mating_pool_size)
        elif PARENTS == 1:
            parents_index = PSM.tournament(fitness, mating_pool_size)
        else:
            parents_index = population
            shuffle(parents_index)
            print('Parent method not selected. Defaulting to original population.')

        # Recombination
        if RECOMBINATIONS == 0:
            offspring = RM.recombination_cut_crossover(population, parents_index)
        else:
            offspring = []
            print('Recombination method not selected. Defaulting to original offspring.')
            for i in range(0, mating_pool_size, 2):
                off1, off2 = population[parents_index[i]].copy(), population[parents_index[i + 1]].copy()
                offspring.append(off1)
                offspring.append(off2)

        # Mutations Selection
        if MUTATIONS == 0:
            offspring = [MM.permutation_swap(i) for i in offspring]
        else:
            print('Offspring method not selected. Defaulting to original offspring.')
        offspring_fitness = [eval_fitness(i) for i in offspring]

        # Survivor Selection
        if SURVIVORS == 0:
            population, fitness = SSM.mu_plus_lambda(population, fitness, offspring, offspring_fitness)
        elif SURVIVORS == 1:
            population, fitness = SSM.replacement(population, fitness, offspring, offspring_fitness)
        else:
            print('Survivor method not selected. Defaulting to original population and fitness.')

        # Break if converged at optimal solution
        if true_opt:
            op_fit = op(fitness)
            optimal_solutions = [i + 1 for i in range(population_size) if fitness[i] == op_fit]
            if cmp(op_fit, known_optimum) and (len(optimal_solutions) == population_size):
                print("Ending early. Converged at generation: {}/{}".format(generation, generation_limit))
                break

    # Final Fitness Info
    op_fit = op(fitness)
    optimal_solutions = [i + 1 for i in range(population_size) if fitness[i] == op_fit]
    print("Best solution fitness:", op_fit, "\nNumber of optimal solutions: ", len(optimal_solutions), '/', population_size)
    print("Best solution indexes:", optimal_solutions)
    if cmp(op_fit, known_optimum):
        print('!!!! - - - NEW BEST: {} - - - !!!!'.format(op_fit))
    # TODO - Grade efficacy based on TSP solutions.
    return op_fit, optimal_solutions, generation


if __name__ == '__main__':
    matrix = [[[[[]  # Make a matrix of empty lists.
                 # matrix[x][y][z][w] returns a list corresponding to the functions used
              for w in range(len(RECOMBINATION_STRINGS))]
              for z in range(len(MUTATION_STRINGS))]
              for y in range(len(SURVIVOR_STRINGS))]
              for x in range(len(PARENT_STRINGS))]

    best_fitnesses = matrix.copy()
    avg_fitnesses = matrix.copy()
    solutions_found = matrix.copy()
    final_generations = matrix.copy()
    times_elapsed = matrix.copy()
    op = None

    for _ in range(100):
        for x in range(len(PARENT_STRINGS)):
            for y in range(len(SURVIVOR_STRINGS)):
                for z in range(len(MUTATION_STRINGS)):
                    for w in range(len(RECOMBINATION_STRINGS)):
                        PARENTS = x
                        SURVIVORS = y
                        MUTATIONS = z
                        RECOMBINATIONS = w

                        start_time = time.time()

                        print("Parent selection: '{}', Survivor selection: '{}'".format(PARENT_STRINGS[x], SURVIVOR_STRINGS[y]))
                        print("Mutation Method: '{}', Recombination Method: '{}'".format(MUTATION_STRINGS[z], RECOMBINATION_STRINGS[w]))
                        if TEST:
                            op = max
                            op_fit, num_sols, generation = queens()
                        else:
                            op = min
                            op_fit, num_sols, generation = tsp()
                        runtime = time.time() - start_time
                        print("--- %s seconds ---" % runtime)
                        best_fitnesses[x][y][z][w].append(op_fit)
                        solutions_found[x][y][z][w].append(num_sols)
                        final_generations[x][y][z][w].append(generation)
                        times_elapsed[x][y][z][w].append(runtime)
                        print("\n -------- \n")

    for x in range(len(PARENT_STRINGS)):
        for y in range(len(SURVIVOR_STRINGS)):
            for z in range(len(MUTATION_STRINGS)):
                for w in range(len(RECOMBINATION_STRINGS)):
                    PARENTS = x
                    SURVIVORS = y
                    MUTATIONS = z
                    RECOMBINATIONS = w

                    print("Parent selection: '{}', Survivor selection: '{}'".format(PARENT_STRINGS[x], SURVIVOR_STRINGS[y]))
                    print("Mutation Method: '{}', Recombination Method: '{}'".format(MUTATION_STRINGS[z], RECOMBINATION_STRINGS[w]))
                    print("Average fitness: {}".format(sum(avg_fitnesses[x][y][z][w])/len(avg_fitnesses[x][y][z][w])))
                    print("Best fitness: {}".format(op(best_fitnesses[x][y][z][w])))
                    print("Total 'best' individuals: {}".format(sum(solutions_found[x][y][z][w])))
                    print("Total generations elapsed: {} generations".format(sum(final_generations[x][y][z][w])))
                    print("Total time elapsed: {} seconds".format(sum(times_elapsed[x][y][z][w])))
                    print("\n -------- \n")
