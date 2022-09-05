import os
from Parser import parser
import exactcover_base as baseAlg
import exactcover_plus as plusAlg
import matrix_a as ma


def execute_files(root_path: str, output_root: str):
    """Executes the exact cover algorithm for all files inside the 'Inputs' folder

    Args:
        root_path (string): path to the 'Inputs' folder
    """
    for file in os.listdir(root_path):
        print(file + " "*10)
        cur_file_path = os.path.join(root_path, file)
        out_file_path = os.path.join(output_root, "ec_" + file)
        ecp_out_file_path = os.path.join(output_root, "ecp_" + file)
        if os.path.isdir(cur_file_path):
            execute_files(cur_file_path, output_root)
        else:
            matrix, m = parser.parse_file(cur_file_path)
            matrix_a = ma.MatrixA(cur_file_path, 100)
            ec_base = baseAlg.ExactCoverBase(matrix, m, out_file_path)
            ec_base.ec()
            ec_plus = plusAlg.ExactCoverPlus(matrix_a, len(m), ecp_out_file_path)
            ec_plus.ec()
            if "Generated" in cur_file_path:
                print("    " + compare_results(ec_base, ec_plus))

def compare_results(baseEC: baseAlg.ExactCoverBase, plusEC: plusAlg.ExactCoverPlus) -> str:
    if baseEC.et > plusEC.et:
        rate = round(baseEC.et/plusEC.et, 2)
        return f"Plus alg {rate} times faster than Base alg"
    elif plusEC.et > baseEC.et:
        rate = round(plusEC.et/baseEC.et, 2)
        return f"Base alg {rate} times faster than Plus alg"
    else:
        return "Both alg executed in similar times"
        

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    input_root = os.path.join(root, "Inputs")
    output_path = os.path.join(root, "Outputs")
    execute_files(input_root, output_path)

