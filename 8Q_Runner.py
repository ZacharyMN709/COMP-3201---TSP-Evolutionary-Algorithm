from src.EACore.EAVarHelper import EAVarHelper
from src.EACore.EARunner import EARunner
from src.Setups.EightQueens.PopulationInitialization import PopulationInitializationHelper
from src.Setups.EightQueens.FitnessEvaluator import FitnessHelper
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
    var_helper = EAVarHelper(8, MAXIMIZE)
    fitness_helper = FitnessHelper(var_helper)
    pop_init_helper = PopulationInitializationHelper(var_helper, DATA_TYPE)
    ea = EARunner(var_helper, DATA_TYPE, fitness_helper, pop_init_helper)
    ea.set_params(METHODS_TO_USE[0], METHODS_TO_USE[1], METHODS_TO_USE[2], METHODS_TO_USE[3],
                  METHODS_TO_USE[4], METHODS_TO_USE[5], METHODS_TO_USE[6])
    print(ea.is_runnable())
    ea.run(GENERATIONS, true_opt=TRUE_OPT, known_optimum=BEST_PATH, print_stats=PRINT_STATS, report_rate=REPORT_RATE)


if __name__ == '__main__':
    with open("8Q-config.json", "r") as file:
        config = json.loads(file.read())

    MAXIMIZE = config["maximization"]
    DATA_TYPE = config["data_type"]
    RUNS = config["runs"]  # Number of times each combination is run.
    GENERATIONS = config["generation_limit"]
    REPORT_RATE = config["report_rate"]
    METHODS_TO_USE = config["methods"]
    PRINT_STATS = config["print_stats"]
    USE_DB = False
    BEST_PATH = 16 if METHODS_TO_USE[0] == 1 else 28
    TRUE_OPT = True
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
    single_run_setup()
