from src.Other.Helper_Strings import funcs_used, final_output


class MergeError(Exception):
    """
    A specific error thrown by the StatsHolder when two datasets are incompatible.
    """
    def __init__(self, message):
        super().__init__(message)


class StatsHolder:
    """

    """
    def __init__(self, POPULATION_METHOD, PARENT_METHOD, SURVIVOR_METHOD, MUTATION_METHOD,
                 RECOMBINATION_METHOD, MANAGEMENT_METHOD, RUNS, best_of, optimum=None):
        """

        :param POPULATION_METHOD:
        :param PARENT_METHOD:
        :param SURVIVOR_METHOD:
        :param MUTATION_METHOD:
        :param RECOMBINATION_METHOD:
        :param MANAGEMENT_METHOD:
        :param RUNS:
        :param best_of:
        :param optimum:
        """
        self.POPULATION_METHOD = POPULATION_METHOD
        self.PARENT_METHOD = PARENT_METHOD
        self.SURVIVOR_METHOD = SURVIVOR_METHOD
        self.MUTATION_METHOD = MUTATION_METHOD
        self.RECOMBINATION_METHOD = RECOMBINATION_METHOD
        self.MANAGEMENT_METHOD = MANAGEMENT_METHOD
        self.RUNS = RUNS
        self.best_of = best_of
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
        from src.Other.Pickle_Helper import get_pickled_stats

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
        best = self.best_of(self.best_fitnesses)
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
            sum(self.runtimes), self.best_of(self.best_fitnesses))
        if self.true_opt:
            best_per = 100 * ((self.best_of(self.best_fitnesses) / self.true_opt) - 1)
            stats_info += "\nBest solution {:4.2f}% larger than true optimum.".format(best_per)
        return self.funcs_used() + stats_info

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if self.best_of == other.best:
            if self.true_opt and other.true_opt:
                opt = self.best_of(self.true_opt, other.true_opt)
            elif self.true_opt:
                opt = self.true_opt
            elif other.true_opt:
                opt = other.true_opt
            else:
                opt = None
            new_obj = StatsHolder(self.POPULATION_METHOD, self.PARENT_METHOD, self.SURVIVOR_METHOD,
                                  self.MUTATION_METHOD, self.RECOMBINATION_METHOD, self.MANAGEMENT_METHOD,
                                  self.RUNS, self.best_of, opt)
            new_obj.RUNS = self.RUNS + other.RUNS
            new_obj.best_fitnesses = self.best_fitnesses + other.best_fitnesses
            new_obj.best_individuals = self.best_individuals + other.best_individuals
            new_obj.solutions_found = self.solutions_found + other.solutions_found
            new_obj.generation_count = self.generation_count + other.generation_count
            new_obj.run_indivs_history = self.run_indivs_history + other.run_indivs_history
            new_obj.run_fitness_history = self.run_fitness_history + other.run_fitness_history
            new_obj.time_tuples = self.time_tuples + other.time_tuples
            new_obj.runtimes = self.runtimes + other.runtimes
            return new_obj
        else:
            raise MergeError

    def average_generation_fitness(self):
        out = [0] * max(self.generation_count)
        for x in range(len(out)):
            temp = [self.run_fitness_history[i][x] if x < len(self.run_fitness_history[i]) else self.true_opt
                    for i in range(self.RUNS)]
            try:
                out[x] = sum(temp) / len(temp)
            except ZeroDivisionError:
                out = out[0:x]
                break
        return out

    def best_generation_fitness(self):
        out = [0] * max(self.generation_count)
        for x in range(len(out)):
            temp = [self.run_fitness_history[i][x]  if x < len(self.run_fitness_history[i]) else self.true_opt
                    for i in range(self.RUNS)]
            try:
                out[x] = self.best_of(temp)
            except ValueError:
                out = out[0:x]
                break
        return out


    def mean(self):
        return sum(self.best_fitnesses) / len(self.best_fitnesses)

    def std(self):
        return (sum([(fit - self.mean()) ** 2 for fit in self.best_fitnesses]) / len(self.best_fitnesses)) ** 0.5

    def ci95(self):
        rng = 1.960 * self.std() / (len(self.best_fitnesses) ** 0.5)
        return self.mean() - rng, self.mean() + rng

    def sr(self):
        return sum([fit < (self.true_opt * 1.1) for fit in self.best_fitnesses]) / len(self.best_fitnesses)

    @staticmethod
    def stat_cols():
        return [
            'Population initialization:    ',
            'Parent selection:             ',
            'Survivor selection:           ',
            'Mutation Method:              ',
            'Recombination Method:         ',
            'Management Method:            ',
            'Runs:                         ',
            'Lower 95%CI:                  ',
            'Mean:                         ',
            'Upper 95%CI:                  ',
            'STD:                          ',
            'SRs:                          '
        ]

    def stat_items(self):
        ci = self.ci95()
        return ['{:<20}'.format(s) for s in [
            self.POPULATION_METHOD,
            self.PARENT_METHOD,
            self.SURVIVOR_METHOD,
            self.MUTATION_METHOD,
            self.RECOMBINATION_METHOD,
            self.MANAGEMENT_METHOD,
            '{}'.format(self.RUNS),
            '{:4.2f} km'.format(ci[0]),
            '{:4.2f} km'.format(self.mean()),
            '{:4.2f} km'.format(ci[1]),
            '{:4.2f} km'.format(self.std()),
            '{:4.2f}%'.format(round(self.sr() * 100, 2))
        ]]

    def print_stats(self):
        ci = self.ci95()
        print(self.funcs_used() +
              'Runs:                         {}\n'.format(self.RUNS) +
              'Lower 95%CI:                  {:4.2f} km\n'.format(ci[0]) +
              'Mean:                         {:4.2f} km\n'.format(self.mean()) +
              'Upper 95%CI:                  {:4.2f} km\n'.format(ci[1]) +
              'STD:                          {:4.2f} km\n'.format(self.std()) +
              'SRs:                          {:4.2f}%\n'.format(round(self.sr() * 100, 2))
              )

if __name__ == '__main__':
    p = [('21021{} G10000.txt'.format(x), 1, 0) for x in range(5)]
    s = StatsHolder.stat_obj_from_pickle(p[0])
    s.average_generation_fitness()
