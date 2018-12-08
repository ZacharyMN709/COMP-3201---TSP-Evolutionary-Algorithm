from time import time

def run(self, pipe, methods, vars, generation_limit, known_optimum=None, true_opt=False, report_rate=0, print_final=True):
    def best_of(fitness):
        pass

    eval_fitness = methods["eval_fitness"]
    initialize = methods["initialize"]
    select_parents = methods["select_parents"]
    generate_offspring = methods["generate_offspring"]
    apply_mutation = methods["apply_mutation"]
    select_survivors = methods["select_survivors"]
    manage_population = methods["manage_population"]

    population_size = vars["population_size"]

    master_start_time = time()
    best_indivs = [None] * generation_limit

    PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime = 0, 0, 0, 0, 0, 0

    # Initialize Population
    start_time = time()
    population, fitness = initialize()
    PITime += time() - start_time

    for generation in range(1, generation_limit + 1):
        # Output generation statistics
        if report_rate != 0 and generation % report_rate == 0:
            # Are we using multithreading?
            if pipe:
                # Send stats back to main thread
                pipe.send([False, generation, best_of(fitness), sum(fitness)/population_size])
            else:
                # Print stats
                print("Generation: {}\n  Best fitness: {}\n  Avg. fitness: {}".format(generation, self.vars.best_of(fitness), sum(fitness)/population_size))

        start_time = time()
        parents_index = select_parents(fitness)
        PSMTime += time() - start_time

        start_time = time()
        offspring = generate_offspring(population, parents_index)
        RMTime += time() - start_time

        start_time = time()
        offspring, offspring_fitness = apply_mutation(offspring)
        MMTime += time() - start_time

        start_time = time()
        population, fitness = select_survivors(population, fitness, offspring, offspring_fitness)
        SSMTime += time() - start_time

        start_time = time()
        population, fitness = manage_population(population, fitness)
        PMMTime += time() - start_time

        # Break if converged at optimal solution
        op_fit = self.vars.best_of(fitness)
        optimal_solutions = [i for i in range(population_size) if fitness[i] == op_fit]
        best_indivs[generation - 1] = (op_fit, population[optimal_solutions[0]][:])
        if true_opt and self.vars.as_good_as(op_fit, known_optimum) and (
                len(optimal_solutions) == population_size):
            print("Ending early. Converged at generation: {}/{}".format(generation, generation_limit))
            break

    # Final Fitness Info
    master_time = time() - master_start_time
    op_fit = self.vars.best_of(fitness)
    best_indivs = best_indivs[:generation - 1]
    optimal_solutions = [i for i in range(population_size) if fitness[i] == op_fit]
    total_time = sum([PSMTime, RMTime, MMTime, SSMTime, PMMTime])
    time_tuple = (PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time)

    if print_final:
        print("Best solution fitness:", op_fit)
        if true_opt: print(
            "Best solution {:4.2f}% larger than true optimum.".format(100 * ((op_fit / known_optimum) - 1)))
        print("Number of optimal solutions: ", len(optimal_solutions), '/', population_size)
        print("Best solution indexes:", optimal_solutions)
        if known_optimum and self.vars.better_than(op_fit, known_optimum):
            print('!!!! - - - NEW BEST: {} - - - !!!!'.format(op_fit))
        print("Best solution path:", population[optimal_solutions[0]])
        # print(timed_funcs.format(PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time))
        print("--- {} seconds ---".format(master_time))

    return op_fit, optimal_solutions, generation, best_indivs, time_tuple
