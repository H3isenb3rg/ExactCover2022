from genericpath import isdir
import os
from Parser import parser
import exactcover_base as baseAlg
import exactcover_plus as plusAlg
import time
import matrix_a as ma

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
        out_file_path = os.path.join(output_root, "ec_" + file)
        ecp_out_file_path = os.path.join(output_root, "ecp_" + file)
        if os.path.isdir(cur_file_path):
            execute_files(cur_file_path)
        else:
            matrix, m = parser.parse_file(cur_file_path)
            matrix_a = ma.MatrixA(cur_file_path, 100)
            #ec_base = baseAlg.ExactCoverBase(matrix, m, out_file_path)
            #ec_base.ec()
            ec_plus = plusAlg.ExactCoverPlus(matrix_a, len(m), ecp_out_file_path)
            ec_plus.ec()


execute_files(input_root)

