import sys
import os

RESULTS_FILE = 'memory_results.txt'
BASE_LINE = 20
PLUS_LINE = 22
OFFSET = 24
LEN = 8


def save_results(output_root: str, file: str):
    output_dir = os.path.join(output_root, file.split(".")[0])
    output = os.path.join(output_dir, RESULTS_FILE)
    sys.stdout = open(output, 'w')


def aggregate_results(output_root: str):
    results_list = []
    for filename in os.scandir(output_root):
        if os.path.isdir(filename):
            dire = os.path.join(output_root, filename)
            results = os.path.join(dire, RESULTS_FILE)
            results_file = open(results, 'r')
            lines = results_file.readlines()
            results_list.append(lines[BASE_LINE][OFFSET: OFFSET+LEN])
            results_list.append(lines[PLUS_LINE][OFFSET: OFFSET+LEN])
    print(results_list)


#test rapido, da togliere
def run_aggregate():
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    output_path = os.path.join(root, "Outputs")
    aggregate_results(output_path)

#run_aggregate()

