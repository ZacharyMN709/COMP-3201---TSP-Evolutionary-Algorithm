from src.Testing import EATester
from Pickle_Helper import pickle_stats_obj
import os


FILE_DICT = {0: '8-Queens',
             1: 'Sahara',
             2: 'Uruguay',
             3: 'Canada',
             4: 'Test World'}

METHOD_DICT = {0: 'Lists',
               1: 'Numpy',
               2: 'Arrays'}


def import_modules(FILENUM=0, MODULE=0):
    if not FILENUM:
        from src.EA_Methods.List_Rep import ParentSelectionMethods as PSM
        from src.EA_Methods.List_Rep import MutationMethods as MM
        from src.EA_Methods.List_Rep import RecombinationMethods as RM
        from src.EA_Methods.List_Rep import SurvivorSelectionMethods as SSM
        from src.EA_Methods.List_Rep import PopulationManagementMethods as PMM
        from src.Setups.EightQueens import EightQueen as DEF
    else:
        if MODULE == 2:
            from src.EA_Methods.Array_Rep import ParentSelectionMethods as PSM
            from src.EA_Methods.Array_Rep import MutationMethods as MM
            from src.EA_Methods.Array_Rep import RecombinationMethods as RM
            from src.EA_Methods.Array_Rep import SurvivorSelectionMethods as SSM
            from src.EA_Methods.Array_Rep import PopulationManagementMethods as PMM
            from src.Setups.TSP import TSP_ARR as DEF
        elif MODULE == 1:
            from src.EA_Methods.Numpy_Rep import ParentSelectionMethods as PSM
            from src.EA_Methods.Numpy_Rep import MutationMethods as MM
            from src.EA_Methods.Numpy_Rep import RecombinationMethods as RM
            from src.EA_Methods.Numpy_Rep import SurvivorSelectionMethods as SSM
            from src.EA_Methods.Numpy_Rep import PopulationManagementMethods as PMM
            from src.Setups.TSP import TSP_NPY as DEF
        else:
            from src.EA_Methods.List_Rep import ParentSelectionMethods as PSM
            from src.EA_Methods.List_Rep import MutationMethods as MM
            from src.EA_Methods.List_Rep import RecombinationMethods as RM
            from src.EA_Methods.List_Rep import SurvivorSelectionMethods as SSM
            from src.EA_Methods.List_Rep import PopulationManagementMethods as PMM
            from src.Setups.TSP import TSP_LST as DEF
    return PSM, RM, MM, SSM, DEF, PMM


def generate_algorithm(FILENUM=0, MODULE=0, MULTITHREAD=False):
    if not FILENUM:
        from src.Setups.EightQueens.EightQueen import random_initialization as initialize
        from src.Setups.EightQueens.EightQueen import fitness_8queen as eval_fitness
        genome_len = 8
    else:
        if MODULE == 2:
            from src.Setups.TSP.TSP_ARR import read_tsp_file as parse_file
            from src.Setups.TSP.TSP_ARR import random_initialization as initialize
            from src.Setups.TSP.TSP_ARR import euclidean_distance as eval_fitness
        elif MODULE == 1:
            from src.Setups.TSP.TSP_NPY import read_tsp_file as parse_file
            from src.Setups.TSP.TSP_NPY import random_initialization as initialize
            from src.Setups.TSP.TSP_NPY import euclidean_distance as eval_fitness
        else:
            from src.Setups.TSP.TSP_LST import read_tsp_file as parse_file
            from src.Setups.TSP.TSP_LST import random_initialization as initialize
            from src.Setups.TSP.TSP_LST import euclidean_distance as eval_fitness
        genome_len = parse_file(FILENUM)

    PSM, RM, MM, SSM, DEF, PMM = import_modules(FILENUM, MODULE)
    tester = EATester(PSM, RM, MM, SSM, DEF, PMM, mt=MULTITHREAD)
    tester.set_params(genome_len, eval_fitness, initialize, None, None, None, None, None)
    return tester


def go_to_project_root():
    script_dir = os.path.dirname(__file__)
    path = os.path.join(script_dir, '..')
    print(path)
    os.chdir(path)
    print("Present working directory:", os.getcwd(), '\n')


print("Present working directory:", os.getcwd(), '\n')

FILENUM = 2  # 0: 8-Queens   1: Sahara   2: Uruguay   3: Canada   4: Test World
METHOD = 0  # 0: Lists   1: Numpy Arrays   2: C Arrays
MULTITHREAD = False
RUNS = 1  # Number of times each combination is run.
GENERATIONS = 10000
SAVE = False

PSM, RM, MM, SSM, DEF, PMM = import_modules(FILENUM, METHOD)

