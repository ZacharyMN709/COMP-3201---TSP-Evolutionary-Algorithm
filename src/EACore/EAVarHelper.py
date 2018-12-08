def gte(x, y):
    return x >= y


def lte(x, y):
    return x <= y


def gt(x, y):
    return x > y


def lt(x, y):
    return x < y


class EAVarHelper:
    """
    A helper class which manages the variables used for the EA. When loaded it sets all to the defaults contained in
    the class. Also helps in dynamically setting whether the problem to be solved maximizes or minimizes. The setters
    are fairly bare-bones, but can be expanded upon to ensure that particular ranges are guaranteed for each variable.
    """
    def __init__(self, genome_length, maximize):
        """
        A class which holds all the variables for the EA. Each method helper should be passed the same instance
        of this class by reference, so all variables are in sync. Also dynamically sets maximization or minimization.
        :param genome_length: The length of the individual used in the EA.
        :param maximize: True is the problem maximizes, False if it minimizes
        """
        self.maximize = maximize
        self.best_of = max if maximize else min
        self.worst_of = min if maximize else max
        self.as_good_as = gte if maximize else lte
        self.better_than = gt if maximize else lt
        self.eval_fitness = None
        self.make_new_indiv = None
        self.wrapper = None

        self.genome_length = genome_length
        self.dist_mod = 0.1
        self.population_size = 60
        self.mating_pool_size = 0
        self.tournament_size = 0
        self.mutation_rate = 0.20
        self.crossover_rate = 0.90
        self.start_temp = 10000
        self.cooling_rate = 0.995
        self.population_threshold = 0
        self.cp1 = 1 * self.genome_length // 4
        self.cp2 = 2 * self.genome_length // 4
        self.cp3 = 3 * self.genome_length // 4
        self.eng_swap_dist = max(10, genome_length // 25)

        self.set_safe_matingpool(self.population_size)
        self.set_tourney_size_by_percent(0.1)
        self.set_population_threshold_by_percent(0.05)

    def set_eval_fitness(self, func):
        self.eval_fitness = func

    def set_new_indiv(self, func, wrapper):
        self.make_new_indiv = func
        self.wrapper = wrapper

    def make_new_individual(self):
        indiv = self.make_new_indiv()
        return self.wrapper(indiv)

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

    def set_swap_gen_eng_dist(self, dist):
        self.eng_swap_dist = max(10, dist)
