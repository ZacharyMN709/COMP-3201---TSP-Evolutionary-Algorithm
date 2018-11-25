import time
from src.Other.Helper_Strings import timed_funcs


def gte(new, old):
    return new >= old


def lte(new, old):
    return new <= old


def gt(new, old):
    return new > old


def lt(new, old):
    return new < old


class EARunner:

    def __init__(self, PSM, RM, MM, SSM, DEF, PMM):
        self.PSM = PSM
        self.RM = RM
        self.MM = MM
        self.SSM = SSM
        self.DEF = DEF
        self.PMM = PMM
        self.op = max if self.DEF.MAX else min
        self.as_good_as = gte if self.DEF.MAX else lte
        self.better_than = gt if self.DEF.MAX else lt
        self.runnable = False

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
        self.EAVars = None

    def set_params(self, genome_len, fit_eval, pop_init, psm, rm, mm, ssm, pmm):
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

        self.EAVars = EADefaultVars(genome_len)

        self.runnable = genome_len and fit_eval and pop_init and psm and rm and mm and ssm

    def run(self, generation_limit, known_optimum=None, true_opt=False, print_gens=0, print_final=True):
        if not self.runnable:
            print("Error! Missing information to run EA. Please check the code for errors.")
            return

        master_start_time = time.time()
        ea_vars = self.EAVars

        self.PSM.set_tournament_size(ea_vars.tournament_size)
        self.RM.set_crossover_points(ea_vars.cp_1, ea_vars.cp_2, ea_vars.cp_3)
        self.RM.set_crossover_rate(ea_vars.crossover_rate)
        self.MM.set_mutation_rate(ea_vars.mutation_rate)
        self.PMM.set_start_temp(ea_vars.start_temp)
        self.PMM.set_distances(self.DEF.MEMOIZED)
        self.PMM.set_cooling_rate(ea_vars.cooling_rate)
        self.PMM.set_population_threshold(ea_vars.population_threshold)
        best_indivs = [None] * generation_limit

        PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime = 0, 0, 0, 0, 0, 0

        # Initialize Population
        start_time = time.time()
        population, fitness = self.initialize(ea_vars.population_size, self.genome_length)
        PITime += time.time() - start_time

        for generation in range(1, generation_limit + 1):

            # Generation Info
            if print_gens != 0 and generation % print_gens == 0:
                print("Generation: {}\n  Best fitness: {}\n  Avg. fitness: {}".format(
                    generation, self.op(fitness), sum(fitness) / ea_vars.population_size)
                )

            start_time = time.time()
            parents_index = self.parent_selection(fitness, ea_vars.mating_pool_size)
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
            op_fit = self.op(fitness)
            optimal_solutions = [i for i in range(ea_vars.population_size) if fitness[i] == op_fit]
            best_indivs[generation-1] = (op_fit, population[optimal_solutions[0]][:])
            if true_opt and self.as_good_as(op_fit, known_optimum) and (len(optimal_solutions) == ea_vars.population_size):
                print("Ending early. Converged at generation: {}/{}".format(generation, generation_limit))
                break

        # Final Fitness Info
        master_time = time.time() - master_start_time
        op_fit = self.op(fitness)
        best_indivs = best_indivs[:generation-1]
        optimal_solutions = [i for i in range(ea_vars.population_size) if fitness[i] == op_fit]
        total_time = sum([PSMTime, RMTime, MMTime, SSMTime, PMMTime])
        time_tuple = (PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time)

        if print_final:
            print("Best solution fitness:", op_fit)
            if true_opt: print(
                "Best solution {:4.2f}% larger than true optimum.".format(100 * ((op_fit / known_optimum) - 1)))
            print("Number of optimal solutions: ", len(optimal_solutions), '/', ea_vars.population_size)
            print("Best solution indexes:", optimal_solutions)
            if known_optimum and self.better_than(op_fit, known_optimum):
                print('!!!! - - - NEW BEST: {} - - - !!!!'.format(op_fit))
            print("Best solution path:", population[optimal_solutions[0]])
            print(timed_funcs.format(PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time))
            print("--- {} seconds ---".format(master_time))

        return op_fit, optimal_solutions, generation, best_indivs, time_tuple


class EADefaultVars:
    def __init__(self, genome_length):

        self.genome_length = genome_length
        self.population_size = 60
        self.mating_pool_size = 0
        self.tournament_size = 0
        self.mutation_rate = 0.20
        self.crossover_rate = 0.90
        self.start_temp = 10000
        self.cooling_rate = 0.995
        self.population_threshold = 0
        self.cp_1 = 1 * self.genome_length // 4
        self.cp_2 = 2 * self.genome_length // 4
        self.cp_3 = 3 * self.genome_length // 4

        self.set_safe_matingpool(self.population_size)
        self.set_tourney_size_by_percent(0.1)
        self.set_population_threshold_by_percent(0.05)

    def set_safe_matingpool(self, size):
        if (size // 2) % 2 == 0:
            self.mating_pool_size = size // 2
        else:
            self.mating_pool_size = (size // 2) + 1

    def set_tourney_size_by_int(self, num):
        self.tournament_size = num

    def set_tourney_size_by_percent(self, per):
        self.tournament_size = int(self.population_size * per)

    def set_population_threshold_by_int(self, num):
        self.population_threshold = num

    def set_population_threshold_by_percent(self, per):
        self.population_threshold = int(self.population_size * per)

    def set_cooling_rate(self, per):
        if per >= 1 and per > 0:
            print('Cooling rate must be between 0 and 1! Defaulting tp 0.995')
            self.cooling_rate = 0.995
        else:
            self.cooling_rate = per

    def set_mutation_rate(self, per):
        if per >= 1 and per > 0:
            print('Mutation rate must be between 0 and 1! Defaulting tp 0.995')
            self.mutation_rate = 0.2
        else:
            self.mutation_rate = per

    def set_crossover_rate(self, per):
        if per >= 1 and per > 0:
            print('Crossover rate must be between 0 and 1! Defaulting tp 0.995')
            self.crossover_rate = 0.995
        else:
            self.crossover_rate = per
