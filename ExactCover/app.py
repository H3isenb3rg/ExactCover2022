from genericpath import isdir
import os
from Parser import parser
# from BaseAlg import exactcover_base as baseAlg
import exactcover_plus as plusAlg

input_root = os.path.join(os.getcwd(), "Inputs")
output_root = os.path.join(os.getcwd(), "Outputs")

def execute_files(root_path):
    """Executes the exact cover algorithm for all files inside the 'Inputs' folder

    Args:
        root_path (string): path to the 'Inputs' folder
    """
    for file in os.listdir(root_path):
        print(file)
        cur_file_path = os.path.join(root_path, file)
        out_file_path = os.path.join(output_root, file)
        if os.path.isdir(cur_file_path):
            execute_files(cur_file_path)
        else:
            matrix, m, bin_matrix = parser.parse_file(cur_file_path)
            # ec_base = baseAlg.ExactCoverBase(matrix, len(m))
            # ec_base.ec()
            ec_plus = plusAlg.ExactCoverPlus(bin_matrix, len(m), out_file_path)
            ec_plus.ec()

execute_files(input_root)