from src.StatsHolder import StatsHolder
from src.Setups.TSP.TSP_Display import GraphingHelper
import pandas as pd


def resolve_unpickle_tuples(method_name, country, implementation, population):
    # (File_name, country, method)
    if method_name == 'Population':
        return [('{}10214 G{}.txt'.format(x, population), country, implementation) for x in range(3)]
    if method_name == 'Mutation':
        return [('210{}14 G{}.txt'.format(x, population), country, implementation) for x in range(4)]
    if method_name == 'Management':
        return [('21021{} G{}.txt'.format(x, population), country, implementation) for x in range(5)]


# Set-up easy grabbing of previously compiled stats.
def pickle_to_df(identity_tuple, truncate):
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
    from src.Setups.TSP import TSP_LST
    TSP_LST.read_tsp_file(FILENUM)
    TSP_LST.set_fitness_function(TSP_LST.euclidean_distance)
    genome_length = len(TSP_LST.LOCATIONS)


    def indiv_helper(indiv_num):
        if indiv_num == 0:
            return TSP_LST.single_random_individual(genome_length)
        if indiv_num == 1:
            return TSP_LST.heuristic_cluster_initialization(1, genome_length)[0][0]
        if indiv_num == 2:
            return TSP_LST.heuristic_euler_initialization(1, genome_length)[0][0]

    indiv1, indiv2 = indiv_helper(type1), indiv_helper(type2)
    grapher.indiv_dual_plot((INIT_DICT[type1], indiv1), (INIT_DICT[type2], indiv2))
    savefig('{} Initialization - {} vs {}.png'.format(FILE_DICT[FILENUM], INIT_DICT[type1], INIT_DICT[type2]), bbox_inches='tight')
    plt.show()


def bset_vs_avgs(type1, type2):
    from src.Setups.TSP import TSP_LST
    TSP_LST.read_tsp_file(FILENUM)
    TSP_LST.set_fitness_function(TSP_LST.euclidean_distance)
    genome_length = len(TSP_LST.LOCATIONS)


    def indiv_helper(indiv_num):
        if indiv_num == 0:
            return TSP_LST.single_random_individual(genome_length)
        if indiv_num == 1:
            return TSP_LST.heuristic_cluster_initialization(1, genome_length)[0][0]
        if indiv_num == 2:
            return TSP_LST.heuristic_euler_initialization(1, genome_length)[0][0]

    indiv1, indiv2 = indiv_helper(type1), indiv_helper(type2)
    grapher.indiv_dual_plot((INIT_DICT[type1], indiv1), (INIT_DICT[type2], indiv2))
    savefig('{} Initialization - {} vs {}.png'.format(FILE_DICT[FILENUM], INIT_DICT[type1], INIT_DICT[type2]), bbox_inches='tight')
    plt.show()


def gen_quad_pickle_plots():
    tests = ['Management', 'Mutation', 'Population']

    for x in tests:
        id_tuple = (x, FILENUM, METHOD, POP_SIZE)
        avgs, opts = pickle_to_df(id_tuple, 0)
        grapher.quad_plot(avgs, opts)
        savefig('{} - {} - {} Tests.png'.format(FILE_DICT[FILENUM], METHOD_DICT[METHOD], x), bbox_inches='tight')
        plt.show()


def gen_dual_pickle_plots():
    tests = ['Management', 'Mutation', 'Population']

    for x in tests:
        id_tuple = (x, FILENUM, METHOD, POP_SIZE)
        avgs, opts = pickle_to_df(id_tuple, 0)
        grapher.modular_dual_plot(avgs, opts, False)
        savefig('{} - {} - {} True Fitness.png'.format(FILE_DICT[FILENUM], METHOD_DICT[METHOD], x), bbox_inches='tight')
        plt.show()
        grapher.modular_dual_plot(avgs, opts, True)
        savefig('{} - {} - {} Relative Fitness.png'.format(FILE_DICT[FILENUM], METHOD_DICT[METHOD], x), bbox_inches='tight')
        plt.show()


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


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from pylab import savefig

    FILENUM = 3  # 0: 8-Queens   1: Sahara   2: Uruguay   3: Canada   4: Test World
    METHOD = 2  # 0: Lists   1: Numpy Arrays   2: C Arrays
    POP_SIZE = 1000

    '''
    for y in [1, 2]:
        FILENUM = y
        grapher = GraphingHelper(FILENUM)
        for x in [0, 2]:
            METHOD = x
            gen_dual_pickle_plots()
    '''

    #grapher = GraphingHelper(1)
    grapher = None
    for y in [1, 2, 3]:
        for x in ['Population', 'Mutation', 'Management']:
            for z in [0, 2]:
                if y == 3 and z == 0: continue
                gens = 10000
                if y == 3: gens = 1000
                fnames = resolve_unpickle_tuples(x, y, z, gens)
                items = list()
                items.append(StatsHolder.stat_cols())
                for f in fnames:
                    stat_obj = StatsHolder.stat_obj_from_pickle(f)
                    items.append(stat_obj.stat_items())

                for i in range(len(items[0])):
                    for col in items:
                        print(col[i], end='')
                    print()
                print()
