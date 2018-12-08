from time import perf_counter
import sqlite3 as sql
from src.Other.Helper_Strings import timed_funcs
from src.EACore.MethodClasses.ParentSelectionMethods import ParentSelectionHelper
from src.EACore.MethodClasses.RecombinationMethods import RecombinationHelper
from src.EACore.MethodClasses.MutationMethods import MutatorHelper
from src.EACore.MethodClasses.SurvivorSelectionMethods import SurvivorSelectionHelper
from src.EACore.MethodClasses.PopulationManagementMethods import PopulationManagementHelper


class EARunner:
    """
    The main body for the generalized EA. Uses the classes which act as containers for function pointer,
    and automatically handle modifying variables by using a shared object which contains those variables.
    """
    def __init__(self, var_helper, data_type, fitness_helper, population_initializer):
        self.vars = var_helper
        self.FEM = fitness_helper
        self.PIM = population_initializer
        self.PSM = ParentSelectionHelper(var_helper)
        self.RM = RecombinationHelper(var_helper, data_type)
        self.MM = MutatorHelper(var_helper)
        self.SSM = SurvivorSelectionHelper(var_helper)
        self.PMM = PopulationManagementHelper(var_helper)
        self.vars.set_new_indiv(self.PIM.single_random_individual, self.PIM.wrapper)

        self.initialize = None
        self.eval_fitness = None
        self.parent_selection = None
        self.generate_offspring = None
        self.apply_mutation = None
        self.select_survivors = None
        self.manage_population = None

    def get_method_helpers(self):
        """
        :return: Returns references to all the helper classes this EARunner is using.
        """
        return self.FEM, self.PIM, self.PSM, self.RM, self.MM, self.SSM, self.PMM

    def set_params(self, fit, pop, psm, rm, mm, ssm, pmm):
        """
        Given valid integers, sets the classes' function pointers to those of the appropriate method.
        :param fit: An integer
        :param pop: An integer
        :param psm: An integer
        :param rm: An integer
        :param mm: An integer
        :param ssm: An integer
        :param pmm: An integer
        """
        self.eval_fitness = self.FEM.get_func_from_index(fit)
        self.initialize = self.PIM.get_func_from_index(pop)
        self.parent_selection = self.PSM.get_func_from_index(psm)
        self.generate_offspring = self.RM.get_func_from_index(rm)
        self.apply_mutation = self.MM.get_func_from_index(mm)
        self.select_survivors = self.SSM.get_func_from_index(ssm)
        self.manage_population = self.PMM.get_func_from_index(pmm)

    def is_runnable(self):
        """
        :return: True if every function pointer has been correctly assigned, false otherwise.
        """
        return \
            self.eval_fitness is not None and \
            self.initialize is not None and \
            self.parent_selection is not None and \
            self.generate_offspring is not None and \
            self.apply_mutation is not None and \
            self.select_survivors is not None and \
            self.manage_population is not None

    def run(self, generation_limit, known_optimum=None, true_opt=False, report_rate=0, print_stats=False, db_name=None):
        """
        The master switch for the EA function. When called, starts running the algorithm if set-ups complete.
        :param generation_limit: The number of generations that should be run
        :param known_optimum: Default: None. If given, is the value of the best optimum known.
        :param true_opt: Default: False. If given True, signals that known_optimum is the true global optimum.
        :param report_rate: Default: 0. The frequency with which to print run stats to screen.
        :param print_stats: Default: False. Whether the program prints the final stats of the run.
        :param db_name: Default: None. If given, the database to store run statistics in.
        :return: The best fitness found, the list of individuals which represent the best solution, the terminal
        generation, and a tuple containing the runtime for each of the portions of the EA.
        """
        try:
            if not self.is_runnable:
                print("Error! Missing information to run EA. Please check the code for errors.")
                print('self.eval_fitness is not None: {}'.format(self.eval_fitness is not None))
                print('self.initialize is not None: {}'.format(self.initialize is not None))
                print('self.parent_selection is not None: {}'.format(self.parent_selection is not None))
                print('self.generate_offspring is not None: {}'.format(self.generate_offspring is not None))
                print('self.apply_mutation is not None: {}'.format(self.apply_mutation is not None))
                print('self.select_survivors is not None: {}'.format(self.select_survivors is not None))
                print('self.manage_population is not None: {}'.format(self.manage_population is not None))
                return

            # Open Database to store stats
            if db_name:
                db = sql.connect(db_name)
                db.execute("CREATE TABLE Generation_Data (generation integer, best_fitness real, avg_fitness real, best_individual text, copies_of_best integer)")
                db.execute("CREATE Table Final_Data (best_fitness real, avg_fitness real, best_individual text, copies_of_best integer, PITime real, PSMTime real, RMTime real, MMTime real, SSMTime real, PMMTime real, TotalTime real)")

            self.vars.set_eval_fitness(self.eval_fitness)

            master_start_time = perf_counter()
            ea_vars = self.vars

            PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime = 0, 0, 0, 0, 0, 0

            # Initialize Population
            start_time = perf_counter()
            population, fitness = self.initialize()
            PITime += perf_counter() - start_time

            for generation in range(1, generation_limit + 1):

                # Generation Info
                if report_rate != 0 and generation % report_rate == 0:
                    best_fitness = self.vars.best_of(fitness)
                    avg_fitness = sum(fitness)/len(fitness)
                    best_individual = str(population[fitness.index(best_fitness)])
                    copies_of_best = fitness.count(best_fitness)
                    stats = [generation, best_fitness, avg_fitness, best_individual, copies_of_best]

                    if db_name:
                        db.execute("INSERT INTO Generation_Data VALUES (?, ?, ?, ?, ?)", stats)
                        db.commit()

                    if print_stats:
                        print("Generation: {}\n  Best fitness: {}\n  Avg. fitness: {}\n  Copies of Best: {}".format(
                            generation, best_fitness, avg_fitness, copies_of_best
                        ))

                start_time = perf_counter()
                parents_index = self.parent_selection(fitness)
                PSMTime += perf_counter() - start_time

                start_time = perf_counter()
                offspring = self.generate_offspring(population, parents_index)
                RMTime += perf_counter() - start_time

                start_time = perf_counter()
                offspring, offspring_fitness = self.apply_mutation(offspring)
                MMTime += perf_counter() - start_time

                start_time = perf_counter()
                population, fitness = self.select_survivors(population, fitness, offspring, offspring_fitness)
                SSMTime += perf_counter() - start_time

                start_time = perf_counter()
                population, fitness = self.manage_population(population, fitness)
                PMMTime += perf_counter() - start_time

                # Break if converged at optimal solution
                best_fitness = self.vars.best_of(fitness)
                optimal_solutions = [i for i in range(ea_vars.population_size) if fitness[i] == best_fitness]
                if true_opt and self.vars.as_good_as(best_fitness, known_optimum) and (
                        len(optimal_solutions) == ea_vars.population_size):
                    print("Ending early. Converged at generation: {}/{}".format(generation, generation_limit))
                    break

            # Final Fitness Info
            master_time = perf_counter() - master_start_time
            best_fitness = self.vars.best_of(fitness)
            avg_fitness = sum(fitness)/len(fitness)
            optimal_solutions = [i for i in range(ea_vars.population_size) if fitness[i] == best_fitness]
            total_time = sum([PSMTime, RMTime, MMTime, SSMTime, PMMTime])
            time_tuple = (PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time)
            best_individual = population[fitness.index(best_fitness)]
            copies_of_best = fitness.count(best_fitness)

            if db_name:
                final_stats = [best_fitness, avg_fitness, str(best_individual), copies_of_best, PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, master_time]
                db.execute("INSERT INTO Final_Data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", final_stats)
                db.commit()
                db.close()

            if print_stats:
                print("Best solution fitness:", best_fitness)
                if true_opt: print(
                    "Best solution {:4.2f}% larger than true optimum.".format(100 * ((best_fitness / known_optimum) - 1)))
                print("Number of optimal solutions: ", len(optimal_solutions), '/', ea_vars.population_size)
                print("Best solution indexes:", optimal_solutions)
                if known_optimum and self.vars.better_than(best_fitness, known_optimum):
                    print('!!!! - - - NEW BEST: {} - - - !!!!'.format(best_fitness))
                print("Best solution path:", population[optimal_solutions[0]])
                print(timed_funcs.format(PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time))
                print("--- {} seconds ---".format(master_time))

            return best_fitness, optimal_solutions, generation, time_tuple
        except KeyboardInterrupt:
            # Final Fitness Info
            master_time = perf_counter() - master_start_time
            best_fitness = self.vars.best_of(fitness)
            avg_fitness = sum(fitness)/len(fitness)
            optimal_solutions = [i for i in range(ea_vars.population_size) if fitness[i] == best_fitness]
            total_time = sum([PSMTime, RMTime, MMTime, SSMTime, PMMTime])
            time_tuple = (PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time)
            best_individual = population[fitness.index(best_fitness)]
            copies_of_best = fitness.count(best_fitness)

            if db_name:
                final_stats = [best_fitness, avg_fitness, str(best_individual), copies_of_best, PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, master_time]
                db.execute("INSERT INTO Final_Data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", final_stats)
                db.commit()
                db.close()

            if print_stats:
                print("Best solution fitness:", best_fitness)
                if true_opt: print(
                    "Best solution {:4.2f}% larger than true optimum.".format(100 * ((best_fitness / known_optimum) - 1)))
                print("Number of optimal solutions: ", len(optimal_solutions), '/', ea_vars.population_size)
                print("Best solution indexes:", optimal_solutions)
                if known_optimum and self.vars.better_than(best_fitness, known_optimum):
                    print('!!!! - - - NEW BEST: {} - - - !!!!'.format(best_fitness))
                print("Best solution path:", population[optimal_solutions[0]])
                print(timed_funcs.format(PITime, PSMTime, RMTime, MMTime, SSMTime, PMMTime, total_time, master_time))
                print("--- {} seconds ---".format(master_time))

            return best_fitness, optimal_solutions, generation, time_tuple
