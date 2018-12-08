from src.Setups.TSP.FileLoader import LoadHelper
from src.EACore.EAVarHelper import EAVarHelper
from src.EACore.EARunner import EARunner, EAFactory
from src.Setups.TSP.PopulationInitialization import PopulationInitializationGenerator
from src.Setups.TSP.FitnessEvaluator import FitnessHelperGenerator
from src.Setups.TSP.Inputs.Optimums import get_best_path

import multiprocessing as mp
import sqlite3 as sql
from datetime import datetime


FILE_DICT = {0: '8-Queens',
             1: 'Sahara',
             2: 'Uruguay',
             3: 'Canada',
             4: 'Test World'}

DATA_TYPE_DICT = {0: 'Lists',
                  1: 'Numpy',
                  2: 'Arrays'}


def single_run_setup():
    file_data = LoadHelper(FILENUM)
    var_helper = EAVarHelper(file_data.genome_length, False)
    pop_init_generator = PopulationInitializationGenerator(file_data.data, FILENUM)
    fitness_helper_generator = FitnessHelperGenerator(file_data.data.dists)
    fitness_helper = fitness_helper_generator.make_fit_helper(var_helper)
    pop_init_helper = pop_init_generator.make_pop_helper(var_helper, DATA_TYPE)

    db_name = "test_"
    for num in METHODS_TO_USE:
        db_name += str(num)
    db_name += datetime.now().strftime("_%H_%M_%S")

    # Create a runner instance for the algorithm
    ea = EARunner(var_helper, DATA_TYPE, fitness_helper, pop_init_helper)
    ea.set_params(METHODS_TO_USE[0], METHODS_TO_USE[1], METHODS_TO_USE[2], METHODS_TO_USE[3],
                  METHODS_TO_USE[4], METHODS_TO_USE[5], METHODS_TO_USE[6])

    ea.run(db_name, GENERATIONS, BEST_PATH, TRUE_OPT, PRINT_GENS, True)


def iterate_all_method_combos():
    factory = EAFactory(FILENUM, False)

    for i in range(1):
     for j in range(3):
      for k in range(3):
       for l in range(2):
        for m in range(4):
         for n in range(2):
          for o in range(5):
           db_name = str(i)+str(j)+str(k)+str(l)+str(m)+str(n)+str(o)
           ea = factory.make_ea_runner(DATA_TYPE, (i, j, k, l, m, n, o))
           ea.run(GENERATIONS, print_stats=True, report_rate=PRINT_GENS)


if __name__ == '__main__':
    FILENUM = 1
    DATA_TYPE = 0
    THREAD_COUNT = 1
    RUNS = 1  # Number of times each combination is run.
    GENERATIONS = 100
    PRINT_GENS = 100
    SAVE = False
    BEST_PATH, _, TRUE_OPT = get_best_path(FILENUM)
    METHODS_TO_USE = (0, 0, 2, 1, 2, 0, 3)
    '''
    Methods available in FitnessHelper:
      0:  Euclidean
    Methods available in PopulationInitializationHelper:
      0:  Random  1:  Cluster  2:  Euler
    Methods available in ParentSelectionHelper:
      0:  MPS  1:  Tourney  2:  Random
    Methods available in RecombinationHelper:
      0:  Order Crossover  1:  PMX Crossover
    Methods available in MutatorHelper:
      0:  Swap  1:  Insert  2:  Inversion  3:  Shift
    Methods available in SurvivorSelectionHelper:
      0:  Mu + Lambda  1:  Replace
    Methods available in PopulationManagementHelper:
      0:  None  1:  Annealing  2:  Entropy  3:  Oroborous  4:  Engineering
    '''

    for x in range(3):
        DATA_TYPE = x
        iterate_all_method_combos()
