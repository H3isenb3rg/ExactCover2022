import os
import re

row_re = "row\s=\s([0-9]+)"
column_re = "column\s=\s([0-9]+)"


# TODO: invece di dare errore con parametro non trovato do un valore di dafault
# TODO: aggiungere controllo row >= column


def parse_config():
    """Parses the config file and returns the parameters"""
    filename = "parameters.cfg"
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    with open(path, "r") as config_file:
        config_str = config_file.read()
    row = read_row(config_str)
    column = read_column(config_str)
    return int(row), int(column)


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


def print_parameters():
    row, column = parse_config()
    print(f"Row = {row} Column = {column}")


if __name__ == "__main__":
    print_parameters()

