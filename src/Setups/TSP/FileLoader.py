import os
import csv
from src.Other.Pickle_Helper import get_pickled_memo, pickle_memo_obj
from array import array

# region Globals and Setters
MAX = False
FILE_DICT = {0: '8-Queens',
             1: 'Sahara',
             2: 'Uruguay',
             3: 'Canada',
             4: 'TestWorld'}


class LoadHelper:
    def __init__(self, filenum, load_from_disk=True, overwrite=False):
        self.filenum = filenum
        self.load = load_from_disk
        self.write = overwrite
        self.abs_dir_path = os.path.join(os.path.dirname(__file__), 'Inputs', FILE_DICT[filenum])
        self.abs_file_path = os.path.join(self.abs_dir_path, self.get_filename(filenum))
        self.locs = []
        self.dists = []
        self.genome_length = 0
        self.pickled_dists = dict()
        self.load_data()

    # region File Management
    def load_data(self):
        if self.load:
            self.pickled_dists = get_pickled_memo(self.filenum)
            if self.pickled_dists:
                self.locs = self.pickled_dists['Locs']
                self.genome_length = len(self.locs)
                self.dists = self.pickled_dists['Dists']
            else:
                self.read_csv()
        else:
            self.read_csv()

    def read_csv(self):
        with open(self.abs_file_path, 'r') as f:
            # Read and parse the file
            file = csv.reader(f, delimiter=' ')
            locations = [(float(i[1]), float(i[2])) for i in file]

            # Shift the numbers, so they are smaller and centered
            max_x, max_y = max(locations, key=lambda i: i[0])[0], max(locations, key=lambda i: i[1])[1]
            min_x, min_y = min(locations, key=lambda i: i[0])[0], min(locations, key=lambda i: i[1])[1]
            shift_x, shift_y = min_x + ((max_x - min_x) / 2), min_y + ((max_y - min_y) / 2)

            # NOTE: Locations are slightly odd. Original (x, y) mapped to normalized (-y, x) to produce
            # identifiable map of Canada.
            self.locs = [(shift_y - i[1], i[0] - shift_x) for i in locations]
            self.genome_length = len(self.locs)
            self.dists = \
                array('f', [[((self.locs[L1][0] - self.locs[L2][0])**2 + (self.locs[L1][1] - self.locs[L2][1])**2)**0.5
                             for L2 in range(L1 + 1, len(self.locs))] for L1 in range(len(self.locs))])

    def save_data(self):
        to_save = {'Locs': self.locs, 'Dists': self.dists}
        pickle_memo_obj(to_save, self.filenum)

    @staticmethod
    def get_filename(filenum):
        if filenum == 1:
            return "TSP_WesternSahara_29.txt"
        elif filenum == 2:
            return "TSP_Uruguay_734.txt"
        elif filenum == 3:
            return "TSP_Canada_4663.txt"
        else:
            print('Warning! Invalid selection. Defaulting to test')
            return "TSP_Testbed_10.txt"
    # endregion

    def get_simple_dist(self, i1, i2):
        return self.dists[i1][i2]

    def get_complex_dist(self, i1, i2):
        if i2 > i1: i1, i2 = i2, i1
        x_1 = (((self.genome_length-i1+1) * self.genome_length)/2) - (((self.genome_length+1) * self.genome_length)/2)
        x_0 = (self.genome_length - i2)
        return self.dists[x_1 + x_0]
