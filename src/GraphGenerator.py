from src.StatsHolder import StatsHolder
from src.Setups.TSP.TSP_Display import GraphingHelper
import pandas as pd

# Set-up easy grabbing of previously compiled stats.
def pickle_to_df(identity_tuple, truncate):
    def resolve_unpickle_tuples(method_name, country, implementation):
        # (File_name, country, method)
        if method_name == 'Population':
            return [('{}10214 G10000.txt'.format(x), country, implementation) for x in range(3)]
        if method_name == 'Mutation':
            return [('210{}14 G10000.txt'.format(x), country, implementation) for x in range(4)]
        if method_name == 'Management':
            return [('21021{} G10000.txt'.format(x), country, implementation) for x in range(5)]

    method_name, country, implementation = identity_tuple
    to_unpickle = resolve_unpickle_tuples(method_name, country, implementation)
    stat_objs = [StatsHolder.stat_obj_from_pickle(x) for x in to_unpickle]
    summaries = [s.average_generation_fitness() for s in stat_objs]
    optimums = [s.best_generation_fitness() for s in stat_objs]
    x_axis = {'x': [x for x in range(len(summaries[0]))][truncate:-1]}
    if method_name == 'Population':
        summaries = {stat_objs[y].POPULATION_METHOD : summaries[y][truncate:-1] for y in range(len(summaries))}
        optimums = {stat_objs[y].POPULATION_METHOD : optimums[y][truncate:-1] for y in range(len(optimums))}
    if method_name == 'Mutation':
        summaries = {stat_objs[y].MUTATION_METHOD : summaries[y][truncate:-1] for y in range(len(summaries))}
        optimums = {stat_objs[y].MUTATION_METHOD : optimums[y][truncate:-1] for y in range(len(optimums))}
    if method_name == 'Management':
        summaries = {stat_objs[y].MANAGEMENT_METHOD : summaries[y][truncate:-1] for y in range(len(summaries))}
        optimums = {stat_objs[y].MANAGEMENT_METHOD : optimums[y][truncate:-1] for y in range(len(optimums))}
    return pd.DataFrame({**x_axis, **summaries}), pd.DataFrame({**x_axis, **optimums})


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

    FILENUM = 1  # 0: 8-Queens   1: Sahara   2: Uruguay   3: Canada   4: Test World
    METHOD = 0  # 0: Lists   1: Numpy Arrays   2: C Arrays

    grapher = GraphingHelper(FILENUM)  ## initialize the grapher with the Uruguay data.
    tests = ['Management', 'Mutation', 'Population']

    for x in tests:
        id_tuple = (x, FILENUM, METHOD)
        avgs, opts = pickle_to_df(id_tuple, 0)
        grapher.quad_plot(avgs, opts)
        savefig('{} - {} - {} Tests.png'.format(FILE_DICT[FILENUM], METHOD_DICT[METHOD], x), bbox_inches='tight')
        plt.show()
