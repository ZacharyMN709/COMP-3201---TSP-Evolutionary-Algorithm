
class FitnessHelper:
    def __init__(self, var_helper, method):
        self.vars = var_helper
        self.method = method
        self.FITNESS_METHODS = [('Euclidean', self.euclidean_distance)
                                ]
        self.FITNESS_DICT = {self.FITNESS_METHODS[x][0]: x for x in range(len(self.FITNESS_METHODS))}

    def get_func_from_index(self, i):
        return self.FITNESS_METHODS[i][1]

    def euclidean_distance(self, indiv):
        return sum([])
