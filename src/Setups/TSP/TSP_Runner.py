import os
from src.Setups.TSP.FileLoader import LoadHelper
from src.EA_Methods.EAVarHelper import EAVarHelper
from src.EA_Methods.EA_Shell import EARunner
from src.Pilot import go_to_project_root, current_dir
from src.Setups.TSP.PopulationInitialization import PopulationInitializationGenerator
from src.Setups.TSP.FitnessEvaluator import FitnessHelper

go_to_project_root()
current_dir()

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
    SAVE = True

    file_data = LoadHelper(FILENUM)
    var_helper = EAVarHelper(file_data.genome_length, False)
    pop_init_generator = PopulationInitializationGenerator(file_data.data, FILENUM)
    fitness_helper = FitnessHelper(var_helper, DATA_TYPE, file_data.data.dists)
    pop_init_helper = pop_init_generator.make_pop_helper(var_helper, DATA_TYPE)

    ea = EARunner(var_helper, DATA_TYPE, fitness_helper, pop_init_helper)


if __name__ == '__main__':
    single_run_setup()
