import os
from src.Setups.TSP.FileLoader import LoadHelper
from src.EA_Methods.EAVarHelper import EAVarHelper
from src.EA_Methods.EA_Shell import EARunner
from src.Pilot import go_to_project_root, current_dir

go_to_project_root()
current_dir()

FILE_DICT = {0: '8-Queens',
             1: 'Sahara',
             2: 'Uruguay',
             3: 'Canada',
             4: 'Test World'}

METHOD_DICT = {0: 'Lists',
               1: 'Numpy',
               2: 'Arrays'}


FILENUM = 1
METHOD = 0
MULTITHREAD = False
RUNS = 1  # Number of times each combination is run.
GENERATIONS = 1
SAVE = True


file_data = LoadHelper(FILENUM)
