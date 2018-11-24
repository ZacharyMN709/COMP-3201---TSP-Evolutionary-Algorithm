import os
import matplotlib.pyplot as plt
import pandas as pd


class GraphingHelper:
    def __init__(self, fnum):
        self.cities = self.read_tsp_file(fnum)
        self.long_names = ['Longitude (Range shifted)', 'Latitude (Range shifted)']
        self.short_names = ['Lat', 'Lon']

    # region Display Methods
    def start_up_display(self):
        # TODO - Improve Graphs
        self.cities.plot.scatter(x=self.long_names[0], y=self.long_names[1], c=self.cities.index.get_values(), colormap='winter')
        plt.title('City Locations (Normalized to origin of 0)')

    def generation_display(self, population):
        # TODO - Improve Graphs
        self.cities.plot.scatter(x=self.long_names[0], y=self.long_names[1], c=self.cities.index.get_values(), colormap='winter')
        plt.title('City Locations (Normalized to origin of 0)')
    # endregion

    # region Initialization
    def read_tsp_file(self, fnum):
        if fnum == 1:
            fname = "TSP_WesternSahara_29.txt"
        elif fnum == 2:
            print('Warning! Takes approximately 1.5 seconds per decade')
            fname = "TSP_Uruguay_734.txt"
        elif fnum == 3:
            print('Warning! Takes approximately 45 seconds per decade')
            fname = "TSP_Canada_4663.txt"
        else:
            print('Warning! Invalid seletion. Defaulting to test')
            fname = "TSP_Testbed_10.txt"

        script_dir = os.path.dirname(__file__)  # absolute path for directory/folder this script is in
        abs_file_path = os.path.join(script_dir, 'TSP_Inputs', fname)

        # Uses indexing from 0, rather than 1, by skipping the first column in the data.
        cities = pd.read_csv(abs_file_path, usecols=[1, 2], header=None, delimiter=' ')
        cities.columns = self.short_names
        cities.index.names = ['City']
        # Translate and invert the x values, and translate the y values
        cities['Lat'] = cities['Lat'] - (cities['Lat'].min() + (cities['Lat'].max() - cities['Lat'].min()) / 2)
        cities['Lon'] = (cities['Lon'].min() + (cities['Lon'].max() - cities['Lon'].min()) / 2) - cities['Lon']
        cities.columns = self.long_names

        return cities
# endregion
