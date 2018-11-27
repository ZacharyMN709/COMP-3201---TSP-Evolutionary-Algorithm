from random import shuffle, sample

LOCATIONS = list()
DISTANCES = dict()
CLSUTERS = list()


def get_map_range():
    max_lat = max(LOCATIONS, key=lambda x: x[0])[0]
    max_lon = max(LOCATIONS, key=lambda x: x[1])[1]
    min_lat = min(LOCATIONS, key=lambda x: x[0])[0]
    min_lon = min(LOCATIONS, key=lambda x: x[1])[1]
    return (max_lat - min_lat), (max_lon - min_lon)


def cities_in_radius(city, radius, cities):
    x, y = [(c[1]-city[1])**2 for c in cities], [(c[0]-city[0])**2 for c in cities]
    indexes = {i for i in range(len(cities)) if (x[i] + y[i])**0.5 <= radius}
    return indexes


def create_clusters(cities, city_indexes, dist_mod, mod_mod):
    height, width = get_map_range()
    if height > width: dist = height * dist_mod * mod_mod
    else: dist = width * dist_mod * mod_mod
    city_clusters = []

    cities_left = set(city_indexes)
    while len(cities_left) != 0:
        city = sample(cities_left, 1)[0]
        cluster = (cities_left & cities_in_radius(LOCATIONS[city], dist, cities)) | {city}
        cities_left = cities_left - cluster
        city_clusters.append(list(cluster))

    return city_clusters


def generate_nested_clusters(locations, dist_mod):
    global CLUSTERS
    CLUSTERS = create_clusters(locations, [x for x in range(len(locations))], dist_mod, 1)
    for i in range(len(CLUSTERS)):
        CLUSTERS[i] = create_clusters([locations[x] for x in CLUSTERS[i]], CLUSTERS[i], dist_mod, 0.5)


def parse_cluster(genome_length):
    shuffle(CLUSTERS)
    indiv = []
    for x in CLUSTERS:
        shuffle(x)
        for y in x:
            shuffle(y)
            indiv += y
    return indiv
