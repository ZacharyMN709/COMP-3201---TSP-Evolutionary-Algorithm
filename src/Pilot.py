import os


def go_to_project_root():
    script_dir = os.path.dirname(__file__)
    path = os.path.join(script_dir, '..')
    print(path)
    os.chdir(path)
    print("Present working directory:", os.getcwd(), '\n')


def current_dir():
    print("Present working directory:", os.getcwd(), '\n')
