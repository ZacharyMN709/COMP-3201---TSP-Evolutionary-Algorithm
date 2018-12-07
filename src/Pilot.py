import os


def go_to_project_root():
    script_dir = os.path.dirname(__file__)
    path = os.path.join(script_dir, '..')
    os.chdir(path)
    print("Present working directory:", os.getcwd())


def current_dir():
    print("Present working directory:", os.getcwd())
