from src.Testing import EARunner


def import_modules(FILENUM=0, PANDAS=False):
    if not FILENUM:
        from src.EA_Methods.List_Rep import ParentSelectionMethods as PSM
        from src.EA_Methods.List_Rep import MutationMethods as MM
        from src.EA_Methods.List_Rep import RecombinationMethods as RM
        from src.EA_Methods.List_Rep import SurvivorSelectionMethods as SSM
        from src.Setups.EightQueens import EightQueen as DEF
    else:
        if PANDAS:
            from src.EA_Methods.Pandas_Rep import ParentSelectionMethods as PSM
            from src.EA_Methods.Pandas_Rep import MutationMethods as MM
            from src.EA_Methods.Pandas_Rep import RecombinationMethods as RM
            from src.EA_Methods.Pandas_Rep import SurvivorSelectionMethods as SSM
            from src.Setups.TSP import TSP_PDS as DEF
        else:
            from src.EA_Methods.List_Rep import ParentSelectionMethods as PSM
            from src.EA_Methods.List_Rep import MutationMethods as MM
            from src.EA_Methods.List_Rep import RecombinationMethods as RM
            from src.EA_Methods.List_Rep import SurvivorSelectionMethods as SSM
            from src.Setups.TSP import TSP_LST as DEF
    return PSM, RM, MM, SSM, DEF


def generate_algoritm(FILENUM=0, PANDAS=False):
    if not FILENUM:
        from src.Setups.EightQueens.EightQueen import random_initialization as initialize
        from src.Setups.EightQueens.EightQueen import fitness_8queen as eval_fitness
        genome_len = 8
    else:
        if PANDAS:
            from src.Setups.TSP.TSP_PDS import read_tsp_file as parse_file
            from src.Setups.TSP.TSP_PDS import random_initialization as initialize
            from src.Setups.TSP.TSP_PDS import euclidean_distance as eval_fitness
        else:
            from src.Setups.TSP.TSP_LST import read_tsp_file as parse_file
            from src.Setups.TSP.TSP_LST import random_initialization as initialize
            from src.Setups.TSP.TSP_LST import euclidean_distance as eval_fitness
        genome_len = parse_file(FILENUM)

    tester = EARunner(PSM, RM, MM, SSM, DEF)
    tester.set_funcs(genome_len, eval_fitness, initialize, None, None, None, None)
    return tester


if __name__ == '__main__':
    # File System Housekeeping
    import os
    import sys

    def go_to_project_root():
        path = os.path.join(os.getcwd(), '..')
        print(path)
        sys.path.append(path)
        os.chdir(path)
        print("Present working directory:", os.getcwd(), '\n')

    print("Present working directory:", os.getcwd(), '\n')

    FILENUM = 0  # 0: 8-Queens   1: Sahara   2: Uruguay   3: Canada   4: Test World
    PANDAS = False
    RUNS = 2  # Number of times each combination is run.
    GENERATIONS = 1000

    PSM, RM, MM, SSM, DEF = import_modules(FILENUM, PANDAS)

    POPULATION_METHODS = [('Random Initialization', DEF.random_initialization)]
    PARENT_METHODS = [('MPS', PSM.mps), ('Tourney', PSM.tournament)]
    RECOMBINATION_METHODS = [('Order Crossover', RM.order_crossover), ('PMX Crossover',RM.pmx_crossover)]
    MUTATION_METHODS = [('Swap', MM.permutation_swap), ('Insert', MM.permutation_insert), ('Inversion', MM.permutation_inversion)]
    SURVIVOR_METHODS = [('Mu + Lambda', SSM.mu_plus_lambda), ('Replace', SSM.replacement)]

    tester = generate_algoritm()
    tester.set_test_vars(POPULATION_METHODS, PARENT_METHODS, RECOMBINATION_METHODS, MUTATION_METHODS, SURVIVOR_METHODS, RUNS)

    if FILENUM:
        from src.Setups.TSP.TSP_Inputs.Optimums import get_best_path
        opt_fitness, opt_individual, true_optimum = get_best_path(FILENUM)
    else:
        opt_fitness, true_optimum = 16, True
        opt_individual = [5, 2, 6, 3, 0, 7, 1, 4]

    tester.iterate_tests(GENERATIONS, opt_fitness, true_optimum)



