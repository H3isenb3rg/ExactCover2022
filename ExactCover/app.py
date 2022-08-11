from genericpath import isdir
import os
from Parser import parser
from BaseAlg import app as baseApp

input_root = os.path.join(os.getcwd(), "Inputs")

def execute_files(root_path):
    """Executes the exact cover algorithm for all files inside the 'Inputs' folder

    Args:
        root_path (string): path to the 'Inputs' folder
    """
    for file in os.listdir(root_path):
        cur_file_path = os.path.join(root_path, file)
        if os.path.isdir(cur_file_path):
            execute_files(cur_file_path)
        else:
            matrix, size_m = parser.parse_file(cur_file_path)
            cov, matrix_b = baseApp.ec(matrix, size_m)
            

execute_files(input_root)