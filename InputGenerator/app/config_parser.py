import os
import re

base_re = "base\s=\s([0-9]+)"
rate_re = "rate\s=\s(0\.[0-9]+)"

def parse_config():
    """Parses the config file and returns the parameters

    Returns:
        base(int): The length of the side of a single box of the sudoku table to generate
        rate(int): The percentual of numbers to remove from the sudoku table
    """
    filename = "parameters.cfg"
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

    with open(path, "r") as config_file:
        config_str = config_file.read()

    base = read_base(config_str)
    rate = read_rate(config_str)
    
    return base, rate


def read_base(cfg_str):
    finds = re.findall(base_re, cfg_str)
    if len(finds)==0:
        raise Exception("Error while reading paramenter base.")

    base = int(finds[0])
    if base < 2 or base > 30:
        raise Exception("'Base' parameter boundaries exceeded. Base must be greater than 1 and at most 30")
    
    return base


def read_rate(cfg_str):
    finds = re.findall(rate_re, cfg_str)
    if len(finds)==0:
        raise Exception("Error while reading paramenter rate.")
    
    rate = float(finds[0])
    if rate <= 0 or rate >= 1:
        raise Exception("'Rate' parameter boundaries exceeded. Rate must be a decimal between than 0 and 1 (0 and 1 excluded)")

    return rate


def print_parameters():
    base, rate = parse_config()
    print(f"Base = {base} Rate = {rate}")


if __name__ == "__main__":
    print_parameters()