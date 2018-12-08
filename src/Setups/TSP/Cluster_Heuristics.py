from random import sample, shuffle


class ClusterBuilder:
    def __init__(self, locs, dists):
        self.locs = locs
        self.dists = dists
        self.map_range = self.get_map_range()

    def get_map_range(self):
        max_lat = max(self.locs, key=lambda x: x[0])[0]
        max_lon = max(self.locs, key=lambda x: x[1])[1]
        min_lat = min(self.locs, key=lambda x: x[0])[0]
        min_lon = min(self.locs, key=lambda x: x[1])[1]
        return (max_lat - min_lat), (max_lon - min_lon)

    def cities_in_radius(self, city, radius, cities):
        x, y = [(c[1]-self.locs[city][1])**2 for c in cities], [(c[0]-self.locs[city][0])**2 for c in cities]
        return {i for i in range(len(cities)) if (x[i] + y[i])**0.5 <= radius}

    def create_clusters(self, cities, city_indexes, dist_mod, mod_mod):
        height, width = self.map_range
        if height > width: dist = height * dist_mod * mod_mod
        else: dist = width * dist_mod * mod_mod
        city_clusters = []

        cities_left = set(city_indexes)
        while len(cities_left) != 0:
            city = sample(cities_left, 1)[0]
            cluster = (cities_left & self.cities_in_radius(city, dist, cities)) | {city}
            cities_left = cities_left - cluster
            city_clusters.append(list(cluster))

        return city_clusters

    def generate_nested_clusters(self, dist_mod):
        clusters = self.create_clusters(self.locs, [x for x in range(len(self.locs))], dist_mod, 1)
        for i in range(len(clusters)):
            clusters[i] = self.create_clusters([self.locs[x] for x in clusters[i]], clusters[i], dist_mod, 0.5)
        return clusters