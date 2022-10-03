import os
from Parser import parser
import exactcover as ec
import matrix_a as ma
import linecache
import filecmp
import cov


def execute_files(root_path: str, output_root: str):
    """Executes the exact cover algorithm for all files inside the 'Inputs' folder

    Args:
        root_path (string): path to the 'Inputs' folder
    """
    for file in os.listdir(root_path):
        print(file + " "*10)
        cur_file_path = os.path.join(root_path, file)
        if os.path.isdir(cur_file_path):
            execute_files(cur_file_path, output_root)
        else:
            m = parser.parse_file(cur_file_path)
            matrix_a = get_matrix_a(cur_file_path, 250)
            ec_base = ec.ExactCover(matrix_a, m, file, output_root)
            ec_base.ec()
            ec_plus = ec.ExactCoverPlus(matrix_a, m, file, output_root)
            ec_plus.ec()
            compare_results_file(ec_base.cov, ec_plus.cov)

            if "Sudoku" in cur_file_path or "Random" in cur_file_path:
                print("    " + compare_results(ec_base, ec_plus))

def compare_results_file(cov_base: cov.Cover, cov_plus: cov.Cover):
    comparison = filecmp.cmp(cov_base.results_path, cov_plus.results_path, shallow=False)
    comment = f"Corresponding Results: {comparison}"

    cov_base.write_comment(comment)
    cov_plus.write_comment(comment)

    return comparison

def get_matrix_a(cur_file_path: str, chunk_size: int = None):
    raw_line = linecache.getline(cur_file_path, 1)
    if ";;; Sudoku" in raw_line:
        return ma.MatrixA_Sudoku(cur_file_path, chunk_size)
    else:
        return ma.MatrixA(cur_file_path, chunk_size)

def compare_results(baseEC: ec.ExactCover, plusEC: ec.ExactCoverPlus) -> str:
    if baseEC.time > plusEC.time:
        rate = round(baseEC.time/plusEC.time, 2)
        return f"Plus alg {rate} times faster than Base alg"
    elif plusEC.time > baseEC.time:
        rate = round(plusEC.time/baseEC.time, 2)
        return f"Base alg {rate} times faster than Plus alg"
    else:
        return "Both alg executed in similar times"

# deprecated
#def time_ec(ec_object: ec.ExactCover):
#    ec_object.ec(False)

# deprecated
#def time_ec_examples(input_path: str, out_path: str, timeit_number: int = 100000):
#    for file in os.listdir(input_path):
#        full_path = os.path.join(input_path, file)
#        if not os.path.isdir(full_path):
#            print(file + " "*10)
#            out_file_path = os.path.join(out_path, f"ec_{file}")
#            ecp_out_file_path = os.path.join(out_path, f"ecp_{file}")
#            m = parser.parse_file(full_path)
#            matrix_a = get_matrix_a(full_path, 250)
#
#            ec_base = ec.ExactCover(matrix_a, m, out_file_path)
#            time_result = timeit.timeit("ec_base.ec(False)", number=timeit_number)
#            ec_base.cov.write_comment(f"Average time over {timeit_number} executions -> {time_result}")   
#
#            ec_plus = ec.ExactCoverPlus(matrix_a, m, ecp_out_file_path)
#            time_result = timeit.timeit("ec_plus.ec(False)", number=timeit_number)
#            ec_plus.cov.write_comment(f"Average time over {timeit_number} executions -> {time_result}")   
       

#if __name__ == '__main__':
#    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#    input_root = os.path.join(root, "Inputs")
#    output_path = os.path.join(root, "Outputs")
#    timeit_number = 1000
#
#    # execute_files(input_root, output_path)
#    for file in os.listdir(input_root):
#        full_path = os.path.join(input_root, file)
#        if not os.path.isdir(full_path):
#            print(file + " "*10)
#            out_file_path = os.path.join(output_path, f"ec_{file}")
#            ecp_out_file_path = os.path.join(output_path, f"ecp_{file}")
#            m = parser.parse_file(full_path)
#            matrix_a = get_matrix_a(full_path, 250)
#
#            ec_base = ec.ExactCover(matrix_a, m, out_file_path)
#            time_result = timeit.timeit("ec_base.ec(False)", number=timeit_number, globals={"ec_base": ec_base})
#            ec_base.cov.write_comment(f"Average time over {timeit_number} executions -> {time_result}")   
#
#            ec_plus = ec.ExactCoverPlus(matrix_a, m, ecp_out_file_path)
#            time_result = timeit.timeit("ec_plus.ec(False)", number=timeit_number, globals={"ec_plus": ec_plus})
#            ec_plus.cov.write_comment(f"Average time over {timeit_number} executions -> {time_result}")   
