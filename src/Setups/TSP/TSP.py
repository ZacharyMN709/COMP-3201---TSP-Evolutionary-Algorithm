import csv
from random import sample

LOCATIONS = dict()
PIVOT = 0


def euclid_memoize(f):
    distances = dict()

    def memoize(loc1, loc2):
        if loc1 > loc2:
            loc1, loc2 = loc2, loc1
        key = "{}.{}".format(loc1, loc2)
        if key not in distances:
            distances[key] = f(loc1, loc2)
        return distances[key]
    return memoize


# region Initialization
def read_TSP_file(fnum):
    if fnum == 1:
        fname = "TSP_WesternSahara_29.txt"
    elif fnum == 2:
        fname = "TSP_Uruguay_734.txt"
    elif fnum == 3:
        fname = "TSP_Canada_4663.txt"
    else:
        fname = "TSP_WesternSahara_29.txt"
    fname = "\\src\\Setups\\TSP\\TSP_Inputs\\" + fname

    max_x, max_y = 0, 0
    min_x, min_y = 0, 0

    shift_x, shift_y = max_x - min_x, max_y - min_y
    # TODO - Populate LOCATIONS from file.


def random_initialization(pop_size, chrom_length, fnum=1):
    read_TSP_file(fnum)
    global PIVOT
    PIVOT = len(LOCATIONS) // 3
    return [sample([c for c in range(chrom_length)], chrom_length) for _ in range(pop_size)]
# endregion


# region Fitness
@euclid_memoize
def euclid_distance(loc1, loc2):
    x1, y1 = LOCATIONS[loc1]
    x2, y2 = LOCATIONS[loc2]
    return ((x1-x2)**2 + (y1 - y2)**2)**0.5
# endregion


# region Recombination
def permutation_cut_and_crossfill(parent1, parent2):
    offspring1 = parent1[:PIVOT] + [x for x in parent2[PIVOT:] + parent2[:PIVOT] if x not in parent1[:PIVOT]]
    offspring2 = parent2[:PIVOT] + [x for x in parent1[PIVOT:] + parent1[:PIVOT] if x not in parent2[:PIVOT]]
    return offspring1, offspring2
# endregion
