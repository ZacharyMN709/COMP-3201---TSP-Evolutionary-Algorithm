from src.Setups.TSP.FileLoader import LoadHelper
from src.EACore.EAVarHelper import EAVarHelper
from src.EACore.EARunner import EARunner
from src.Setups.TSP.EAFactory import EAFactory
from src.Setups.TSP.PopulationInitialization import PopulationInitializationGenerator
from src.Setups.TSP.FitnessEvaluator import FitnessHelperGenerator
from src.Setups.TSP.Inputs.Optimums import get_best_path

from datetime import datetime
import json


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

    ea.run(db_name, GENERATIONS, BEST_PATH, TRUE_OPT, REPORT_RATE, True)


def iterate_all_method_combos():
    factory = EAFactory(FILENUM, False)
    for x in range(3):
     for i in range(1):
      for j in range(3):
       for k in range(3):
        for l in range(2):
         for m in range(4):
          for n in range(2):
           for o in range(5):
            if USE_DB:
                db_name = str(x)+str(i)+str(j)+str(k)+str(l)+str(m)+str(n)+str(o)
            else:
                db_name = None

            ea = factory.make_ea_runner(DATA_TYPE, (i, j, k, l, m, n, o))
            ea.run(GENERATIONS, db_name=db_name, print_stats=PRINT_STATS, report_rate=REPORT_RATE)


if __name__ == '__main__':
    with open("config.json", "r") as file:
        config = json.loads(file.read())

    DB_NAME = config["db_name"]
    TEST_ALL = config["test_all"]
    FILENUM = config["data_set"]
    DATA_TYPE = config["data_type"]
    RUNS = config["runs"]  # Number of times each combination is run.
    GENERATIONS = config["generation_limit"]
    REPORT_RATE = config["report_rate"]
    BEST_PATH, _, TRUE_OPT = get_best_path(FILENUM)
    METHODS_TO_USE = config["methods"]
    PRINT_STATS = config["print_stats"]
    USE_DB = config["use_db"]
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

    if TEST_ALL:
        iterate_all_method_combos()
    else:
        factory = EAFactory(FILENUM, False)
        ea = factory.make_ea_runner(DATA_TYPE, METHODS_TO_USE)
        if not USE_DB:
            DB_NAME = None
        ea.run(GENERATIONS, db_name=DB_NAME, print_stats=PRINT_STATS, report_rate=REPORT_RATE)
