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

    fname = 'C:\\Users\\Zachary\\Documents\\GitHub\\COMP 3201 - TSP Evolutionary Algorithm\\src\\Setups\\TSP\\TSP_Inputs\\' + fname
    with open(fname, 'r') as f:
        # Read and parse the file
        file = csv.reader(f, delimiter=' ')
        locations = [(float(i[1]), float(i[2])) for i in file]

        # Shift the numbers, so they are smaller and centered
        max_x, max_y = max(locations, key=lambda i: i[0])[0], max(locations, key=lambda i: i[1])[1]
        min_x, min_y = min(locations, key=lambda i: i[0])[0], min(locations, key=lambda i: i[1])[1]
        shift_x, shift_y = min_x + ((max_x - min_x)/2), min_y + ((max_y - min_y)/2)
        locations = [(i[0] - shift_x, i[1] - shift_y) for i in locations]

        # Save each location relative to an index for future use.
        for i in range(len(locations)):
            LOCATIONS[i] = locations[i]

    global PIVOT
    PIVOT = len(LOCATIONS) // 3

    return len(LOCATIONS)


def random_initialization(pop_size, genome_length):
    return [sample([c for c in range(genome_length)], genome_length) for _ in range(pop_size)]
# endregion


# region Fitness
def euclidean_distance(individual):
    return sum([calc_distance(individual[i-1], individual[i]) for i in range(len(individual))])


@euclid_memoize
def calc_distance(loc1, loc2):
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


if __name__ == '__main__':
    read_TSP_file(1)
