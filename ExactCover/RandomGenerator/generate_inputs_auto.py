import os
import app

ROWS = 40
MIN_COLUMNS = 10
STEP_COLUMNS = 2

COLUMNS = 20
MIN_ROWS = 30
STEP_ROWS = 1

COUNT = 10


def generate_random_rows(count, rows, min_columns, step):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    for i in range(count):
        generate_random_config(rows, min_columns + step * i)
        app.run(root)


def generate_random_columns(count, columns, min_rows, step):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    for i in range(count):
        generate_random_config(min_rows + step * i, columns)
        app.run(root)


def generate_random_config(row, column):
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cfg_path = os.path.join(root, "RandomGenerator/parameters.cfg")
    cfg_file = open(cfg_path, "w")
    cfg_file.write("solution = 1\n")
    cfg_file.write("row = " + str(row) + "\n")
    cfg_file.write("column = " + str(column) + "\n")
    cfg_file.close()


#generate_random_rows(COUNT, ROWS, MIN_COLUMNS, STEP_COLUMNS)
generate_random_columns(COUNT, COLUMNS, MIN_ROWS, STEP_ROWS)
