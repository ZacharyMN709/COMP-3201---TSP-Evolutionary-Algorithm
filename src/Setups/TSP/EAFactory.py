from src.Setups.TSP.FileLoader import LoadHelper
from src.Setups.TSP.PopulationInitialization import PopulationInitializationGenerator
from src.Setups.TSP.FitnessEvaluator import FitnessHelperGenerator
from src.EACore.EAVarHelper import EAVarHelper
from src.EACore.EARunner import EARunner


class EAFactory:
    def __init__(self, filenum, maximize):
        self.filenum = filenum
        self.maximize = maximize
        self.file_data = LoadHelper(filenum)
        self.data = self.file_data.data
        self.genome_length = self.file_data.genome_length
        self.pop_generator = PopulationInitializationGenerator(self.data, filenum)
        self.fit_generator = FitnessHelperGenerator(self.data.dists)

    def make_ea_runner(self, data_type, params):
        var_helper = EAVarHelper(self.genome_length, self.maximize)
        fitness_helper = self.fit_generator.make_fit_helper(var_helper)
        pop_init_helper = self.pop_generator.make_pop_helper(var_helper, data_type)
        ea = EARunner(var_helper, data_type, fitness_helper, pop_init_helper)
        ea.set_params(params[0], params[1], params[2], params[3], params[4], params[5], params[6])
        return ea

    def change_file(self, filenum):
        self.filenum = filenum
        self.file_data = LoadHelper(filenum)
        self.data = self.file_data.data
        self.genome_length = self.file_data.genome_length
        self.pop_generator = PopulationInitializationGenerator(self.data, filenum)
        self.fit_generator = FitnessHelperGenerator(self.data.dists)
