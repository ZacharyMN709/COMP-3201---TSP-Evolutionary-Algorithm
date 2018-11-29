class BaseHelper:
    def __init__(self, var_helper, method, nm_pairs):
        self.vars = var_helper
        self.method = method
        self.name_method_pairs = nm_pairs
        self.name_to_index_dict = {self.name_method_pairs[x][0]: x for x in range(len(self.name_method_pairs))}

    def __str__(self):
        template = 'Methods available in {}:\n'
        for i in range(len(self.name_method_pairs)):
            template += '  {}:  {}'.format(i, self.name_method_pairs[i][0])
        return template

    def __repr__(self):
        return self.__str__()