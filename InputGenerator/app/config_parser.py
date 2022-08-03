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

    base = int(re.findall(base_re, config_str)[0])
    rate = float(re.findall(rate_re, config_str)[0])
    
    return base, rate

def print_parameters():
    base, rate = parse_config()
    print(f"Base = {base} Rate = {rate}")

if __name__ == "__main__":
    print_parameters()