import os
import matplotlib.pyplot as plt
import pandas as pd
from math import pi, cos


class GraphingHelper:
    def __init__(self, fnum):
        self.long_names = ['Longitude (Range shifted)', 'Latitude (Range shifted)']
        self.short_names = ['Lat', 'Lon']
        self.cities = self.read_tsp_file(fnum)
        self.colour = [1.0, 0.0, 0.0]

    # region Display Methods
    def start_up_display(self):
        # TODO - Improve Graphs
        self.cities.plot.scatter(x=self.long_names[0], y=self.long_names[1], c=self.cities.index.get_values(), colormap='winter')
        plt.title('City Locations (Normalized to origin of 0)')

    def generation_display(self, generation, fitness, individual, title='Path at Generation {: <5}:   {:4.2f}'):
        # TODO - Improve Graphs
        x = self.cities[self.long_names[0]]
        y = self.cities[self.long_names[1]]

        self.cities.plot.scatter(x=self.long_names[0], y=self.long_names[1],  c=self.cities.index.get_values(), colormap='winter')

        for i in range(len(self.cities)):
            c1 = individual[i - 1]
            c2 = individual[i]
            per = 2 * pi * i / len(self.cities)
            red_mod = max(cos(per), 0) * 0.3
            bright_mod = -min(cos(per), 0) * 0.3
            plt.plot([x[c1], x[c2]], [y[c1], y[c2]], color=[1 - red_mod, bright_mod, bright_mod])
        plt.title(title.format(generation, fitness))
        plt.show()

    def alt_generation_display(self, generation, fitness, individual):
        # TODO - Improve Graphs
        x = self.cities[self.long_names[0]]
        y = self.cities[self.long_names[1]]

        for i in range(len(self.cities)):
            c1 = individual[i - 1]
            c2 = individual[i]
            per = pi * i / len(self.cities)
            red_mod = max(cos(per), 0) * 0.3
            bright_mod = -min(cos(per), 0) * 0.3
            plt.plot([x[c1], x[c2]], [y[c1], y[c2]], color=[1 - red_mod, bright_mod, bright_mod], marker='o')
        plt.title('Path at Generation {: <5}:   {:4.2f}'.format(generation, fitness))
        plt.show()
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
