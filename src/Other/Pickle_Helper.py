"""
A module which helps package objects and save them for future use.
At present statistics are handled this way, but it is sub-optimal.
This modules is also used to save the MST, and memoized city distances.
"""

import os
import pickle
import time

FILE_DICT = {0: '8-Queens',
             1: 'Sahara',
             2: 'Uruguay',
             3: 'Canada',
             4: 'TestWorld'}

METHOD_DICT = {0: 'Lists',
               1: 'Numpy',
               2: 'Arrays'}


def get_timestamp():
    return time.strftime("%m-%d-%H-%M", time.gmtime())


def go_to_project_root():
    os.chdir(get_root_dir())


def get_root_dir():
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, '..', '..')


def move_dir(abs_dir_path):
    os.chdir(abs_dir_path)
    return abs_dir_path


# region Heuristic Handler
def pickle_euler_obj(to_save, file_num):
    abs_dir_path = get_euler_dir(file_num)
    move_dir(abs_dir_path)
    fname = get_euler_file(file_num)

    abs_file_path = os.path.join(abs_dir_path, fname)
    with open(abs_file_path, 'wb') as f:
        pickle.dump(to_save, f)
        print('Saved: {}'.format(fname))

    with open(abs_file_path + '-Fast', 'wb') as f:
        pickle.dump({'Euler': to_save['Euler']}, f)
        print('Saved: {}'.format(fname + '-Fast'))
    go_to_project_root()


def get_euler_dir(fnum):
    abs_dir_path = os.path.join(get_root_dir(), 'src', 'Setups', 'TSP', 'Inputs', FILE_DICT[fnum])
    return abs_dir_path


def get_euler_file(file_num):
    return 'TSP_{}_MST.txt'.format(FILE_DICT[file_num])


def get_pickled_euler(file_num, fast=False):
    # A dictionary which is to be pickled.
    # {'MST': MST,
    # 'Odd': ODD,
    # 'Euler': EUL}

    try:
        if fast:
            abs_dir_path = get_euler_dir(file_num)
            fname = get_euler_file(file_num) + '-Fast'
            with open(os.path.join(abs_dir_path, fname), 'rb') as f:
                euler_dict = pickle.load(f)
                print('Loaded: {}'.format(fname))
            return euler_dict
        else:
            abs_dir_path = get_euler_dir(file_num)
            fname = get_euler_file(file_num)
            with open(os.path.join(abs_dir_path, fname), 'rb') as f:
                euler_dict = pickle.load(f)
                print('Loaded: {}'.format(fname))
            return euler_dict
    except FileNotFoundError:
        return None

# endregion


# region Heuristic Handler
def pickle_memo_obj(to_save, file_num):
    abs_dir_path = get_memo_dir(file_num)
    move_dir(abs_dir_path)
    fname = get_memo_file(file_num)

    abs_file_path = os.path.join(abs_dir_path, fname)
    with open(abs_file_path, 'wb') as f:
        pickle.dump(to_save, f)
        print('Saved: {}'.format(fname))

    go_to_project_root()


def get_memo_dir(fnum):
    abs_dir_path = os.path.join(get_root_dir(), 'src', 'Setups', 'TSP', 'Inputs', FILE_DICT[fnum])
    return abs_dir_path


def get_memo_file(file_num):
    return 'TSP_{}_Dists.txt'.format(FILE_DICT[file_num])


def get_pickled_memo(file_num):
    # {'Locs': locs,
    #  'Dists', dists}
    try:
        abs_dir_path = get_euler_dir(file_num)
        fname = get_memo_file(file_num)
        with open(os.path.join(abs_dir_path, fname), 'rb') as f:
            euler_dict = pickle.load(f)
            print('Loaded: {}'.format(fname))
        return euler_dict
    except FileNotFoundError:
        return None
# endregion


FILENUM = 1  # 0: 8-Queens   1: Sahara   2: Uruguay   3: Canada   4: Test World
METHOD = 0  # 0: Lists   1: Numpy Arrays   2: C Arrays

if __name__ == '__main__':
    pass


