from src.EACore.MethodClasses.HelperTemplate import BaseHelper


class FitnessHelper(BaseHelper):
    def __init__(self, var_helper):
        name_method_pairs = [('Maximization', self.fitness_8queen),
                             ('Diagonal', self.fitness_8queen_quick)
                             ]
        super().__init__(var_helper, name_method_pairs)

    def __str__(self):
        return super().__str__().format('FitnessHelper')

    def inc(self, dic, key):
        if key in dic:
            dic[key] += 1
        else:
            dic[key] = 0

    def clashes(self, dic):
        return int(sum([(((1 + dic[x]) * dic[x]) / 2) for x in dic if dic[x] != 0]))

    def fitness_8queen(self, individual):  # maximization
        M = 28

        neg_diag = dict()
        pos_diag = dict()
        m = len(individual)

        for i in range(m):
            self.inc(neg_diag, (i - individual[i]))
            self.inc(pos_diag, (i + individual[i]))

        return M - (self.clashes(neg_diag) + self.clashes(pos_diag))

    def fitness_8queen_quick(self, individual):  # maximization
        m = len(individual)
        neg_diag = set([i - individual[i] for i in range(m)])
        pos_diag = set([i + individual[i] for i in range(m)])

        return len(neg_diag) + len(pos_diag)
