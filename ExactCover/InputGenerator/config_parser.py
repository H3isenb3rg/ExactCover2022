import os
import re

base_re = "base\s=\s([0-9]+)"
rate_re = "rate\s=\s(0\.[0-9]+)"
p_re = "p\s=\s(0\.[0-9]+)"
groups_re = "groups\s=\s(1|2|3|4)"

# TODO: invece di dare errore con parametro non trovato do un valore di dafault

def parse_config():
    """Parses the config file and returns the parameters

    Returns:
        base(int): The length of the side of a single box of the sudoku table to generate
        rate(float): The percentual of numbers to remove from the sudoku table
    """
    filename = "parameters.cfg"
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

    with open(path, "r") as config_file:
        config_str = config_file.read()

    base = read_base(config_str)
    rate = read_rate(config_str)
    p = read_p(config_str)
    groups = read_groups(config_str)
    
    return base, rate, p, groups

def read_p(cfg_str: str) -> float:
    finds = re.findall(p_re, cfg_str)
    if len(finds)==0:
        raise Exception("Error while reading paramenter p. Parameter not found")
    
    p = float(finds[0])
    if p < 0 or p >= 1:
        raise Exception("'p' parameter boundaries exceeded. p must be a decimal between than 0 and 1 (1 excluded)")

    return p


def read_base(cfg_str: str) -> int:
    finds = re.findall(base_re, cfg_str)
    if len(finds)==0:
        raise Exception("Error while reading paramenter base. Parameter not found")

    base = int(finds[0])
    if base < 2 or base > 30:
        raise Exception("'Base' parameter boundaries exceeded. Base must be greater than 1 and at most 30")
    
    if base > 6:
        print("Exceeded recommended base dimension. Generation might take some time")
        response = input("Continue anyway? (Y/N): ")
        while response!="Y" and response!="N":
            print("Please input Y(Yes) or N(No)")
            response = input("Continue anyway? (Y/N): ")
        
        if response=="N":
            exit()
    
    return base

def read_groups(cfg_str: str) -> int:
    finds = re.findall(groups_re, cfg_str)
    if len(finds)==0:
        raise Exception("Error while reading paramenter groups. Parameter not found or wrong values")

    groups = int(finds[0])    
    return groups


def read_rate(cfg_str: str) -> float:
    finds = re.findall(rate_re, cfg_str)
    if len(finds)==0:
        raise Exception("Error while reading paramenter rate. Parameter not found")
    
    rate = float(finds[0])
    if rate <= 0 or rate >= 1:
        raise Exception("'Rate' parameter boundaries exceeded. Rate must be a decimal between than 0 and 1 (0 and 1 excluded)")

    return rate


def print_parameters():
    base, rate, p, groups = parse_config()
    print(f"Base = {base} Rate = {rate} P = {p} Groups = {groups}")


if __name__ == "__main__":
    print_parameters()