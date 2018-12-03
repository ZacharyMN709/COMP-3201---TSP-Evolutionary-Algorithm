import time
from src.Other.Helper_Strings import timed_funcs
from src.Setups.TSP.PopulationInitialization import PopulationInitializationHelper
from src.Setups.TSP.FitnessEvaluator import FitnessHelper
from src.EA_Methods.ParentSelectionMethods import ParentSelectionHelper
from src.EA_Methods.RecombinationMethods import RecombinationHelper
from src.EA_Methods.MutationMethods import MutatorHelper
from src.EA_Methods.SurvivorSelectionMethods import SurvivorSelectionHelper
from src.EA_Methods.PopulationManagementMethods import PopulationManagementHelper


class EARunner:
    def __init__(self, var_helper, method, fitness_helper):
        self.vars = var_helper
        self.FEM = fitness_helper
        self.PIM = PopulationInitializationHelper(var_helper, method)
        self.PSM = ParentSelectionHelper(var_helper, method)
        self.RM = RecombinationHelper(var_helper, method)
        self.MM = MutatorHelper(var_helper, method)
        self.SSM = SurvivorSelectionHelper(var_helper, method)
        self.PMM = PopulationManagementHelper(var_helper, method)
        self.runnable = False

        self.initialize = None
        self.eval_fitness = None
        self.parent_selection = None
        self.generate_offspring = None
        self.apply_mutation = None
        self.select_survivors = None
        self.manage_population = None

    def get_method_helpers(self):
        return self.FEM, self.PIM, self.PSM, self.RM, self.MM, self.SSM, self.PMM

    def set_params(self, fit, pop, psm, rm, mm, ssm, pmm):
        self.eval_fitness = self.FEM.get_func_from_index(fit)
        self.initialize = self.PIM.get_func_from_index(pop)
        self.parent_selection = self.PSM.get_func_from_index(psm)
        self.generate_offspring = self.RM.get_func_from_index(rm)
        self.apply_mutation = self.MM.get_func_from_index(mm)
        self.select_survivors = self.SSM.get_func_from_index(ssm)
        self.manage_population = self.PMM.get_func_from_index(pmm)

    def is_runnable(self):
        return \
            self.eval_fitness is not None and \
            self.initialize is not None and \
            self.parent_selection is not None and \
            self.generate_offspring is not None and \
            self.apply_mutation is not None and \
            self.select_survivors is not None and \
            self.manage_population is not None

    def run(self, generation_limit, test_id, known_optimum=None, true_opt=False, print_gens=0, print_final=True):
        if not self.runnable:
            print("Error! Missing information to run EA. Please check the code for errors.")
            return

        print("Test: {}".format(test_id))
        self.vars.set_eval_fitness(self.eval_fitness)

        master_start_time = time.time()
        ea_vars = self.vars

        best_indivs = [None] * generation_limit

        PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime = 0, 0, 0, 0, 0, 0

        # Initialize Population
        start_time = time.time()
        population, fitness = self.initialize(ea_vars.population_size, self.vars.genome_length)
        PITime += time.time() - start_time

        for generation in range(1, generation_limit + 1):

            # Generation Info
            if print_gens != 0 and generation % print_gens == 0:
                print("Test: {}\nGeneration: {}\n  Best fitness: {}\n  Avg. fitness: {}".format(
                    test_id, generation, self.vars.best_of(fitness), sum(fitness) / ea_vars.population_size)
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
            op_fit = self.vars.best_of(fitness)
            optimal_solutions = [i for i in range(ea_vars.population_size) if fitness[i] == op_fit]
            best_indivs[generation - 1] = (op_fit, population[optimal_solutions[0]][:])
            if true_opt and self.vars.as_good_as(op_fit, known_optimum) and (
                    len(optimal_solutions) == ea_vars.population_size):
                print("Ending early. Converged at generation: {}/{}".format(generation, generation_limit))
                break

        # Final Fitness Info
        master_time = time.time() - master_start_time
        op_fit = self.vars.best_of(fitness)
        best_indivs = best_indivs[:generation - 1]
        optimal_solutions = [i for i in range(ea_vars.population_size) if fitness[i] == op_fit]
        total_time = sum([PSMTime, RMTime, MMTime, SSMTime, PMMTime])
        time_tuple = (PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time)

        if print_final:
            print("Best solution fitness:", op_fit)
            if true_opt: print(
                "Best solution {:4.2f}% larger than true optimum.".format(100 * ((op_fit / known_optimum) - 1)))
            print("Number of optimal solutions: ", len(optimal_solutions), '/', ea_vars.population_size)
            print("Best solution indexes:", optimal_solutions)
            if known_optimum and self.vars.better_than(op_fit, known_optimum):
                print('!!!! - - - NEW BEST: {} - - - !!!!'.format(op_fit))
            print("Best solution path:", population[optimal_solutions[0]])
            print(timed_funcs.format(PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time))
            print("--- {} seconds ---".format(master_time))

        return op_fit, optimal_solutions, generation, best_indivs, time_tuple
