import numpy as np
from src.EACore.MethodClasses.HelperTemplate import BaseHelper
from random import random, randint
from copy import deepcopy


class RecombinationHelper(BaseHelper):
    """
    This class may need to be modified or extended in order to properly support numpy.
    However it presently supports both c arrays and python lists.
    """
    def __init__(self, var_helper, data_type):
        """
        :param var_helper: A reference to an EAVarHelper instance.
        :param data_type: The integer representation for the data type the individuals use. Determines which function
        pointers that can be returned.
        """
        if data_type != 1:
            name_method_pairs = [('Order Crossover', self.recombine_parents_using(self.order_crossover)),
                                 ('PMX Crossover', self.recombine_parents_using(self.pmx_crossover))
                                 ]
        else:
            name_method_pairs = [('Order Crossover', self.recombine_parents_using(self.numpy_order_crossover)),
                                 ('PMX Crossover', self.recombine_parents_using(self.numpy_pmx_crossover))
                                 ]
        super().__init__(var_helper, name_method_pairs)

    def __str__(self):
        return super().__str__().format('RecombinationHelper')

    # region Recombination Methods

    # Takes in a method, and automatically manages the incoming population/parents
    #  to mate parents pairwise, based on the recombination rate.
    def recombine_parents_using(self, func):
        def pair_parents(population, parents_index):
            offspring = [None] * len(parents_index)
            # Pair off parents,
            for i in range(0, len(parents_index), 2):
                # apply the crossover randomly,
                if random() < self.vars.crossover_rate:
                    offspring[i], offspring[i + 1] = \
                        func(population[parents_index[i]], population[parents_index[i + 1]])
                # or add copies of the originals, if no mutation happens.
                else:
                    offspring[i], offspring[i + 1] = \
                        deepcopy(population[parents_index[i]]), deepcopy(population[parents_index[i + 1]])
            return offspring

        pair_parents.__name__ = func.__name__
        return pair_parents

    def order_crossover(self, parent1, parent2):
        """
        Takes the first part of a genomic sequence, and then appends all the missing elements in the order they're
        found in the other parent.
        :param parent1: An individual from the population list
        :param parent2: An individual from the population list
        :return: Two new offspring
        """
        def crossoverhelper(parent, offspring):
            # Set the start point if where to copy, and set the elements to skip
            start, exclude = self.vars.cp1, set(offspring[:self.vars.cp1])

            # From the start point to the end of the list, add the non-duplicates
            for i in range(self.vars.cp1, self.vars.genome_length):
                if parent[i] not in exclude:
                    offspring[start] = parent[i]
                    start += 1

            # From the beginning of the list to the start point , add the non-duplicates
            for i in range(0, self.vars.cp1):
                if parent[i] not in exclude:
                    offspring[start] = parent[i]
                    start += 1
            return offspring

        # Copy the parents, so that modifying them does not cause problems elsewhere.
        offspring1, offspring2 = deepcopy(parent1), deepcopy(parent2)
        return crossoverhelper(parent2, offspring1), crossoverhelper(parent1, offspring2)

    def pmx_crossover(self, parent1, parent2):
        """
        A function which implements 'Partially Mapped Crossover'. Please see in-line comments for
        further explanation of how it works.
        :param parent1: An individual from the population list
        :param parent2: An individual from the population list
        :return: Two new offspring
        """
        # Find the differing genetic material of crossover segments, to handle duplicates.
        diffs = set(parent1[self.vars.cp1:self.vars.cp2]) ^ set(parent2[self.vars.cp1:self.vars.cp2])

        def pmx_helper(parent, mate):
            # Generate simple offspring template, which contains some duplicates, to be modified.
            offspring = deepcopy(mate)
            for i in range(self.vars.cp1, self.vars.cp2):
                offspring[i] = parent[i]

            off_mod = []
            for x in mate[self.vars.cp1:self.vars.cp2]:
                if x in diffs:
                    # Find the index of the unique element in the mate's crossover segment,
                    i = mate.index(x)
                    # then in the mate, find the index of the element in the parent at the previous index,
                    # until the found index is outside the index range of the crossover points.
                    while self.vars.cp1 <= i < self.vars.cp2:
                        i = mate.index(parent[i])
                    # Save the index of the duplicate to overwrite, and the element that replaces it.
                    off_mod.append((x, i))
            # Finally, make all of the needed adjustments to the offspring.
            for c in off_mod: offspring[c[1]] = c[0]
            return offspring

        return pmx_helper(parent1, parent2), pmx_helper(parent2, parent1)

    def numpy_order_crossover(self, parent1, parent2):
        """
        Takes the first part of a genomic sequence, and then appends all the missing elements in the order they're
        found in the other parent.
        :param parent1: An individual from the population list
        :param parent2: An individual from the population list
        :return: Two new offspring
        """
        # TODO - Optimize, by reducing/removing concatenation
        # Makes the offspring from the selected sub-sequence, and all the elements not in that sub-sequence.
        def crossover_helper(parent, mate):
            # Shift the individual's genome
            temp1 = np.roll(parent, self.vars.genome_length - self.vars.cp1)
            # Make a mask of the elements to keep
            mask1 = np.isin(temp1, mate[:self.vars.cp1], invert=True)
            # Then use that mask to take the start, and all the non-duplicates and append them together.
            return np.concatenate((mate[:self.vars.cp1], temp1[mask1]), axis=None)
        return crossover_helper(parent1, parent2), crossover_helper(parent2, parent1)

    def numpy_pmx_crossover(self, parent1, parent2):
        """
        A function which implements 'Partially Mapped Crossover'. Please see in-line comments for
        further explanation of how it works.
        :param parent1: An individual from the population list
        :param parent2: An individual from the population list
        :return: Two new offspring
        """
        # TODO - Optimize, by reducing/removing concatenation
        # Find the differing genetic material of crossover segments, to handle duplicates.
        diffs = set(parent1[self.vars.cp1:self.vars.cp2]) ^ set(parent2[self.vars.cp1:self.vars.cp2])
    
        def pmx_helper(parent, mate):
            # Generate simple offspring template, which contains some duplicates, to be modified.
            offspring = np.concatenate((mate[:self.vars.cp1], parent[self.vars.cp1:self.vars.cp2], mate[self.vars.cp2:]), axis=None)
            off_mod = []
            for x in mate[self.vars.cp1:self.vars.cp2]:
                if x in diffs:
                    # Find the index of the unique element in the mate's crossover segment,
                    i, = np.where(mate == x)
                    # then in the mate, find the index of the element in the parent at the previous index,
                    # until the found index is outside the index range of the crossover points.
                    while self.vars.cp1 <= i < self.vars.cp2:
                        i, = np.where(mate == parent[i])
                    # Save the index of the duplicate to overwrite, and the element that replaces it.
                    off_mod.append((x,  i))
            # Finally, make all of the needed adjustments to the offspring.
            for c in off_mod: offspring[c[1]] = c[0]
            return offspring
    
        return pmx_helper(parent1, parent2), pmx_helper(parent2, parent1)

    def edge_crossover(self, parent1, parent2):
        # TODO - Fix. Currently giving indexing errors.
        # Make the edge list.
        edge_list = {key: set() for key in parent1}
        for x in range(-1, self.vars.genome_length - 1):
            edge_list[parent1[x]].add(parent1[x - 1])
            edge_list[parent1[x]].add(parent1[x + 1])
            edge_list[parent2[x]].add(parent2[x - 1])
            edge_list[parent2[x]].add(parent2[x + 1])

        # Make a dictionary of edge list lengths to simplify handling of edges.
        edge_list_len = {key: set() for key in range(0, 5)}
        for key in edge_list: edge_list_len[len(edge_list[key])].add(key)

        def edge_helper(edge_list, edge_list_len):
            # Generate an empty individual
            offspring = [None for _ in range(self.vars.genome_length)]

            # Randomly select the first element to insert
            x = randint(0, self.vars.genome_length - 1)

            for i in range(0, self.vars.genome_length - 1):
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


if __name__ == '__main__':
    from src.EACore.EAVarHelper import EAVarHelper
    from time import time
    from random import shuffle

    rc = RecombinationHelper(EAVarHelper(20, False), 0)

    methods = [rc.order_crossover,
               rc.pmx_crossover,
               ]

    for x in methods:
        start = time()
        for y in range(100):
            indiv = [x for x in range(20)]
            indiv2 = indiv.copy()
            shuffle(indiv2)
            print(x(indiv, indiv2))
        print(time() - start)
