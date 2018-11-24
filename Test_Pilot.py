from src.Testing import EATester
import os
import sys
import pickle
import time


def get_timestamp():
    return time.strftime("%m-%d %H:%M", time.gmtime())


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


def generate_algoritm(FILENUM=0, MODULE=0):
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

    tester = EATester(PSM, RM, MM, SSM, DEF, PMM)
    tester.set_funcs(genome_len, eval_fitness, initialize, None, None, None, None, None)
    return tester


def go_to_project_root():
    path = os.path.join(os.getcwd(), '..')
    print(path)
    sys.path.append(path)
    os.chdir(path)
    print("Present working directory:", os.getcwd(), '\n')


if __name__ == '__main__':
    print("Present working directory:", os.getcwd(), '\n')

    FILE_DICT = {0: '8-Queens',
                 1: 'Sahara',
                 2: 'Uruguay',
                 3: 'Canada',
                 4: 'Test World'}

    METHOD_DICT = {0: 'Lists',
                   1: 'NumpyV1',
                   2: 'NumpyV2'}

    FILENUM = 2  # 0: 8-Queens   1: Sahara   2: Uruguay   3: Canada   4: Test World
    METHOD = 0  # 0: Lists   1: Numpy Arrays   2: Numpy Arrays V2
    RUNS = 10  # Number of times each combination is run.
    GENERATIONS = 2000
    SAVE = True

    PSM, RM, MM, SSM, DEF, PMM = import_modules(FILENUM, METHOD)

    POPULATION_METHODS = [('Random Initialization', DEF.random_initialization), ('Cluster Initialization', DEF.heurisitic_cluster_initialization)]
    PARENT_METHODS = [('MPS', PSM.mps), ('Tourney', PSM.tournament), ('Random', PSM.random_uniform)]
    RECOMBINATION_METHODS = [('Order Crossover', RM.order_crossover), ('PMX Crossover', RM.pmx_crossover)]
    MUTATION_METHODS = [('Swap', MM.permutation_swap), ('Insert', MM.permutation_insert), ('Inversion', MM.permutation_inversion)]
    SURVIVOR_METHODS = [('Mu + Lambda', SSM.mu_plus_lambda), ('Replace', SSM.replacement)]
    MANAGEMENT_METHODS = [('None', PMM.static_return), ('Annealing', PMM.metallurgic_annealing), ('Entropy', PMM.metallurgic_annealing), ('Oroborous', PMM.metallurgic_annealing)]

    tester = generate_algoritm(FILENUM, METHOD)
    tester.set_test_vars(RUNS, POPULATION_METHODS[:], PARENT_METHODS[1:2], RECOMBINATION_METHODS[1:2],
                         MUTATION_METHODS[2:3], SURVIVOR_METHODS[0:1], MANAGEMENT_METHODS[:])

    if FILENUM:
        from src.Setups.TSP.TSP_Inputs.Optimums import get_best_path
        opt_fitness, opt_individual, true_optimum = get_best_path(FILENUM)
    else:
        opt_fitness, true_optimum = 16, True
        opt_individual = [5, 2, 6, 3, 0, 7, 1, 4]

    result_matrix = tester.iterate_tests(GENERATIONS, opt_fitness, true_optimum, 20)

    if SAVE:
        fname = '{}_{} R{}-G{}, {}'.format(
            FILE_DICT.get(FILENUM, '?'), METHOD_DICT.get(METHOD, '?'), RUNS, GENERATIONS, get_timestamp())
        with open(fname, 'wb') as f:
            pickle.dump(result_matrix, f)



