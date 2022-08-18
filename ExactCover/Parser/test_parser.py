import parser
import os


def gen_matrix(file: str):
    matrix = parser.parse_file(file)
    return matrix


def check_rows(matrix: list, lines: int) -> bool:
    if len(matrix) != lines:
        return False
    return True


def check_bounds(matrix: list, maximum: int) -> bool:
    for row in matrix:
        for element in row:
            if element < 0 or element > maximum:
                return False
    return True


def check_columns(matrix: list, indexes_for_row: int) -> bool:
    dim_matrix = len(matrix)
    for i in range(dim_matrix):
        if len(matrix[i]) == indexes_for_row[i]:
            continue
        else:
            return False
    return True


def test_parser():
    """ Launch all the tests """
    file = 'prova_parser.txt'
    matrix = gen_matrix(file)
    dimension = file_dim(file)
    indexes_for_row = ones_for_row(file)
    assert check_columns(matrix, indexes_for_row)
    assert check_rows(matrix, dimension[0])
    assert check_bounds(matrix, dimension[1])


def file_dim(file: str):
    dimension = [0, 0]
    file = open(file, 'r')
    lines = file.readlines()
    for line in lines:
        if line[0] != ';':
            dimension[0] = dimension[0] + 1
            dimension[1] = int((len(line) - 1) / 2)
    return dimension


def ones_for_row(file: str):
    ones = []
    file = open(file, 'r')
    lines = file.readlines()
    for line in lines:
        if line[0] != ';':
            ones.append(line.count('1'))
    return ones



#test al volo
test_parser()

