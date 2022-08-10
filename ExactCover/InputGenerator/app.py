from io import TextIOWrapper
import config_parser
import sudoku_gen
import os
import numpy as np
from datetime import datetime

def run():
    """Executes the input generator"""
    base, rate = config_parser.parse_config()
    sudoku = sudoku_gen.Sudoku(base, rate)
    root_dir = os.path.join(os.getcwd(), "Inputs")
    input_dir = os.path.join(root_dir, "Generated")

    dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = f"{base}_{int(rate*100)}_{dt_string}.txt"
    input_file_path = os.path.join(input_dir, filename)
    with open(input_file_path, "w", encoding='UTF-8') as input_file:
        input_file.write(str(sudoku))

    with open(input_file_path, "a", encoding='UTF-8') as input_file:
        print_matrix_a(input_file, sudoku)


def print_matrix_a(file_obj: TextIOWrapper, sudoku: sudoku_gen.Sudoku):
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
                file_obj.write(build_empty_cell_string(row_i, col_i, sudoku.base))
            else:
                file_obj.write(build_filled_cell_string(row_i, col_i, sudoku.base, int(cell)))
    

def build_filled_cell_string(row_i, col_i, base, symbol):
    n = base**4
    side = base*base
    out = ""

    # Init A same for each symbol
    list_A = np.zeros(n, dtype=int)
    list_A[row_i*side + col_i] = 1
    out += " ".join([str(i) for i in list_A]) + " "

    # Append portion B
    list_B = np.zeros(n, dtype=int)
    list_B[row_i*side + symbol-1] = 1
    out += " ".join([str(i) for i in list_B]) + " "

    # Append portion C
    list_C = np.zeros(n, dtype=int)
    list_C[col_i*side + symbol-1] = 1
    out += " ".join([str(i) for i in list_C]) + " "

    # Append portion D
    cur_box = (row_i//base)*base + (col_i//base)
    list_D = np.zeros(n, dtype=int)
    list_D[cur_box*side + symbol-1] = 1
    out += " ".join([str(i) for i in list_D]) + " -\n"

    return out


def build_empty_cell_string(row_i, col_i, base):
    n = base**4
    side = base*base
    out = ""

    # Init A same for each symbol
    list_A = np.zeros(n, dtype=int)
    list_A[row_i*side + col_i] = 1
    list_A_str = " ".join([str(i) for i in list_A])

    # Build remaining portion for each possible symbol
    for symbol in range(1, side+1):
        out += list_A_str + " "

        # Append portion B
        list_B = np.zeros(n, dtype=int)
        list_B[row_i*side + symbol-1] = 1
        out += " ".join([str(i) for i in list_B]) + " "

        # Append portion C
        list_C = np.zeros(n, dtype=int)
        list_C[col_i*side + symbol-1] = 1
        out += " ".join([str(i) for i in list_C]) + " "

        # Append portion D
        cur_box = (row_i//base)*base + (col_i//base)
        list_D = np.zeros(n, dtype=int)
        list_D[cur_box*side + symbol-1] = 1
        out += " ".join([str(i) for i in list_D]) + " -\n"

    return out


if __name__ == '__main__':
    run()