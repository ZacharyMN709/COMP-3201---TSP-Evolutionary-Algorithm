from random import sample


# region Globals and Setters
MAX = True
eval_fitness = None


def set_fitness_function(i):
    global eval_fitness
    eval_fitness = i
# endregion


# region Display Methods
def start_up_display():
    pass


def generation_display(population):
    pass
# endregion


# region Initialization
def fitness_applicator(func):
    def generate_population(pop_size, genome_length):
        population = func(pop_size, genome_length)
        global eval_fitness
        return population, [eval_fitness(i) for i in population]
    return generate_population


@fitness_applicator
def random_initialization(pop_size, chrom_length):
    return [sample([c for c in range(chrom_length)], chrom_length) for _ in range(pop_size)]
# endregion


# region Fitness
def fitness_8queen_old(individual):  # maximization
    M = 28

    neg_diag = dict()
    pos_diag = dict()
    m = len(individual)

    def inc(dic, key):
        if key in dic:
            dic[key] += 1
        else:
            dic[key] = 0

    def clashes(dic):
        return int(sum([(((1 + dic[x]) * dic[x]) / 2) for x in dic if dic[x] != 0]))

    for i in range(m):
        inc(neg_diag, (i - individual[i]))
        inc(pos_diag, (i + individual[i]))

    return M - (clashes(neg_diag) + clashes(pos_diag))


def fitness_8queen(individual):  # maximization
    m = len(individual)
    neg_diag = set([i - individual[i] for i in range(m)])
    pos_diag = set([i + individual[i] for i in range(m)])

    return len(neg_diag) + len(pos_diag)
# endregion
