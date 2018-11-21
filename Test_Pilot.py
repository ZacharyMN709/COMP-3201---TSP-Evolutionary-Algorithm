from src.Testing import EARunner
import os
import sys


def import_modules(FILENUM=0, MODULE=0):
    if not FILENUM:
        from src.EA_Methods.List_Rep import ParentSelectionMethods as PSM
        from src.EA_Methods.List_Rep import MutationMethods as MM
        from src.EA_Methods.List_Rep import RecombinationMethods as RM
        from src.EA_Methods.List_Rep import SurvivorSelectionMethods as SSM
        from src.Setups.EightQueens import EightQueen as DEF
    else:
        if MODULE == 2:
            from src.EA_Methods.Pandas_Rep import ParentSelectionMethods as PSM
            from src.EA_Methods.Pandas_Rep import MutationMethods as MM
            from src.EA_Methods.Pandas_Rep import RecombinationMethods as RM
            from src.EA_Methods.Pandas_Rep import SurvivorSelectionMethods as SSM
            from src.Setups.TSP import TSP_PDS as DEF
        elif MODULE == 1:
            from src.EA_Methods.Numpy_Rep import ParentSelectionMethods as PSM
            from src.EA_Methods.Numpy_Rep import MutationMethods as MM
            from src.EA_Methods.Numpy_Rep import RecombinationMethods as RM
            from src.EA_Methods.Numpy_Rep import SurvivorSelectionMethods as SSM
            from src.Setups.TSP import TSP_NPY as DEF
        else:
            from src.EA_Methods.List_Rep import ParentSelectionMethods as PSM
            from src.EA_Methods.List_Rep import MutationMethods as MM
            from src.EA_Methods.List_Rep import RecombinationMethods as RM
            from src.EA_Methods.List_Rep import SurvivorSelectionMethods as SSM
            from src.Setups.TSP import TSP_LST as DEF
    return PSM, RM, MM, SSM, DEF


def generate_algoritm(FILENUM=0, MODULE=0):
    if not FILENUM:
        from src.Setups.EightQueens.EightQueen import random_initialization as initialize
        from src.Setups.EightQueens.EightQueen import fitness_8queen as eval_fitness
        genome_len = 8
    else:
        if MODULE == 2:
            from src.Setups.TSP.TSP_PDS import read_tsp_file as parse_file
            from src.Setups.TSP.TSP_PDS import random_initialization as initialize
            from src.Setups.TSP.TSP_PDS import euclidean_distance as eval_fitness
        elif MODULE == 1:
            from src.Setups.TSP.TSP_NPY import read_tsp_file as parse_file
            from src.Setups.TSP.TSP_NPY import random_initialization as initialize
            from src.Setups.TSP.TSP_NPY import euclidean_distance as eval_fitness
        else:
            from src.Setups.TSP.TSP_LST import read_tsp_file as parse_file
            from src.Setups.TSP.TSP_LST import random_initialization as initialize
            from src.Setups.TSP.TSP_LST import euclidean_distance as eval_fitness
        genome_len = parse_file(FILENUM)

    tester = EARunner(PSM, RM, MM, SSM, DEF)
    tester.set_funcs(genome_len, eval_fitness, initialize, None, None, None, None)
    return tester


def go_to_project_root():
    path = os.path.join(os.getcwd(), '..')
    print(path)
    sys.path.append(path)
    os.chdir(path)
    print("Present working directory:", os.getcwd(), '\n')


if __name__ == '__main__':
    print("Present working directory:", os.getcwd(), '\n')

    FILENUM = 1  # 0: 8-Queens   1: Sahara   2: Uruguay   3: Canada   4: Test World
    METHOD = 0  # 0: Lists   1: Numpy Arrays   2: Pandas Dataframes
    RUNS = 5  # Number of times each combination is run.
    GENERATIONS = 500

    PSM, RM, MM, SSM, DEF = import_modules(FILENUM, METHOD)

    POPULATION_METHODS = [('Random Initialization', DEF.random_initialization)]
    PARENT_METHODS = [('MPS', PSM.mps), ('Tourney', PSM.tournament)]
    RECOMBINATION_METHODS = [('Order Crossover', RM.order_crossover), ('PMX Crossover', RM.pmx_crossover)]
    MUTATION_METHODS = [('Swap', MM.permutation_swap), ('Insert', MM.permutation_insert), ('Inversion', MM.permutation_inversion)]
    SURVIVOR_METHODS = [('Mu + Lambda', SSM.mu_plus_lambda), ('Replace', SSM.replacement)]

    tester = generate_algoritm(FILENUM, METHOD)
    tester.set_test_vars(POPULATION_METHODS, PARENT_METHODS[1:], RECOMBINATION_METHODS[1:],
                         MUTATION_METHODS[2:], SURVIVOR_METHODS[1:], RUNS)

    if FILENUM:
        from src.Setups.TSP.TSP_Inputs.Optimums import get_best_path
        opt_fitness, opt_individual, true_optimum = get_best_path(FILENUM)
    else:
        opt_fitness, true_optimum = 16, True
        opt_individual = [5, 2, 6, 3, 0, 7, 1, 4]

    tester.iterate_tests(GENERATIONS, opt_fitness, true_optimum, 25)



