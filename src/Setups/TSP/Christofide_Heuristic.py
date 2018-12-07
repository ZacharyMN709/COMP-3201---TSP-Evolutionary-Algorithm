from random import shuffle, sample
from copy import deepcopy
from src.Other.Pickle_Helper import get_pickled_euler


class EulerTourBuilder:
    def __init__(self, dists, filenum):
        self.dists = dists
        self.filenum = filenum
        self.built = False
        self.mst = None
        self.odd = None

    def gen_mst_and_vertices(self):
        if self.built: return
        if not self.load_from_file():
            self.new_minimum_spanning_tree()
            self.find_odd_vertices()
        self.built = True

    def make_new_circuit(self):
        self.gen_mst_and_vertices()
        matched_mst = self.minimum_weight_matching()
        euler_tour = self.create_euler_tour(matched_mst)
        return self.remove_duplicates(euler_tour)

    # union by rank and path compression, used to detect cycle when forming MST
    class UnionFind:
        def __init__(self):
            self.weights = {}
            self.parents = {}

        def __getitem__(self, object):
            if object not in self.parents:
                self.parents[object] = object
                self.weights[object] = 1
                return object

            # find path of objects leading to the root
            path = [object]
            root = self.parents[object]
            while root != path[-1]:
                path.append(root)
                root = self.parents[root]

            # compress the path and return
            # flattens the structure of tree by making every node point to the root whenever Find is used on it
            for ancestor in path:
                self.parents[ancestor] = root
            return root

        def __iter__(self):
            return iter(self.parents)

        def union(self, *objects):
            roots = [self[x] for x in objects]
            heaviest = max([(self.weights[r], r) for r in roots])[1]
            for r in roots:
                if r != heaviest:
                    self.weights[heaviest] += self.weights[r]
                    self.parents[r] = heaviest

    def load_from_file(self):
        euler_dict = get_pickled_euler(self.filenum)
        if euler_dict:
            self.mst, self.odd = euler_dict['MST'], euler_dict['Odd']
            return True
        else:
            return False

    # create minimum spanning tree using UnionFind()
    def new_minimum_spanning_tree(self):
        self.mst = []
        subtrees = self.UnionFind()
        # sorts weighted edges, picks ones of lightest weight at beginning of list and adds them to tree
        for weight, pt1, pt2 in sorted((self.dists[pt1][pt2], pt1, pt2)
                                       for pt1 in range(len(self.dists))
                                        for pt2 in range(len(self.dists[pt1]))):
            if subtrees[pt1] != subtrees[pt2]:
                self.mst.append((pt1, pt2, weight))
                subtrees.union(pt1, pt2)

    def find_odd_vertices(self):
        # Count all the edges for vertexes of the MST
        edge_count = [0 for _ in range(len(self.dists))]
        for edge in self.mst:
            edge_count[edge[0]] += 1
            edge_count[edge[1]] += 1

        # Return the vertexes with an odd number of edges
        self.odd = [vertex for vertex in range(len(edge_count)) if edge_count[vertex] % 2 == 1]

    # add minimum weight matching edges to MST
    # problem in this class
    # TODO - Make non-destructive
    def minimum_weight_matching(self):
        mst = deepcopy(self.mst)
        odd_vert = deepcopy(self.odd)
        shuffle(odd_vert)

        while odd_vert:
            # take an odd vertex
            v = odd_vert.pop()
            length = float("inf")
            closest = 0
            for u in odd_vert:
                # don't match a vertex to itself, run through odd vertices until we find one closest to v
                if v != u and self.dists[v][u] < length:
                    length = self.dists[v][u]
                    closest = u

            # add matched vertices to MST
            mst.append((v, closest, length))
            # remove matched vertex from odd vertex list
            odd_vert.remove(closest)
            return mst

    # TODO - Make non-destructive
    def create_euler_tour(self, matched_mst_tree):
        # delete repeated edges in matched MST
        # TODO - Make non-destructive
        def remove_edge(matched_mst, v1, v2):
            # compare each matched edge to edge in MST, if edge already exists in MST, delete it??
            for i, item in enumerate(matched_mst):
                if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
                    del matched_mst[i]
            return matched_mst

        neighbours = [[] for _ in range(len(self.dists))]
        for edge in matched_mst_tree:
            neighbours[edge[0]].append(edge[1])  # add vertex 1 to vertex 2's list of neighbours
            neighbours[edge[1]].append(edge[0])  # add vertex 2 to vertex 1's list of neighbours

        # find euler circuit
        start_vertex = matched_mst_tree[0][0]
        EP = [neighbours[start_vertex][0]]

        while len(matched_mst_tree) > 0:
            for i, v in enumerate(EP):
                if len(neighbours[v]) > 0:
                    break

            while len(neighbours[v]) > 0:
                w = neighbours[v][0]

                remove_edge(matched_mst_tree, v, w)

                del neighbours[v][(neighbours[v].index(w))]
                del neighbours[w][(neighbours[w].index(v))]

                i += 1
                EP.insert(i, w)
                v = w
        return EP

    def remove_duplicates(self, tour):
        # delete repeated vertices in Euler cycle to create Hamiltonian cycle and find solution for TSP
        path = []
        visited = [False] * len(self.dists)
        for v in tour:
            if not visited[v]:
                path.append(v)
                visited[v] = True
        return path

    def rand_dupe_removal(self, tour):
        dupes = {i: [] for i in range(len(self.dists))}
        for i in range(len(tour)): dupes[tour[i]].append(i)
        for i in range(len(self.dists)):
            dupes = dupes[i]
            to_remove = sample(dupes, len(dupes) - 1)
            for x in to_remove:
                del tour[x]
        return tour

    def generate_pickle_object(self, unloaded=False):
        from src.Other.Pickle_Helper import pickle_euler_obj
        if unloaded:
            from src.Setups.TSP.FileLoader import LoadHelper
            data = LoadHelper(self.filenum)
            self.dists = data.data.dists
        self.gen_mst_and_vertices()
        to_save = {'MST': self.mst,
                   'Odd': self.odd}
        pickle_euler_obj(to_save, self.filenum)
