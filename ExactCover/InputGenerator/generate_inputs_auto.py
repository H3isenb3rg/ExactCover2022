import os
import app

MIN_RATE = 0.1
STEP = 0.9
COUNT = 10
BASE = 2


def generate_sudoku(count, base, min_rate, step):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    for i in range(count):
        generate_sudoku_config(base, min_rate + step * i)
        app.run(root)


def generate_sudoku_config(base, rate):
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cfg_path = os.path.join(root, "InputGenerator/parameters.cfg")
    cfg_file = open(cfg_path, "w")
    cfg_file.write("p = 0.0\n")
    cfg_file.write("groups = 4\n")
    cfg_file.write("base = " + str(base) + "\n")
    cfg_file.write("rate = " + str(rate) + "\n")
    cfg_file.close()


generate_sudoku(COUNT, BASE, MIN_RATE, STEP)
