import time
from src.EA_Shell import EARunner


output_string = "\
Population initialization:   {: <25}\
Parent selection:            {: <25}\n\
Survivor selection:          {: <25}\
Mutation Method:             {: <25}\n\
Recombination Method:        {: <25}\
Management Method:           {: <25}\
"

final_output = "\
Average fitness: {}\nBest fitness: {}\
Total 'best' individuals: {}\n\
Total generations elapsed: {} generations\n\
Total time elapsed: {} seconds\
"


class EATester(EARunner):
    def __init__(self, PSM, RM, MM, SSM, DEF, PMM):
        super().__init__(PSM, RM, MM, SSM, DEF, PMM)
        self.RUNS = None
        self.POPULATION_METHODS = None
        self.PARENT_METHODS = None
        self.RECOMBINATION_METHODS = None
        self.MUTATION_METHODS = None
        self.SURVIVOR_METHODS = None
        self.MANAGEMENT_METHODS = None
        self.testable = False

    def set_test_vars(self, runs, pop, par, rec, mut, sur, man):
        self.RUNS = runs
        self.POPULATION_METHODS = pop
        self.PARENT_METHODS = par
        self.RECOMBINATION_METHODS = rec
        self.MUTATION_METHODS = mut
        self.SURVIVOR_METHODS = sur
        self.MANAGEMENT_METHODS = man

        self.testable = pop and par and rec and mut and sur and runs and man

    def iterate_tests(self, generation_limit, known_optimum=None, true_opt=False, print_gens=False):
        if not self.testable:
            print("Error! Missing information to run tests. Please check the code for errors.")
            return

        def print_header(v, w, x, y, z, a):
            print(output_string.format(
                self.POPULATION_METHODS[v][0],
                self.PARENT_METHODS[w][0],
                self.SURVIVOR_METHODS[z][0],
                self.MUTATION_METHODS[y][0],
                self.RECOMBINATION_METHODS[x][0],
                self.MANAGEMENT_METHODS[a][0]))

        def run_test(v, w, x, y, z, a):
            start_time = time.time()
            print_header(v, w, x, y, z, a)

            self.set_funcs(self.genome_length, self.eval_fitness,
                           self.POPULATION_METHODS[v][1], self.PARENT_METHODS[w][1], self.RECOMBINATION_METHODS[x][1],
                           self.MUTATION_METHODS[y][1], self.SURVIVOR_METHODS[z][1], self.MANAGEMENT_METHODS[a][1])
            op_fit, optimal_solutions, generation = self.run_ea_algorithm(generation_limit, known_optimum, true_opt, print_gens)

            runtime = time.time() - start_time
            print("--- %s seconds ---" % runtime)
            best_fitnesses[v][w][x][y][z][a].append(op_fit)
            solutions_found[v][w][x][y][z][a].append(len(optimal_solutions))
            final_generations[v][w][x][y][z][a].append(generation)
            times_elapsed[v][w][x][y][z][a].append(runtime)
            print("\n -------- \n")

        def print_final(v, w, x, y, z, a):
            print("Number of iterations used: {}".format(self.RUNS))
            print_header(v, w, x, y, z, a)

            mean = sum(best_fitnesses[v][w][x][y][z][a]) / len(best_fitnesses[v][w][x][y][z][a])
            best = self.op(best_fitnesses[v][w][x][y][z][a])
            mean_per = 100 * ((mean / known_optimum) - 1)
            best_per = 100 * ((best / known_optimum) - 1)
            solutions = sum(solutions_found[v][w][x][y][z][a])
            generations = sum(final_generations[v][w][x][y][z][a])
            runtime = sum(times_elapsed[v][w][x][y][z][a])

            print(final_output.format(mean, best, solutions, generations, runtime))
            if true_opt:
                print("Average solution {:4.2f}% larger than true optimum.".format(mean_per))
                print("Best solution {:4.2f}% larger than true optimum.".format(best_per))
            print("\n -------- \n")

        # Stats Set-up
        import copy

        matrix = [[[[[[[]  # Make a matrix of empty lists.
                      # matrix[v][w][x][y][z][a] returns a list corresponding to the functions used
                       for a in range(len(self.MANAGEMENT_METHODS))]
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
                                for a in range(len(self.MANAGEMENT_METHODS)):
                                    run_test(v, w, x, y, z, a)

        # Stats Output
        for v in range(len(self.POPULATION_METHODS)):
            for w in range(len(self.PARENT_METHODS)):
                for x in range(len(self.RECOMBINATION_METHODS)):
                    for y in range(len(self.MUTATION_METHODS)):
                        for z in range(len(self.SURVIVOR_METHODS)):
                            for a in range(len(self.MANAGEMENT_METHODS)):
                                print_final(v, w, x, y, z, a)
