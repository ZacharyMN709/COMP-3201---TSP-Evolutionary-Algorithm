import time


def gte(x, y):
    return x >= y


def lte(x, y):
    return x <= y


def gt(x, y):
    return x > y


def lt(x, y):
    return x < y


class EARunner:

    def __init__(self, PSM, RM, MM, SSM, DEF):
        self.PSM = PSM
        self.RM = RM
        self.MM = MM
        self.SSM = SSM
        self.DEF = DEF
        self.op = max if self.DEF.MAX else min
        self.cmp_eq = gte if self.DEF.MAX else lte
        self.cmp_ne = gt if self.DEF.MAX else lt
        self.runnable = False
        self.testable =False

        self.genome_length = None
        self.initialize = None
        self.eval_fitness = None
        self.parent_selection = None
        self.generate_offspring = None
        self.apply_mutation = None
        self.select_survivors = None

    def set_funcs(self, genome_len, fit_eval, pop_init, psm, rm, mm, ssm):
        self.genome_length = genome_len
        self.eval_fitness = fit_eval
        self.initialize = pop_init
        self.parent_selection = psm
        self.generate_offspring = rm
        self.apply_mutation = mm
        self.select_survivors = ssm

        self.runnable = genome_len and fit_eval and pop_init and psm and rm and mm and ssm

    def evo_algo(self, generation_limit, known_optimum=None, true_opt=False, print_gens=0):
        if not self.runnable:
            print("Error! Missing information to run EA. Please check the code for errors.")
            return

        population_size = 60
        mating_pool_size = population_size//2 if (population_size//2) % 2 == 0 else (population_size//2)+1  # has to be even
        tournament_size = population_size//10
        mutation_rate = 0.2
        crossover_rate = 0.9
        cp_1, cp_2, cp_3 = self.genome_length//4, 2*self.genome_length//4, 3*self.genome_length//4

        self.PSM.set_tournament_size(tournament_size)
        self.RM.set_genome_length(self.genome_length)
        self.RM.set_crossover_points(cp_1, cp_2, cp_3)
        self.RM.set_crossover_rate(crossover_rate)
        self.MM.set_mutation_rate(mutation_rate)
        self.MM.set_genome_length(self.genome_length)
        self.MM.set_fitness_function(self.eval_fitness)
        self.DEF.set_fitness_function(self.eval_fitness)
        self.PSM.set_op(self.op)
        self.SSM.set_op(self.op)

        # Initialize Population
        population, fitness = self.initialize(population_size, self.genome_length)

        for generation in range(1, generation_limit + 1):

            # Generation Info
            if print_gens != 0 and generation % print_gens == 0:
                print("Generation: {}\n  Best fitness: {}\n  Avg. fitness: {}".format(
                    generation, self.op(fitness), sum(fitness)/len(fitness))
                )

            parents_index = self.parent_selection(fitness, mating_pool_size)
            offspring = self.generate_offspring(population, parents_index)
            offspring, offspring_fitness = self.apply_mutation(offspring)
            population, fitness = self.select_survivors(population, fitness, offspring, offspring_fitness)

            # Break if converged at optimal solution
            if true_opt:
                op_fit = self.op(fitness)
                optimal_solutions = [i + 1 for i in range(population_size) if fitness[i] == op_fit]
                if self.cmp_eq(op_fit, known_optimum) and (len(optimal_solutions) == population_size):
                    print("Ending early. Converged at generation: {}/{}".format(generation, generation_limit))
                    break

        # Final Fitness Info
        op_fit = self.op(fitness)
        optimal_solutions = [i + 1 for i in range(population_size) if fitness[i] == op_fit]
        print("Best solution fitness:", op_fit)
        if true_opt: print("Best solution {:4.2f}% larger than true optimum.".format(100*((op_fit/known_optimum)-1)))
        print("Number of optimal solutions: ", len(optimal_solutions), '/', population_size)
        print("Best solution indexes:", optimal_solutions)
        if self.cmp_ne(op_fit, known_optimum):
            print('!!!! - - - NEW BEST: {} - - - !!!!'.format(op_fit))
        print("Best solution path:", population[optimal_solutions[0]])
        # print('--- Solution Length: {} ---'.format(len(population[optimal_solutions[0]])))
        # TODO - Grade efficacy based on TSP solutions.
        return op_fit, optimal_solutions, generation

    def set_test_vars(self, pop, par, rec, mut, sur, runs):
        self.POPULATION_METHODS = pop
        self.PARENT_METHODS = par
        self.RECOMBINATION_METHODS = rec
        self.MUTATION_METHODS = mut
        self.SURVIVOR_METHODS = sur
        self.RUNS = runs

        self.testable = pop and par and rec and mut and sur and runs

    def iterate_tests(self, generation_limit, known_optimum=None, true_opt=False, print_gens=False):
        if not self.testable:
            print("Error! Missing information to run tests. Please check the code for errors.")
            return

        def run_test(v, w, x, y, z):
            start_time = time.time()
            if len(self.POPULATION_METHODS) != 1:
                print("Population initialization: '{}'".format(self.POPULATION_METHODS[v][0]))
            print("Parent selection: '{}', Survivor selection: '{}'".format(
                self.PARENT_METHODS[w][0], self.SURVIVOR_METHODS[z][0]))
            print("Mutation Method: '{}', Recombination Method: '{}'".format(
                self.MUTATION_METHODS[y][0], self.RECOMBINATION_METHODS[x][0]))

            self.set_funcs(self.genome_length, self.eval_fitness,
                           self.POPULATION_METHODS[v][1], self.PARENT_METHODS[w][1], self.RECOMBINATION_METHODS[x][1],
                           self.MUTATION_METHODS[y][1], self.SURVIVOR_METHODS[z][1])
            op_fit, optimal_solutions, generation = self.evo_algo(generation_limit, known_optimum, true_opt, print_gens)

            runtime = time.time() - start_time
            print("--- %s seconds ---" % runtime)
            best_fitnesses[v][w][x][y][z].append(op_fit)
            solutions_found[v][w][x][y][z].append(len(optimal_solutions))
            final_generations[v][w][x][y][z].append(generation)
            times_elapsed[v][w][x][y][z].append(runtime)
            print("\n -------- \n")

        def print_final(v, w, x, y, z):
            if len(self.POPULATION_METHODS) != 1:
                print("Population initialization: '{}'".format(self.POPULATION_METHODS[v][0]))
            print("Parent selection: '{}', Survivor selection: '{}'".format(
                self.PARENT_METHODS[w][0], self.SURVIVOR_METHODS[z][0]))
            print("Mutation Method: '{}', Recombination Method: '{}'".format(
                self.MUTATION_METHODS[y][0], self.RECOMBINATION_METHODS[x][0]))
            mean = sum(best_fitnesses[v][w][x][y][z]) / len(best_fitnesses[v][w][x][y][z])
            print("Average fitness: {}".format(mean))
            if true_opt: print(
                "Average solution {:4.2f}% larger than true optimum.".format(100 * ((mean / known_optimum) - 1)))
            best = self.op(best_fitnesses[v][w][x][y][z])
            print("Best fitness: {}".format(best))
            if true_opt: print(
                "Best solution {:4.2f}% larger than true optimum.".format(100 * ((best / known_optimum) - 1)))
            print("Total 'best' individuals: {}".format(sum(solutions_found[v][w][x][y][z])))
            print("Total generations elapsed: {} generations".format(sum(final_generations[v][w][x][y][z])))
            print("Total time elapsed: {} seconds".format(sum(times_elapsed[v][w][x][y][z])))
            print("\n -------- \n")

        # Stats Set-up
        import copy

        matrix = [[[[[[]  # Make a matrix of empty lists.
                      # matrix[v][w][x][y][z] returns a list corresponding to the functions used
                      for z in range(len(self.SURVIVOR_METHODS))]
                     for y in range(len(self.MUTATION_METHODS))]
                    for x in range(len(self.RECOMBINATION_METHODS))]
                   for w in range(len(self.PARENT_METHODS))]
                  for v in range(len(self.POPULATION_METHODS))]

        best_fitnesses = copy.deepcopy(matrix)
        solutions_found = copy.deepcopy(matrix)
        final_generations = copy.deepcopy(matrix)
        times_elapsed = copy.deepcopy(matrix)

        # EA Iterator
        for _ in range(self.RUNS):
            for v in range(len(self.POPULATION_METHODS)):
                for w in range(len(self.PARENT_METHODS)):
                    for x in range(len(self.RECOMBINATION_METHODS)):
                        for y in range(len(self.MUTATION_METHODS)):
                            for z in range(len(self.SURVIVOR_METHODS)):
                                run_test(v, w, x, y, z)

        # Stats Output
        for v in range(len(self.POPULATION_METHODS)):
            for w in range(len(self.PARENT_METHODS)):
                for x in range(len(self.RECOMBINATION_METHODS)):
                    for y in range(len(self.MUTATION_METHODS)):
                        for z in range(len(self.SURVIVOR_METHODS)):
                            print_final(v, w, x, y, z)
