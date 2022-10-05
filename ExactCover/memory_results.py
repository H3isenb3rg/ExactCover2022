import sys
import os


def save_results(output_root: str, file: str):
    output_dir = os.path.join(output_root, file.split(".")[0])
    output = os.path.join(output_dir, "memory_results")
    sys.stdout = open(output, 'w')

