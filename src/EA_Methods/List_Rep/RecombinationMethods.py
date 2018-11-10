from random import random, randint


# region Globals and Setters
genome_length = 0
crossover_rate = 0.9
p1 = 2
p2 = 5
p3 = 8


def set_genome_length(i):
    global genome_length
    genome_length = i


def set_crossover_rate(i):
    global crossover_rate
    crossover_rate = i


def set_crossover_points(i, j, k):
    global p1, p2, p3
    if i > k: i, k = k, i
    if i > j: i, j = j, i
    if j > k: j, k = k, j

    p1, p2, p3 = i, j, k
# endregion


# region Recombination Methods

# Takes in a method, and automatically manages the incoming population/parents
#  to mate parents pairwise, based on the recombination rate.
def method_randomizer(func):
    def select_method(population, parents_index):
        offspring = []
        # Pair off parents,
        for i in range(0, len(parents_index), 2):
            # apply the mutation randomly,
            if random() < crossover_rate:
                off1, off2 = func(population[parents_index[i]], population[parents_index[i + 1]])
            # or add copies of the originals, if no mutation happens.
            else:
                off1, off2 = population[parents_index[i]].copy(), population[parents_index[i + 1]].copy()

            # Finaly, add the offspring to the list.
            offspring.append(off1)
            offspring.append(off2)
        return offspring
    return select_method


@method_randomizer
def order_crossover(parent1, parent2):
    # Makes the offspring from the selected sub-sequence, and all the elements not in that sub-sequence.
    offspring1 = parent1[:p1] + [x for x in parent2[p1:] + parent2[:p1] if x not in parent1[:p1]]
    offspring2 = parent2[:p1] + [x for x in parent1[p1:] + parent1[:p1] if x not in parent2[:p1]]
    return offspring1, offspring2


@method_randomizer
def pmx_crossover(parent1, parent2):
    # Find the differing genetic material of crossover segments, to handle duplicates.
    diffs = set(parent1[p1:p2]) ^ set(parent2[p1:p2])

    def pmx_helper(parent, mate):
        # Generate simple offspring template, which contains some duplicates, to be modified.
        offspring = mate[:p1] + parent[p1:p2] + mate[p2:]
        off_mod = []
        for x in mate[p1:p2]:
            if x in diffs:
                # Find the index of the unique element in the mate's crossover segment,
                i = mate.index(x)
                # then in the mate, find the index of the element in the parent at the previous index,
                # until the found index is outside the index range of the crossover points.
                while p1 <= i < p2:
                    i = mate.index(parent[i])
                # Save the index of the duplicate to overwrite, and the element that replaces it.
                off_mod.append((x,  i))
        # Finally, make all of the needed adjustments to the offspring.
        for c in off_mod: offspring[c[1]] = c[0]
        return offspring

    return pmx_helper(parent1, parent2), pmx_helper(parent2, parent1)


@method_randomizer
def edge_crossover(parent1, parent2):
    edge_list = {key: set() for key in parent1}
    for x in range(-1, genome_length-1):
        edge_list[parent1[x]].add(parent1[x-1])
        edge_list[parent1[x]].add(parent1[x+1])
        edge_list[parent2[x]].add(parent2[x-1])
        edge_list[parent2[x]].add(parent2[x+1])
    edge_list_lens = {key: set() for key in range(2, 6)}
    for key in edge_list: edge_list_lens[len(edge_list[key])].add(key)

    def edge_helper(edge_list, edge_list_len):
        offspring = [None for _ in range(genome_length)]
        x = randint(0, genome_length - 1)
        offspring[0] = x




    print('Stub Method!')
    return parent1, parent2
# endregion


if __name__ == '__main__':
    from random import sample
    genome_length = 10
    crossover_rate = 1
    test = [sample([c for c in range(genome_length)], genome_length) for _ in range(genome_length)]
    out = pmx_crossover(test, [c for c in range(genome_length)])
    for x in range(len(test)):
        print(test[x])
        print(out[x])
        print('- - -')
