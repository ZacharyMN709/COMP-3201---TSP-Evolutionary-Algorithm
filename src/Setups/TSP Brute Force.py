import math
import time
import random

#read in data from text file
def create_data():
    f = open("TSP_WesternSahara_29.txt", "r")
    data = []
    f1 = f.readlines()
    for l in f1:
        row = l.split()
        data.append([float(row[1]), float(row[2])]) #reads in every city as pair of coordinates    
    f.close()
    return data

#find distance between two cities    
def get_length(x1, y1, x2, y2):
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist

#calculate distances between all cities, build graph
def build_graph(data):
    graph = {}
    for pt in range(len(data)):
        graph[pt] = {}
        for next_pt in range(len(data)):
            #don't calculate distance between a city and itself, don't calculate distance between two cities if that distance already calculated
            if (pt != next_pt) and (next_pt not in graph): 
                graph[pt][next_pt] = get_length(data[pt][0], data[pt][1], data[next_pt][0], data[next_pt][1]) #2d dict

    for x in graph: #fix diagonal
        for y in range(len(data)-1, x, -1):
            graph[y][x] = graph[x][y]
    return graph

#union by rank and path compression, used to detect cycle when forming MST
class UnionFind():
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

        #compress the path and return
        #flattens the structure of tree by making every node point to the root whenever Find is used on it
        for ancestor in path:
            self.parents[ancestor] = root
        return root
    
    def __iter__(self):
        return iter(self.parents)
    
    def union(self, *objects): #* allows you to call function with arbitrary number of arguments
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest
                
#create minimum spanning tree using UnionFind()
def minimum_spanning_tree(graph):
    tree = []
    subtrees = UnionFind()
    #sorts weighted edges, picks ones of lightest weight at beginning of list and adds them to tree
    for weight, pt1, pt2 in sorted((graph[pt1][pt2], pt1, pt2) for pt1 in graph for pt2 in graph[pt1]):
        if subtrees[pt1] != subtrees[pt2]:
            tree.append((pt1, pt2, weight))
            subtrees.union(pt1, pt2)
    return tree

#find odd vertexes in MST to match
def find_odd_vertexes(MST):
    temp= {}
    vertexes = []
    for edge in MST:
        #if first vertex not in temp, add it in, and set edges connected to it to 0
        if edge[0] not in temp:
            temp[edge[0]] = 0

        #if second vertex not in temp, add it in, and set edges connected to it to 0
        if edge[1] not in temp:
            temp[edge[1]] = 0

        #if vertex already in temp or two vertices are connected by an edge, update their edge count by 1
        temp[edge[0]] += 1
        temp[edge[1]] += 1

    #once all vertices and their edge counts are in temp, calculate if they're odd
    for vertex in temp:
        if temp[vertex] % 2 == 1:
            vertexes.append(vertex)
    return vertexes

#add minimum weight matching edges to MST
#problem in this class
def minimum_weight_matching(MST, G, odd_vert):
    random.shuffle(odd_vert)

    while odd_vert:
        #take an odd vertex
        v = odd_vert.pop()
        length = float("inf") #initialize length variable
        closest = 0 #initialize closest vertex variable
        for u in odd_vert:
            #don't match a vertex to itself, run through odd vertices until we find one closest to v
            if v != u and G[v][u] < length:
                length = G[v][u]
                closest = u
                
        #add matched vertices to MST
        MST.append((v, closest, length))
        #remove matched vertex from odd vertex list
        odd_vert.remove(closest)

#delete repeated edges in matched MST
def remove_edge(matchedMST, v1, v2):
    for i, item in enumerate(matchedMST):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del matchedMST[i]
    return matchedMST

#find euler tour
def euler_tour(matchedMSTree, G):
    #find neighbours
    neighbours = {}
    for edge in matchedMSTree:
        #if vertex 1 of edge not in neighbours, add it
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []

        #if vertex 2 of edge not in neighbours, add it
        if edge[1] not in neighbours:
            neighbours[edge[1]] = []

        neighbours[edge[0]].append(edge[1]) #add vertex 1 to vertex 2's list of neighbours
        neighbours[edge[1]].append(edge[0]) #add vertex 2 to vertex 1's list of neighbours

    #find euler circuit
    start_vertex = matchedMSTree[0][0]
    EP = [neighbours[start_vertex][0]]

    while len(matchedMSTree) > 0:
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break

        while len(neighbours[v]) > 0:
            w = neighbours[v][0]

            remove_edge(matchedMSTree, v, w)

            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]

            i += 1
            EP.insert(i, w)
            v = w
    return EP
    
def tsp():
    start_time = time.time()
    tour = create_data()
    T = build_graph(tour)
    print("Graph: ", T)
    MSTree = minimum_spanning_tree(T)
    print("MSTree: ", MSTree)
    odd_vertexes = find_odd_vertexes(MSTree)
    print("Odd vertexes in MSTree: ", odd_vertexes)
    minimum_weight_matching(MSTree, T, odd_vertexes)
    print("Minimum weight matching: ", MSTree)
    tour = euler_tour(MSTree, T)
    print("Euler circuit: ", tour)

    #delete repeated vertices in Euler cycle to create Hamiltonian cycle and find solution for TSP
    current = tour[0]
    path = [current]
    visited = [False] * len(tour)
    length = 0
    for v in tour[1:]:
        if not visited[v]:
            path.append(v)
            visited[v] = True
            length += T[current][v]
            current = v
    path.append(path[0])

    end_time = time.time() - start_time
    print("Result path: ", path)
    print("Result length of the path: ", length)
    print("Total time: ", end_time, "seconds")

    return length, path

tsp()
