import os
import pickle
import time
from src.StatsHolder import MergeError

FILE_DICT = {0: '8-Queens',
             1: 'Sahara',
             2: 'Uruguay',
             3: 'Canada',
             4: 'Test World'}

METHOD_DICT = {0: 'Lists',
               1: 'Numpy',
               2: 'Arrays'}

def get_timestamp():
    return time.strftime("%m-%d-%H-%M", time.gmtime())


def go_to_project_root():
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)
    print("Present working directory:", os.getcwd(), '\n')


def pickle_stats_obj(to_save, file_num, method_used):
    def move_dir():
        script_dir = os.path.dirname(__file__)  # absolute path for directory/folder this script is in

        # Get the right dir based on test parameters
        abs_dir_path = os.path.join(script_dir, 'Results', FILE_DICT.get(file_num, 4), METHOD_DICT.get(method_used, 0))

        # Change to that dir
        os.chdir(abs_dir_path)

        # Change to that dir
        os.chdir(abs_dir_path)
        print("Present working directory:", os.getcwd(), '\n')
        return abs_dir_path

    def backup_save():
        files_in_path = len([name for name in os.listdir('.') if os.path.isfile(name)])
        new_file_name = fname + '-' + str(files_in_path)
        new_file_path = os.path.join(abs_dir_path, new_file_name)
        with open(new_file_path, 'wb') as f:
            pickle.dump(to_save, f)
            print('Saved: {}'.format(new_file_name))

    # - - - -


    abs_dir_path = move_dir()
    indices = to_save['Funcs']
    fname = '{}{}{}{}{}{} G{}.txt'.format(indices[0], indices[1], indices[2], indices[3],
                                          indices[4], indices[5], to_save['Generations'])
    abs_file_path = os.path.join(abs_dir_path, fname)
    if os.path.isfile(abs_file_path):
        with open(abs_file_path, 'rb') as f:
            loaded = pickle.load(f)
        try:
            new_obj = loaded['Stats'] + to_save['Stats']
            loaded['Stats'] = new_obj
            loaded['Runs'] = loaded['Runs'] + to_save['Runs']
            try:
                with open(abs_file_path, 'wb') as f:
                    pickle.dump(loaded, f)
                    print('Saved: {}'.format(fname))
            except MemoryError:
                print('Memory Error Encountered. The two files are too big to be merged.')
                print('Saving new file as separate entity.')
                backup_save()
                return
        except MergeError:
            print('Merge Error Encountered. The two files are likely not the same.')
            print('Saving new file as separate entity.')
            backup_save()
    else:
        with open(abs_file_path, 'wb') as f:
            pickle.dump(to_save, f)
            print('Saved: {}'.format(fname))
    go_to_project_root()


def get_dir(filenum, method_used):
    script_dir = os.path.dirname(__file__)  # absolute path for directory/folder this script is in

    # Get the right dir based on test parameters
    abs_dir_path = os.path.join(script_dir, 'Results', FILE_DICT.get(filenum, 4), METHOD_DICT.get(method_used, 0))
    return abs_dir_path


def get_pickled_stats(file_name, file_num, method_used):
    # A dictionary which is to be pickled.
    # {'Stats': obj,
    # 'Funcs': indices,
    # 'Runs': RUNS,
    # 'Generations': GENERATIONS}

    abs_dir_path = get_dir(file_num, method_used)
    with open(os.path.join(abs_dir_path, file_name), 'rb') as f:
        stats_dict = pickle.load(f)
        print('Loaded: {}'.format(os.path.join(abs_dir_path, file_name)))

    return stats_dict


FILENUM = 1  # 0: 8-Queens   1: Sahara   2: Uruguay   3: Canada   4: Test World
METHOD = 0  # 0: Lists   1: Numpy Arrays   2: C Arrays

if __name__ == '__main__':

    loaded = get_pickled_stats('010210 G1.txt', 1, 0)

    print(loaded['Runs'])


