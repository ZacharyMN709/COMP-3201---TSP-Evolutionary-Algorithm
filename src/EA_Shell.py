import time


def gte(x, y):
    return x >= y


def lte(x, y):
    return x <= y


def gt(x, y):
    return x > y


def lt(x, y):
    return x < y


time_string = "\
PSMTime = {:4.2f},\
RMTime = {:4.2f},\
MMTime = {:4.2f},\
SSMTime = {:4.2f},\
PMMTime = {:4.2f}\n\
Total time: {:4.2f}\
"


class EARunner:

    def __init__(self, PSM, RM, MM, SSM, DEF, PMM):
        self.PSM = PSM
        self.RM = RM
        self.MM = MM
        self.SSM = SSM
        self.DEF = DEF
        self.PMM = PMM
        self.op = max if self.DEF.MAX else min
        self.cmp_eq = gte if self.DEF.MAX else lte
        self.cmp_ne = gt if self.DEF.MAX else lt
        self.runnable = False
        self.testable = False

        self.PSM.set_op(self.op)
        self.SSM.set_op(self.op)
        self.PMM.set_op(self.op)

        self.genome_length = None
        self.initialize = None
        self.eval_fitness = None
        self.parent_selection = None
        self.generate_offspring = None
        self.apply_mutation = None
        self.select_survivors = None
        self.manage_population = None

    def set_funcs(self, genome_len, fit_eval, pop_init, psm, rm, mm, ssm, pmm):
        self.genome_length = genome_len
        self.eval_fitness = fit_eval
        self.initialize = pop_init
        self.parent_selection = psm
        self.generate_offspring = rm
        self.apply_mutation = mm
        self.select_survivors = ssm
        self.manage_population = pmm

        self.MM.set_fitness_function(self.eval_fitness)
        self.PMM.set_fitness_function(self.eval_fitness)
        self.DEF.set_fitness_function(self.eval_fitness)

        self.RM.set_genome_length(self.genome_length)
        self.MM.set_genome_length(self.genome_length)
        self.PMM.set_genome_length(self.genome_length)

        self.runnable = genome_len and fit_eval and pop_init and psm and rm and mm and ssm

    def run_ea_algorithm(self, generation_limit, known_optimum=None, true_opt=False, print_gens=0):
        if not self.runnable:
            print("Error! Missing information to run EA. Please check the code for errors.")
            return

        population_size = 60
        mating_pool_size = population_size//2 if (population_size//2) % 2 == 0 else (population_size//2)+1  # has to be even
        tournament_size = population_size//10
        mutation_rate = 0.2
        crossover_rate = 0.9
        start_temp = 10000
        cooling_rate = 0.995
        population_threshold = 0.35 * population_size
        cp_1, cp_2, cp_3 = self.genome_length//4, 2*self.genome_length//4, 3*self.genome_length//4

        self.PSM.set_tournament_size(tournament_size)
        self.RM.set_crossover_points(cp_1, cp_2, cp_3)
        self.RM.set_crossover_rate(crossover_rate)
        self.MM.set_mutation_rate(mutation_rate)
        self.PMM.set_start_temp(start_temp)
        self.PMM.set_cooling_rate(cooling_rate)
        self.PMM.set_population_threshold(population_threshold)

        # TODO - Figure out how to set population method
        # Maybe split the EA into different run different implementations
        # self.PMM.set_population_method(i)

        PSMTime, RMTime, MMTime, SSMTime, PMMTime = 0, 0, 0, 0, 0

        # Initialize Population
        population, fitness = self.initialize(population_size, self.genome_length)

        for generation in range(1, generation_limit + 1):

            # Generation Info
            if print_gens != 0 and generation % print_gens == 0:
                print("Generation: {}\n  Best fitness: {}\n  Avg. fitness: {}".format(
                    generation, self.op(fitness), sum(fitness)/len(fitness))
                )

            start_time = time.time()
            parents_index = self.parent_selection(fitness, mating_pool_size)
            PSMTime += time.time() - start_time

            start_time = time.time()
            offspring = self.generate_offspring(population, parents_index)
            RMTime += time.time() - start_time

            start_time = time.time()
            offspring, offspring_fitness = self.apply_mutation(offspring)
            MMTime += time.time() - start_time

            start_time = time.time()
            population, fitness = self.select_survivors(population, fitness, offspring, offspring_fitness)
            SSMTime += time.time() - start_time

            start_time = time.time()
            population, fitness = self.manage_population(population, fitness)
            PMMTime += time.time() - start_time

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
        total_time = sum([PSMTime, RMTime, MMTime, SSMTime, PMMTime])

        print("Best solution fitness:", op_fit)
        if true_opt: print("Best solution {:4.2f}% larger than true optimum.".format(100*((op_fit/known_optimum)-1)))
        print("Number of optimal solutions: ", len(optimal_solutions), '/', population_size)
        print("Best solution indexes:", optimal_solutions)
        if self.cmp_ne(op_fit, known_optimum): print('!!!! - - - NEW BEST: {} - - - !!!!'.format(op_fit))
        print("Best solution path:", population[optimal_solutions[0]])
        print(time_string.format(PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time))
        return op_fit, optimal_solutions, generation
