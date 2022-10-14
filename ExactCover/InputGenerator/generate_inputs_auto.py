import os
from InputGenerator import app as ig
from RandomGenerator import app as rg


ROWS = 50
MIN_COLUMNS = 10
MAX_COLUMNS = 50
COLUMNS = 10
MIN_ROWS = 10
MAX_ROWS = 50
MIN_RATE = 0.1
MAX_RATE = 0.9
COUNT = 10


def generate_random_rows(count, rows, min_columns, step):
    for i in range(count):
        generate_random_config(rows, min_columns + step * i)
        rg.run()




#def generate_random_columns(count, columns, min_rows, step):


#def generate_sudoku(count, base, min, step):


def generate_random_config(row, column):
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cfg_path = os.path.join(root, "ExactCover/RandomGenerator/parameters.cfg")
    cfg_file = open(cfg_path, "w")
    cfg_file.write("solution = 1\n")
    cfg_file.write("row = " + str(row) + "\n")
    cfg_file.write("column = " + str(column) + "\n")
    cfg_file.close()


def generate_sudoku_config(base, rate):
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cfg_path = os.path.join(root, "ExactCover/InputGenerator/parameters.cfg")
    cfg_file = open(cfg_path, "w")
    cfg_file.write("p = 0.0\n")
    cfg_file.write("groups = 4\n")
    cfg_file.write("base = " + str(base) + "\n")
    cfg_file.write("groups = " + str(rate) + "\n")
    cfg_file.close()


generate_random_rows(COUNT, 50, 10, 2)
