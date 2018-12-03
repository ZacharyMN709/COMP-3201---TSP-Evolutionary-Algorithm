def gte(x, y):
    return x >= y


def lte(x, y):
    return x <= y


def gt(x, y):
    return x > y


def lt(x, y):
    return x < y


class EAVarHelper:
    def __init__(self, genome_length, maximise):
        self.best_of = max if maximise else min
        self.worst_of = min if maximise else max
        self.as_good_as = gte if maximise else lte
        self.better_than = gt if maximise else lt

        self.genome_length = genome_length
        self.eval_fitness = None
        self.dist_mod = 0.1
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
        self.eng_swap_dist = max(10, genome_length // 25)

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

    def set_eval_fitness(self, func):
        self.eval_fitness = func

    def set_swap_gen_eng_dist(self, dist):
        self.eng_swap_dist = max(10, dist)
