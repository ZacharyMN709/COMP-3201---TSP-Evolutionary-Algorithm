from src.Setups.TSP.FileLoader import LoadHelper
from src.EA_Methods.EAVarHelper import EAVarHelper
from src.EA_Methods.EA_Shell import EARunner
from src.Pilot import go_to_project_root, current_dir
from src.Setups.TSP.PopulationInitialization import PopulationInitializationGenerator
from src.Setups.TSP.FitnessEvaluator import FitnessHelper
from src.Setups.TSP.Inputs.Optimums import get_best_path

go_to_project_root()

FILE_DICT = {0: '8-Queens',
             1: 'Sahara',
             2: 'Uruguay',
             3: 'Canada',
             4: 'Test World'}

DATA_TYPE_DICT = {0: 'Lists',
                  1: 'Numpy',
                  2: 'Arrays'}


def single_run_setup():
    FILENUM = 1
    DATA_TYPE = 0
    MULTITHREAD = False
    RUNS = 1  # Number of times each combination is run.
    GENERATIONS = 1
    PRINT_GENS = 1
    SAVE = True
    BEST_PATH, _, TRUE_OPT = get_best_path(FILENUM)

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
    METHODS_TO_USE = (0, 2, 1, 1, 2, 0, 4)

    file_data = LoadHelper(FILENUM)
    var_helper = EAVarHelper(file_data.genome_length, False)
    pop_init_generator = PopulationInitializationGenerator(file_data.data, FILENUM)
    fitness_helper = FitnessHelper(var_helper, DATA_TYPE, file_data.data.dists)
    pop_init_helper = pop_init_generator.make_pop_helper(var_helper, DATA_TYPE)

    ea = EARunner(var_helper, DATA_TYPE, fitness_helper, pop_init_helper)
    ea.set_params(METHODS_TO_USE[0], METHODS_TO_USE[1], METHODS_TO_USE[2], METHODS_TO_USE[3],
                  METHODS_TO_USE[4], METHODS_TO_USE[5], METHODS_TO_USE[6])

    ea.run(GENERATIONS, 0, BEST_PATH, TRUE_OPT, PRINT_GENS)


if __name__ == '__main__':
    single_run_setup()
