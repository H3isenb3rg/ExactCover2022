from io import TextIOWrapper
import os
from datetime import datetime
from ExactCover.RandomGenerator import random_gen, config_parser


def run(root_dir: str):
    row, column, solution = config_parser.parse_config()
    matrix_a = random_gen.gen_matrix(row, column, solution)
    input_dir = os.path.join(os.path.join(root_dir, "Inputs"), "Random")
    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)
    dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = f"{row}x{column}_{dt_string}.txt" #da sistemare
    input_file_path = os.path.join(input_dir, filename)
    with open(input_file_path, "a", encoding='UTF-8') as input_file:
        print_matrix_a(input_file, matrix_a)


def print_matrix_a(file_obj: TextIOWrapper, matrix_a):
    for row in range(len(matrix_a)):
        for column in range(len(matrix_a[0])):
            if matrix_a[row][column] == 0:
                file_obj.write('0 ')
            else:
                file_obj.write('1 ')
        file_obj.write('- \n')


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    run(root)

