"""
A module which plots data from pickled 'StatsHolder's. Future implementations will move away from this.
This is not meant for public use, and will be removed in the future.
"""
from src.Other.StatsHolder import StatsHolder
from src.Setups.TSP.TSP_Display import GraphingHelper
import pandas as pd


# Set-up easy grabbing of previously compiled stats.
def pickle_to_df(identity_tuple, truncate):
    def resolve_unpickle_tuples(method_name, country, implementation, population):
        # (File_name, country, method)
        if method_name == 'Population':
            return [('{}10214 G{}.txt'.format(x, population), country, implementation) for x in range(3)]
        if method_name == 'Mutation':
            return [('210{}14 G{}.txt'.format(x, population), country, implementation) for x in range(4)]
        if method_name == 'Management':
            return [('21021{} G{}.txt'.format(x, population), country, implementation) for x in range(5)]

    method_name, country, implementation, pop = identity_tuple
    to_unpickle = resolve_unpickle_tuples(method_name, country, implementation, pop)
    summaries = {}
    optimums = {}
    for x in to_unpickle:
        stat_obj = StatsHolder.stat_obj_from_pickle(x)
        sum_list = stat_obj.average_generation_fitness()[truncate:-1]
        opt_list = stat_obj.best_generation_fitness()[truncate:-1]
        if method_name == 'Population':
            summaries[stat_obj.POPULATION_METHOD] = sum_list
            optimums[stat_obj.POPULATION_METHOD] = opt_list
        if method_name == 'Mutation':
            summaries[stat_obj.MUTATION_METHOD] = sum_list
            optimums[stat_obj.MUTATION_METHOD] = opt_list
        if method_name == 'Management':
            summaries[stat_obj.MANAGEMENT_METHOD] = sum_list
            optimums[stat_obj.MANAGEMENT_METHOD] = opt_list

    return pd.DataFrame(summaries), pd.DataFrame(optimums)


def gen_two_indivs(type1, type2):
    from src.Setups.TSP import FileLoader, PopulationInitialization
    from src.EACore.EAVarHelper import EAVarHelper

    file_data = FileLoader.LoadHelper(FILENUM)
    gen = PopulationInitialization.PopulationInitializationGenerator(file_data.data, FILENUM)
    helper = gen.make_pop_helper(EAVarHelper(file_data.genome_length, False) ,0)

    def indiv_helper(indiv_num):
        if indiv_num == 0:
            return helper.single_random_individual()
        if indiv_num == 1:
            return helper.single_cluster_individual()
        if indiv_num == 2:
            return helper.single_euler_individual()

    indiv1, indiv2 = indiv_helper(type1), indiv_helper(type2)
    grapher.indiv_dual_plot((INIT_DICT[type1], indiv1), (INIT_DICT[type2], indiv2))


def gen_pickle_plots():
    tests = ['Management', 'Mutation', 'Population']

    for x in tests:
        id_tuple = (x, FILENUM, METHOD, POP_SIZE)
        avgs, opts = pickle_to_df(id_tuple, 0)
        grapher.quad_plot(avgs, opts)
        savefig('{} - {} - {} Tests.png'.format(FILE_DICT[FILENUM], METHOD_DICT[METHOD], x), bbox_inches='tight')
        plt.show()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from pylab import savefig

    FILE_DICT = {0: '8-Queens',
                 1: 'Sahara',
                 2: 'Uruguay',
                 3: 'Canada',
                 4: 'Test World'}

    METHOD_DICT = {0: 'Lists',
                   1: 'Numpy',
                   2: 'Arrays'}

    INIT_DICT = {0: 'Random',
                 1: 'Cluster',
                 2: 'Christofides'}

    FILENUM = 1  # 0: 8-Queens   1: Sahara   2: Uruguay   3: Canada   4: Test World
    METHOD = 0  # 0: Lists   1: Numpy Arrays   2: C Arrays
    POP_SIZE = 1000

    grapher = GraphingHelper(FILENUM)
    gen_two_indivs(0, 1)
