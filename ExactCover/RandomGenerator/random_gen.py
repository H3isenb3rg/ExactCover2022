import random
import time
import numpy as np
from random import seed
from random import random


def gen_matrix(row, column, solution):
    matrix_a = [[0 for x in range(column)] for y in range(row)]
    assert column < row, "There is more column than row. " \
                         "Will be impossible compute cov from this file"
    occupied = [0 for x in range(column)]
    for i in range(row):
        for j in range(column):
            matrix_a[i][j] = random_one()
            if matrix_a[i][j] == 1:
                occupied[j] += 1
    if solution:
        for i in range(column):
            for j in range(column):
                matrix_a[i][j] = i == j
    assert all_occupied(occupied), "There is an empty column. " \
                                   "Will be impossible compute cov from this file"
    np.random.shuffle(matrix_a)
    return matrix_a


def random_one():
    seed(time.time())
    return round(np.random.rand())


def all_occupied(occupied):
    for i in occupied:
        if i == 0:
            return False
    return True

