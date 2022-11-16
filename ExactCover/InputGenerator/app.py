from io import TextIOWrapper
from xmlrpc.client import boolean
import config_parser
import sudoku_gen
import os
import numpy as np
import random
from datetime import datetime


def run(root_dir: str):
    """Executes the input generator"""
    base, rate, p, groups = config_parser.parse_config()
    sudoku = sudoku_gen.Sudoku(base, rate, p)
    input_dir = os.path.join(os.path.join(root_dir, "Inputs"), "Sudoku")
    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)

    dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = f"{base}_{int(rate*100)}_{int(p*100)}_{groups}_{dt_string}.txt"
    input_file_path = os.path.join(input_dir, filename)
    with open(input_file_path, "w", encoding='UTF-8') as input_file:
        input_file.write(str(sudoku))

    with open(input_file_path, "a", encoding='UTF-8') as input_file:
        print_matrix_a(input_file, sudoku, groups)


def print_matrix_a(file_obj: TextIOWrapper, sudoku: sudoku_gen.Sudoku, groups: int = 4):
    # Matrix columns description
    # A) side^2 columns -> side^2 different cells and will be used to indicate that a symbol has been placed in a particular cell.
    # B) side^2 columns -> labeled by the base^2 rows and base^2 possible symbols
    # C) side^2 columns -> labeled by the base^2 columns and base^2 possible symbols.
    # D) side^2 columns -> labeled by the base^2 boxes and base^2 possible symbols.
    side = sudoku.base * sudoku.base

    for row_i, row in enumerate(sudoku.base_board):
        print(f'Building matrix A: Row={row_i+1}/{side}', end='\r')
        for col_i, cell in enumerate(row):
            if cell == 0:
                file_obj.write(build_empty_cell_string(row_i, col_i, sudoku.base, sudoku.p, True, groups))
            else:
                file_obj.write(build_filled_cell_string(row_i, col_i, sudoku.base, int(cell), True, groups))
    

def build_filled_cell_string(row_i, col_i, base, symbol, separator: bool = False, groups: int = 4):
    n = base**4
    side = base*base
    out = ""

    # Init A same for each symbol
    list_A = np.zeros(n, dtype=int)
    list_A[row_i*side + col_i] = 1
    out += " ".join([str(i) for i in list_A])

    if groups < 2:
        out += " -\n"
        return out
    out+=(" | " if separator else " ")

    # Append portion B
    list_B = np.zeros(n, dtype=int)
    list_B[row_i*side + symbol-1] = 1
    out += " ".join([str(i) for i in list_B])

    if groups < 3:
        out += " -\n"
        return out
    out+=(" | " if separator else " ")

    # Append portion C
    list_C = np.zeros(n, dtype=int)
    list_C[col_i*side + symbol-1] = 1
    out += " ".join([str(i) for i in list_C])

    if groups < 4:
        out += " -\n"
        return out
    out+=(" | " if separator else " ")

    # Append portion D
    cur_box = (row_i//base)*base + (col_i//base)
    list_D = np.zeros(n, dtype=int)
    list_D[cur_box*side + symbol-1] = 1
    out += " ".join([str(i) for i in list_D]) + " -\n"

    return out


def build_empty_cell_string(row_i, col_i, base, p: float = 0, separator: bool = False, groups: int = 4):
    n = base**4
    side = base*base
    out = ""

    # Init A same for each symbol
    list_A = np.zeros(n, dtype=int)
    list_A[row_i*side + col_i] = 1

    # Build remaining portion for each possible symbol
    for symbol in range(1, side+1):
        # Append portion A
        out += " ".join(["1" if i==0 and random.random()<p else str(i) for i in list_A])

        if groups < 2:
            out += " -\n"
            continue
        out+=(" | " if separator else " ")

        # Append portion B
        list_B = np.zeros(n, dtype=int)
        list_B[row_i*side + symbol-1] = 1
        out += " ".join(["1" if i==0 and random.random()<p else str(i) for i in list_B])

        if groups < 3:
            out += " -\n"
            continue
        out+=(" | " if separator else " ")

        # Append portion C
        list_C = np.zeros(n, dtype=int)
        list_C[col_i*side + symbol-1] = 1
        out += " ".join(["1" if i==0 and random.random()<p else str(i) for i in list_C])

        if groups < 4:
            out += " -\n"
            continue
        out+=(" | " if separator else " ")

        # Append portion D
        cur_box = (row_i//base)*base + (col_i//base)
        list_D = np.zeros(n, dtype=int)
        list_D[cur_box*side + symbol-1] = 1
        out += " ".join(["1" if i==0 and random.random()<p else str(i) for i in list_D]) + " -\n"

    return out


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    run(root)