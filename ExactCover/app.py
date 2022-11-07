import os
from Parser import parser
import exactcover as ec
import matrix_a as ma
import linecache
import filecmp
import cov
import pandas as pd
#from filprofiler.api import profile

def launch(input_root, output_path):
    comp_results = []

    try:
        execute_files(input_root, output_path, comp_results)
    except KeyboardInterrupt:
        pass

    print(comp_results)
    results_df = pd.DataFrame.from_records(
        comp_results, 
        columns=[
            "name", 
            "N", 
            "M", 
            "Time Base", 
            "Time Plus",
            "Visited Base",
            "Visited Plus",
            "Total Nodes Base",
            "Total Nodes Plus",
            "Visited Rate Base",
            "Visited Rate Plus",
            "Cov Len Base",
            "Cov Len Plus",
            "Sudoku Rate",
            "Sudoku Base"
            ])
    results_df.to_csv(os.path.join(output_path, "data.csv"))


def execute_files(root_path: str, output_root: str, results: list):
    """Executes the exact cover algorithm for all files inside the 'Inputs' folder

    Args:
        root_path (string): path to the 'Inputs' folder
    """
    for file in os.listdir(root_path):
        print(file + " "*10)
        cur_file_path = os.path.join(root_path, file)
        if os.path.isdir(cur_file_path):
            execute_files(cur_file_path, output_root, results)
        else:
            # m = parser.parse_file(cur_file_path)
            matrix_a = get_matrix_a(cur_file_path, 250)
            ec_base = ec.ExactCover(matrix_a, file, output_root)
            #profile(lambda: ec_base.ec(), 'fil/base' + file) # cambiare commento per profilare memoria
            ec_base.ec()
            ec_plus = ec.ExactCoverPlus(matrix_a, file, output_root)
            #profile(lambda: ec_plus.ec(), 'fil/plus' + file) # cambiare commento per profilare memoria
            ec_plus.ec()
            compare_results_file(ec_base.cov, ec_plus.cov)

            results_to_append = [
                file,                   # Name of the file
                len(matrix_a),          # |N|
                len(ec_base.m),         # |M|
                ec_base.time,           # EC Base execution time
                ec_plus.time,           # EC Plus execution time
                ec_base.visited_nodes,  # nodi visitati
                ec_plus.visited_nodes,  
                ec_base.total_nodes,    # nodi totali
                ec_plus.total_nodes,  
                round(ec_base.visited_nodes*100/ec_base.total_nodes, 2),    # % nodi visitati
                round(ec_plus.visited_nodes*100/ec_plus.total_nodes, 2),  
                len(ec_base.cov),       # Numero di set nel COV 
                len(ec_plus.cov)
            ]

            if "Sudoku" in cur_file_path or "Random" in cur_file_path:
                if "Sudoku" in cur_file_path:
                    results_to_append.extend([
                        ec_base.matrix_a.rate,  # Sudoku -> Rate
                        ec_base.matrix_a.base   # Sudoku -> Base
                    ])
                else:
                    results_to_append.extend([
                        0,
                        0
                    ])
                print("    " + compare_results(ec_base, ec_plus))

            results.append(results_to_append)

def log_computational_results():
    pass

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
        return ma.MatrixA_Binary(cur_file_path, chunk_size)

def compare_results(baseEC: ec.ExactCover, plusEC: ec.ExactCoverPlus) -> str:
    if baseEC.time > plusEC.time:
        rate = round(baseEC.time/plusEC.time, 2)
        return f"Plus alg {rate} times faster than Base alg"
    elif plusEC.time > baseEC.time:
        rate = round(plusEC.time/baseEC.time, 2)
        return f"Base alg {rate} times faster than Plus alg"
    else:
        return "Both alg executed in similar times"
