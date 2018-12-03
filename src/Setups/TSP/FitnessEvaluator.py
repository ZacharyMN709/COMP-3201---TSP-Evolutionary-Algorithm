from src.EA_Methods.HelperTemplate import BaseHelper


class FitnessHelper(BaseHelper):
    def __init__(self, var_helper, data_type):
        name_method_pairs = [('Euclidean', self.euclidean_distance)
                             ]
        super().__init__(var_helper, data_type, name_method_pairs)

    def __str__(self):
        return super().__str__().format('FitnessHelper')

    def euclidean_distance(self, indiv):
        return sum([])
