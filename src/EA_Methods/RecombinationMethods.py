from random import random, randint
from copy import deepcopy


class RecombinationHelper:
    def __init__(self, var_helper, method):
        self.vars = var_helper
        self.method = method

    # region Recombination Methods

    # Takes in a method, and automatically manages the incoming population/parents
    #  to mate parents pairwise, based on the recombination rate.
    def method_randomizer(self, func):
        def select_method(population, parents_index):
            offspring = [None] * len(parents_index)
            # Pair off parents,
            for i in range(0, len(parents_index), 2):
                # apply the mutation randomly,
                if random() < self.vars.crossover_rate:
                    offspring[i], offspring[i + 1] = \
                        func(population[parents_index[i]], population[parents_index[i + 1]])
                # or add copies of the originals, if no mutation happens.
                else:
                    offspring[i], offspring[i + 1] = \
                        population[parents_index[i]].copy(), population[parents_index[i + 1]].copy()
            return offspring
        return select_method

    @method_randomizer
    def order_crossover(self, parent1, parent2):
        # Makes the offspring from the selected sub-sequence, and all the elements not in that sub-sequence.
        offspring1 = parent1[:self.vars.p1] + [x for x in parent2[self.vars.p1:] + parent2[:self.vars.p1] if x not in set(parent1[:self.vars.p1])]
        offspring2 = parent2[:self.vars.p1] + [x for x in parent1[self.vars.p1:] + parent1[:self.vars.p1] if x not in set(parent2[:self.vars.p1])]
        return offspring1, offspring2

    @method_randomizer
    def pmx_crossover(self, parent1, parent2):
        # Find the differing genetic material of crossover segments, to handle duplicates.
        diffs = set(parent1[self.vars.p1:self.vars.p2]) ^ set(parent2[self.vars.p1:self.vars.p2])

        def pmx_helper(parent, mate):
            # Generate simple offspring template, which contains some duplicates, to be modified.
            offspring = mate[:self.vars.p1] + parent[self.vars.p1:self.vars.p2] + mate[self.vars.p2:]
            off_mod = []
            for x in mate[self.vars.p1:self.vars.p2]:
                if x in diffs:
                    # Find the index of the unique element in the mate's crossover segment,
                    i = mate.index(x)
                    # then in the mate, find the index of the element in the parent at the previous index,
                    # until the found index is outside the index range of the crossover points.
                    while self.vars.p1 <= i < self.vars.p2:
                        i = mate.index(parent[i])
                    # Save the index of the duplicate to overwrite, and the element that replaces it.
                    off_mod.append((x,  i))
            # Finally, make all of the needed adjustments to the offspring.
            for c in off_mod: offspring[c[1]] = c[0]
            return offspring

        return pmx_helper(parent1, parent2), pmx_helper(parent2, parent1)

    @method_randomizer
    def edge_crossover(self, parent1, parent2):
        # Make the edge list.
        edge_list = {key: set() for key in parent1}
        for x in range(-1, self.vars.genome_length-1):
            edge_list[parent1[x]].add(parent1[x-1])
            edge_list[parent1[x]].add(parent1[x+1])
            edge_list[parent2[x]].add(parent2[x-1])
            edge_list[parent2[x]].add(parent2[x+1])

        # Make a dictionary of edge list lengths to simplify handling of edges.
        edge_list_len = {key: set() for key in range(0, 5)}
        for key in edge_list: edge_list_len[len(edge_list[key])].add(key)

        def edge_helper(edge_list, edge_list_len):
            # Generate an empty individual
            offspring = [None for _ in range(self.vars.genome_length)]

            # Randomly select the first element to insert
            x = randint(0, self.vars.genome_length - 1)

            # TODO - Fix
            for i in range(0, self.vars.genome_length-1):
                # Set the element in the list, and increment
                offspring[i] = x

                # Clean and update the edge list and length list
                for y in edge_list[x]:
                    edge_list_len[len(edge_list[y]) - 1].add(y)
                    edge_list_len[len(edge_list[y])].remove(y)
                    edge_list[y].remove(x)
                edge_list_len[len(edge_list[x])].remove(x)

                # Find the next edge through the lowest list length
                for y in range(1, 5):
                    temp = edge_list[x] & edge_list_len[y]
                    if len(temp) != 0:
                        del edge_list[x]
                        x = temp.pop()
                        break

            # Set the last element manually, as it is the only one left.
            offspring[-1] = edge_list[x].pop()
            return offspring

        return edge_helper(deepcopy(edge_list), deepcopy(edge_list_len)), edge_helper(edge_list, edge_list_len)
    # endregion