POPULATION_METHODS = [('Random', DEF.random_initialization), ('Cluster', DEF.heuristic_cluster_initialization), ('Euler', DEF.heuristic_euler_initialization)]
PARENT_METHODS = [('MPS', PSM.mps), ('Tourney', PSM.tournament), ('Random', PSM.random_uniform)]
RECOMBINATION_METHODS = [('Order Crossover', RM.order_crossover), ('PMX Crossover', RM.pmx_crossover)]
MUTATION_METHODS = [('Swap', MM.permutation_swap), ('Insert', MM.permutation_insert), ('Inversion', MM.permutation_inversion), ('Shift', MM.permutation_shift)]
SURVIVOR_METHODS = [('Mu + Lambda', SSM.mu_plus_lambda), ('Replace', SSM.replacement)]
MANAGEMENT_METHODS = [('None', PMM.static_return), ('Annealing', PMM.metallurgic_annealing), ('Entropy', PMM.entropic_stabilizing), ('Oroborous', PMM.ouroboric_culling), ('Engineering', PMM.genetic_engineering)]

POPULATION_DICT = {POPULATION_METHODS[x][0]: x for x in range(len(POPULATION_METHODS))}
PARENT_DICT = {PARENT_METHODS[x][0]: x for x in range(len(PARENT_METHODS))}
RECOMBINATION_DICT = {RECOMBINATION_METHODS[x][0]: x for x in range(len(RECOMBINATION_METHODS))}
MUTATION_DICT = {MUTATION_METHODS[x][0]: x for x in range(len(MUTATION_METHODS))}
SURVIVOR_DICT = {SURVIVOR_METHODS[x][0]: x for x in range(len(SURVIVOR_METHODS))}
MANAGEMENT_DICT = {MANAGEMENT_METHODS[x][0]: x for x in range(len(MANAGEMENT_METHODS))}

"""
BASE INDIVIDUAL FOR STATS TESTING
tester.set_test_vars(RUNS, POPULATION_METHODS[2:3], PARENT_METHODS[1:2], RECOMBINATION_METHODS[1:2],
                     MUTATION_METHODS[2:3], SURVIVOR_METHODS[0:1], MANAGEMENT_METHODS[4:5])
"""


'''
POPULATION TESTING
tester.set_test_vars(RUNS, POPULATION_METHODS, PARENT_METHODS[1:2], RECOMBINATION_METHODS[1:2],
                     MUTATION_METHODS[2:3], SURVIVOR_METHODS[0:1], MANAGEMENT_METHODS[4:5])
'''
'''
MUTATION TESTING
tester.set_test_vars(RUNS, POPULATION_METHODS[2:3], PARENT_METHODS[1:2], RECOMBINATION_METHODS[1:2],
                     MUTATION_METHODS, SURVIVOR_METHODS[0:1], MANAGEMENT_METHODS[4:5])
'''
'''
MANAGEMENT TESTING
tester.set_test_vars(RUNS, POPULATION_METHODS[2:3], PARENT_METHODS[1:2], RECOMBINATION_METHODS[1:2],
                     MUTATION_METHODS[2:3], SURVIVOR_METHODS[0:1], MANAGEMENT_METHODS)
'''



tester = generate_algorithm(FILENUM, METHOD, MULTITHREAD)
tester.set_test_vars(RUNS, POPULATION_METHODS[2:3], PARENT_METHODS[1:2], RECOMBINATION_METHODS[1:2],
                     MUTATION_METHODS[2:3], SURVIVOR_METHODS[0:1], MANAGEMENT_METHODS)

if FILENUM:
    from src.Setups.TSP.TSP_Inputs.Optimums import get_best_path
    opt_fitness, opt_individual, true_optimum = get_best_path(FILENUM)
else:
    opt_fitness, true_optimum = 16, True
    opt_individual = [5, 2, 6, 3, 0, 7, 1, 4]

if __name__ == '__main__':

    def save_run():
        # Iterates over each StatsHolder Object
        for a in range(matrix_dimensions[0]):
            for b in range(matrix_dimensions[1]):
                for c in range(matrix_dimensions[2]):
                    for d in range(matrix_dimensions[3]):
                        for e in range(matrix_dimensions[4]):
                            for f in range(matrix_dimensions[5]):
                                if FILENUM != 0:
                                    obj = result_matrix[a][b][c][d][e][f]

                                    indices = (
                                        POPULATION_DICT[obj.POPULATION_METHOD],
                                        PARENT_DICT[obj.PARENT_METHOD],
                                        SURVIVOR_DICT[obj.SURVIVOR_METHOD],
                                        MUTATION_DICT[obj.MUTATION_METHOD],
                                        RECOMBINATION_DICT[obj.RECOMBINATION_METHOD],
                                        MANAGEMENT_DICT[obj.MANAGEMENT_METHOD]
                                    )

                                    # A dictionary which is to be pickled.
                                    to_save = {'Stats': obj,
                                               'Funcs': indices,
                                               'Runs': RUNS,
                                               'Generations': GENERATIONS}
                                    pickle_stats_obj(to_save, FILENUM, METHOD)

    for _ in range(20):
        result_matrix, matrix_dimensions = tester.iterate_tests(GENERATIONS, opt_fitness, true_optimum, 100)
        print('Matrix dimensions are: {}'.format(matrix_dimensions))
        if SAVE and FILENUM != 0: save_run()
