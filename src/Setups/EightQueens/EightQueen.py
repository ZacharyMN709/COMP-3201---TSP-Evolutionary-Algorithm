from random import sample


# initialize a population of permutation
def random_initialization(pop_size, chrom_length):
    return [sample([c for c in range(chrom_length)], chrom_length) for _ in range(pop_size)]


# compute fitness of an individual for the 8-queen puzzle
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


def permutation_cut_and_crossfill(parent1, parent2):
    PIVOT = 3
    offspring1 = parent1[:PIVOT] + [x for x in parent2[PIVOT:] + parent2[:PIVOT] if x not in parent1[:PIVOT]]
    offspring2 = parent2[:PIVOT] + [x for x in parent1[PIVOT:] + parent1[:PIVOT] if x not in parent2[:PIVOT]]
    return offspring1, offspring2

