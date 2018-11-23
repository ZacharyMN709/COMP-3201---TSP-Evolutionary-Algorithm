import csv
from random import sample, shuffle
import matplotlib.pyplot as plt
import pandas as pd
import time
from array import array
from src.Setups.TSP.TSP_Inputs.Optimums import get_best_path

# region Globals and Setters
MAX = False
FILENUM = None
LOCATIONS = dict()
CITIES = None
DISTANCES = None
DATAFRAME_COLUMNS = ['Longitude (Range shifted)', 'Latitude (Range shifted)']
MEMOIZED = dict()
CLUSTERS = []
eval_fitness = None
dist_mod = 0.10


def set_fitness_function(i):
    global eval_fitness
    eval_fitness = i
# endregion


def fitness_applicator(func):
    def generate_population(pop_size, genome_length):
        population = func(pop_size, genome_length)
        global eval_fitness
        return population, [eval_fitness(i) for i in population]
    return generate_population


# region Display Methods
def start_up_display():
    # TODO - Improve Graphs
    CITIES.plot.scatter(x=DATAFRAME_COLUMNS[0], y=DATAFRAME_COLUMNS[1], c=CITIES.index.get_values(), colormap='winter')
    plt.title('City Locations (Normalized to origin of 0)')


def generation_display(population):
    # TODO - Improve Graphs
    CITIES.plot.scatter(x=DATAFRAME_COLUMNS[0], y=DATAFRAME_COLUMNS[1], c=CITIES.index.get_values(), colormap='winter')
    plt.title('City Locations (Normalized to origin of 0)')
# endregion


# region Initialization
def read_tsp_file(fnum):
    global FILENUM
    FILENUM = fnum
    if fnum == 1:
        fname = "TSP_WesternSahara_29.txt"
    elif fnum == 2:
        print('Warning! Takes approximately 1.5 seconds per decade')
        fname = "TSP_Uruguay_734.txt"
    elif fnum == 3:
        print('Warning! Takes approximately 45 seconds per decade')
        fname = "TSP_Canada_4663.txt"
    else:
        print('Warning! Invalid seletion. Defaulting to test')
        fname = "TSP_Testbed_10.txt"

    import os
    script_dir = os.path.dirname(__file__)  # absolute path for directory/folder this script is in
    abs_file_path = os.path.join(script_dir, 'TSP_Inputs', fname)

    with open(abs_file_path, 'r') as f:
        # Read and parse the file
        file = csv.reader(f, delimiter=' ')
        locations = [(float(i[1]), float(i[2])) for i in file]

        # Shift the numbers, so they are smaller and centered
        max_x, max_y = max(locations, key=lambda i: i[0])[0], max(locations, key=lambda i: i[1])[1]
        min_x, min_y = min(locations, key=lambda i: i[0])[0], min(locations, key=lambda i: i[1])[1]
        shift_x, shift_y = min_x + ((max_x - min_x)/2), min_y + ((max_y - min_y)/2)

        # NOTE: Locations are slightly odd. Original (x, y) mapped to normalized (-y, x) to produce
        # identifiable population map of Canada.
        locations = [(shift_y - i[1], i[0] - shift_x) for i in locations]

        # Save each location relative to an index for future use.
        global LOCATIONS
        LOCATIONS = {key: locations[key] for key in range(len(locations))}

    global CITIES
    # Uses indexing from 0, rather than 1, by skipping the first column in the data.
    CITIES = pd.read_csv(abs_file_path, usecols=[1, 2], header=None, delimiter=' ')
    CITIES.columns = ['Lat', 'Lon']
    CITIES.index.names = ['City']
    # Translate and invert the x values, and translate the y values
    CITIES['Lat'] = CITIES['Lat'] - (CITIES['Lat'].min() + (CITIES['Lat'].max() - CITIES['Lat'].min()) / 2)
    CITIES['Lon'] = (CITIES['Lon'].min() + (CITIES['Lon'].max() - CITIES['Lon'].min()) / 2) - CITIES['Lon']
    CITIES.columns = DATAFRAME_COLUMNS

    global DISTANCES
    Lats = CITIES[DATAFRAME_COLUMNS[0]].transpose()
    Lons = CITIES[DATAFRAME_COLUMNS[1]].transpose()
    DISTANCES = pd.DataFrame([((Lats - Lats[i])**2 + (Lons - Lons[i])**2)**0.5 for i in range(Lons.size)])

    global MEMOIZED
    MEMOIZED = {key: dict() for key in range(len(LOCATIONS))}

    return len(LOCATIONS)
# endregion


# region Population Seeding
def get_map_range():
    print("THESE ARE THE CITIES", CITIES)
    x = CITIES.max()
    y = CITIES.min()
    return (x[0] - y[0]), (x[1] - y[1])


def cities_in_radius(city, radius):
    x, y = CITIES[DATAFRAME_COLUMNS[1]], CITIES[DATAFRAME_COLUMNS[0]]
    bool_frame = (((x-CITIES.loc[city][1])**2 + (y-CITIES.loc[city][0])**2)**0.5) <= radius
    image = CITIES[bool_frame]
    image.index.names = ['City - {}'.format(city)]
    return image


def find_clusters():
    height, width = get_map_range()
    if height > width: dist = height
    else: dist = width

    cities_left = set(CITIES.index)

    city_clusters = []

    while len(cities_left) != 0:
        city = sample(cities_left, 1)[0]
        cluster = cities_left & set(cities_in_radius(city, dist*dist_mod).index)
        cities_left = cities_left - cluster
        city_clusters.append(list(cluster))

    return city_clusters


def single_random_individual(genome_length):
    return array('i', (sample([c for c in range(genome_length)], genome_length)))


def single_heuristic_individual(genome_length):
    shuffle(CLUSTERS)
    indiv = []
    for x in CLUSTERS:
        shuffle(x)
        indiv += x
    return indiv


@fitness_applicator
def random_initialization(pop_size, genome_length):
    return [single_random_individual(genome_length) for _ in range(pop_size)]


@fitness_applicator
def heurisitic_cluster_initialization(pop_size, genome_length):
    global CLUSTERS
    CLUSTERS = find_clusters()
    return [single_heuristic_individual(genome_length) for _ in range(pop_size)]


@fitness_applicator
def heurisitic_grid_initialization(pop_size, genome_length):
    global CLUSTERS
    CLUSTERS = find_clusters()
    return [single_heuristic_individual(genome_length) for _ in range(pop_size)]
# endregion


# region Fitness
def euclid_memoize(f):
    def memoize(loc1, loc2):
        if loc1 < loc2:  # Make sure loc1 is the bigger of the two. Removes memoization redundancy.
            loc1, loc2 = loc2, loc1
        if loc2 not in MEMOIZED[loc1]:
            MEMOIZED[loc1][loc2] = f(loc1, loc2)
        return MEMOIZED[loc1][loc2]
    return memoize


def euclidean_distance(individual):  # Minimization
    return sum([calc_distance(individual[i-1], individual[i]) for i in range(len(individual))])


@euclid_memoize
def calc_distance(loc1, loc2):
    x1, y1 = LOCATIONS[loc1]
    x2, y2 = LOCATIONS[loc2]
    return ((x1-x2)**2 + (y1 - y2)**2)**0.5
# endregion
