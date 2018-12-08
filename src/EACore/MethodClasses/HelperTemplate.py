class BaseHelper:
    """
    A template class for all of the method helper classes.
    Contains functions for intended expansions which are not presently implemented.
    """
    def __init__(self, var_helper, nm_pairs, default_method=None):
        """
        :param var_helper: A reference to an EAVarHelper instance.
        :param nm_pairs: The list of class methods to be usable outside the class.
        :param default_method: Default: None. For future use.
        """
        self.vars = var_helper
        self.name_method_pairs = nm_pairs
        self.name_to_index_dict = {self.name_method_pairs[x][0]: x for x in range(len(self.name_method_pairs))}
        if default_method is not None:
            self.selected_method = self.get_func_from_index(default_method)
        else:
            self.selected_method = None

    def __str__(self):
        template = 'Methods available in {}:\n'
        for i in range(len(self.name_method_pairs)):
            template += '  {}:  {}\n'.format(i, self.name_method_pairs[i][0])
        return template

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.name_method_pairs)

    def get_func_from_index(self, i):
        """
        :param i: An integer.
        :return: Returns the function pointer associated with that index.
        """
        try:
            return self.name_method_pairs[i][1]
        except IndexError:
            print('Method not found! Returning None!')
            return None

    def set_func_from_index(self, i):
        # TODO - For future implementation of accessing the function from the helper class
        self.selected_method = self.get_func_from_index(i)
