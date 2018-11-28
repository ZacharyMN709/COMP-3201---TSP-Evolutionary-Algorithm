from src.Other.Helper_Strings import funcs_used, final_output


class MergeError(Exception):
    def __init__(self, message):
        super().__init__(message)


class StatsHolder:
    def __init__(self, POPULATION_METHOD, PARENT_METHOD, SURVIVOR_METHOD, MUTATION_METHOD,
                 RECOMBINATION_METHOD, MANAGEMENT_METHOD, RUNS, op, optimum=None):

        self.POPULATION_METHOD = POPULATION_METHOD
        self.PARENT_METHOD = PARENT_METHOD
        self.SURVIVOR_METHOD = SURVIVOR_METHOD
        self.MUTATION_METHOD = MUTATION_METHOD
        self.RECOMBINATION_METHOD = RECOMBINATION_METHOD
        self.MANAGEMENT_METHOD = MANAGEMENT_METHOD
        self.RUNS = RUNS
        self.best = op
        self.true_opt = optimum

        self.best_fitnesses = [None] * self.RUNS
        self.best_individuals = [None] * self.RUNS
        self.solutions_found = [None] * self.RUNS
        self.generation_count = [None] * self.RUNS
        self.run_indivs_history = [None] * self.RUNS
        self.run_fitness_history = [None] * self.RUNS
        self.time_tuples = [None] * self.RUNS
        self.runtimes = [None] * self.RUNS

    @classmethod
    def stat_obj_from_pickle(cls, pickle_tuple):
        from Pickle_Helper import get_pickled_stats

        file_name, file_num, method_used = pickle_tuple
        stats_dict = get_pickled_stats(file_name, file_num, method_used)
        return stats_dict['Stats']

    def set_run_stats(self, i, op_fit, best_indivs, gencount, run_history, time_tuple):
        if self.RUNS < i:
            print('Index is out of bounds! Not saving data for index: {}'.format(i))
        else:
            self.best_fitnesses[i] = op_fit
            self.best_individuals[i] = best_indivs
            self.solutions_found[i] = len(best_indivs)
            self.generation_count[i] = gencount
            self.run_indivs_history[i] = [x[1] for x in run_history]
            self.run_fitness_history[i] = [x[0] for x in run_history]
            self.time_tuples[i] = time_tuple
            self.runtimes[i] = time_tuple[-1]

    def print_simple_stats(self):
        mean = sum(self.best_fitnesses) / len(self.best_fitnesses)
        best = self.best(self.best_fitnesses)
        mean_per = 100 * ((mean / self.true_opt) - 1)
        best_per = 100 * ((best / self.true_opt) - 1)
        solutions = sum(self.solutions_found)
        generations = sum(self.generation_count)
        runtime = sum(self.runtimes)

        print(final_output.format(mean, best, solutions, generations, runtime))
        if self.true_opt:
            print("  Average solution {:4.2f}% larger than true optimum.".format(mean_per))
            print("  Best solution {:4.2f}% larger than true optimum.".format(best_per))

    def funcs_used(self):
        return funcs_used.format(
            self.POPULATION_METHOD,
            self.PARENT_METHOD,
            self.SURVIVOR_METHOD,
            self.MUTATION_METHOD,
            self.RECOMBINATION_METHOD,
            self.MANAGEMENT_METHOD) + '\n'

    def __str__(self):
        stats_info = 'Total Runtime: {}\nBest Fitness Produced: {}'.format(
            sum(self.runtimes), self.best(self.best_fitnesses))
        if self.true_opt:
            best_per = 100 * ((self.best(self.best_fitnesses) / self.true_opt) - 1)
            stats_info += "\nBest solution {:4.2f}% larger than true optimum.".format(best_per)
        return self.funcs_used() + stats_info

    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        if self.best == other.best:
            if self.true_opt and other.true_opt:
                opt = self.best(self.true_opt, other.true_opt)
            elif self.true_opt:
                opt = self.true_opt
            elif other.true_opt:
                opt = other.true_opt
            else:
                opt = None
            new_obj = StatsHolder(self.POPULATION_METHOD, self.PARENT_METHOD, self.SURVIVOR_METHOD, self.MUTATION_METHOD,
                                  self.RECOMBINATION_METHOD, self.MANAGEMENT_METHOD, self.RUNS, self.best, opt)
            new_obj.RUNS                = self.RUNS                + other.RUNS
            new_obj.best_fitnesses      = self.best_fitnesses      + other.best_fitnesses
            new_obj.best_individuals    = self.best_individuals    + other.best_individuals
            new_obj.solutions_found     = self.solutions_found     + other.solutions_found
            new_obj.generation_count    = self.generation_count    + other.generation_count
            new_obj.run_indivs_history  = self.run_indivs_history  + other.run_indivs_history
            new_obj.run_fitness_history = self.run_fitness_history + other.run_fitness_history
            new_obj.time_tuples         = self.time_tuples         + other.time_tuples
            new_obj.runtimes            = self.runtimes            + other.runtimes
            return new_obj
        else:
            raise MergeError

    @staticmethod  # @staticmethod allows all StatsHolder objects to use this, irrespective of self.
    def compare(stats1, stats2):
        pass

    def average_generation_fitness(self):
        out = [0] * max(self.generation_count)
        for x in range(len(out)):
            temp = [self.run_fitness_history[i][x] for i in range(self.RUNS) if x < len(self.run_fitness_history[i])]
            try:
                out[x] = sum(temp) / len(temp)
            except ZeroDivisionError:
                out = out[0:x]
                break
        return out

    def best_generation_fitness(self):
        out = [0] * max(self.generation_count)
        for x in range(len(out)):
            temp = [self.run_fitness_history[i][x] for i in range(self.RUNS) if x < len(self.run_fitness_history[i])]
            try:
                out[x] = self.best(temp)
            except ZeroDivisionError:
                out = out[0:x]
                break
        return out


if __name__ == '__main__':
    p = [('21021{} G10000.txt'.format(x), 1, 0) for x in range(5)]
    s = StatsHolder.stat_obj_from_pickle(p[0])
    s.average_generation_fitness()
    pass
