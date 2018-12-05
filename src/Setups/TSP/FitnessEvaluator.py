from src.EA_Methods.HelperTemplate import BaseHelper


class FitnessHelperGenerator:
    def __init__(self, data):
        self.dists = data.dists

    def make_fit_helper(self, var_helper):
        return FitnessHelper(var_helper, self.dists)


class FitnessHelper(BaseHelper):
    def __init__(self, var_helper, dists):
        name_method_pairs = [('Euclidean', self.euclidean_distance)
                             ]
        super().__init__(var_helper, name_method_pairs)
        self.dists = dists

    def __str__(self):
        return super().__str__().format('FitnessHelper')

    def euclidean_distance(self, indiv):
        return sum([self.dists[indiv[i - 1]][indiv[i]] for i in range(self.vars.genome_length)])

    def single_swap_fast_calc(self, fitness, lst1, lst2):
        to_sub = self.dists[lst1[0]][lst1[1]] + self.dists[lst1[2]][lst1[1]] + \
                 self.dists[lst2[0]][lst2[1]] + self.dists[lst2[2]][lst2[1]]
        to_add = self.dists[lst1[0]][lst2[1]] + self.dists[lst1[2]][lst2[1]] + \
                 self.dists[lst2[0]][lst1[1]] + self.dists[lst2[2]][lst1[1]]
        return fitness + to_add - to_sub
