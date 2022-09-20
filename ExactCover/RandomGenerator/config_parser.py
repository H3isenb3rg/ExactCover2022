import os
import re

row_re = "row\s=\s([0-9]+)"
column_re = "column\s=\s([0-9]+)"
solution_re = "solution\s=\s([0-1])"


def parse_config():
    """Parses the config file and returns the parameters"""
    filename = "parameters.cfg"
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    with open(path, "r") as config_file:
        config_str = config_file.read()
    row = read_row(config_str)
    column = read_column(config_str)
    solution = read_solution(config_str)
    return int(row), int(column), bool(solution)


def read_row(cfg_str: str) -> float:
    finds = re.findall(row_re, cfg_str)
    if len(finds) == 0:
        raise Exception("Error while reading paramenter row. Parameter not found")
    row = float(finds[0])
    if row < 0:
        raise Exception("'row' parameter boundaries exceeded. row must be integer positive")
    return row


def read_column(cfg_str: str) -> int:
    finds = re.findall(column_re, cfg_str)
    if len(finds) == 0:
        raise Exception("Error while reading paramenter column. Parameter not found")
    column = float(finds[0])
    if column < 0:
        raise Exception("'column' parameter boundaries exceeded. column must be integer positive")
    return column


def read_solution(cfg_str: str) -> bool:
    finds = re.findall(solution_re, cfg_str)
    if len(finds) == 0:
        raise Exception("Error while reading parameter solution. Parameter not found")
    if finds[0] != '0' and finds[0] != '1':
        raise Exception("solution must be 0 or 1")
    return finds[0]


def print_parameters():
    row, column = parse_config()
    print(f"Row = {row} Column = {column}")


if __name__ == "__main__":
    print_parameters()

