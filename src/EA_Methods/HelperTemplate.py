class BaseHelper:
    def __init__(self, var_helper, data_type, nm_pairs, default_method=None):
        self.vars = var_helper
        self.data_type = data_type
        self.name_method_pairs = nm_pairs
        self.name_to_index_dict = {self.name_method_pairs[x][0]: x for x in range(len(self.name_method_pairs))}
        if default_method is not None:
            self.selected_method = self.get_func_from_index(default_method)
        else:
            self.selected_method = None

    def __str__(self):
        template = 'Methods available in {}:\n'
        for i in range(len(self.name_method_pairs)):
            template += '  {}:  {}'.format(i, self.name_method_pairs[i][0])
        return template

    def __repr__(self):
        return self.__str__()

    def get_func_from_index(self, i):
        try:
            return self.name_method_pairs[i][1]
        except IndexError:
            print('Method not found! Returning None!')
            return None

    def set_func_from_index(self, i):
        # TODO - For future implementation of accessing the function from the helper class
        self.selected_method = self.get_func_from_index(i)

