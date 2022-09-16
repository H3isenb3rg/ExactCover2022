import random
import time
from random import seed
from random import random


def gen_matrix(row, column):
    matrix_a = [[0 for x in range(column)] for y in range(row)]
    occupied = [0 for x in range(column)]
    for i in range(row):
        for j in range(column):
            matrix_a[i][j] = random_one(1 - occupied[j] * 0.02)
            if matrix_a[i][j] == 1:
                occupied[j] += 1
    assert all_occupied(occupied), "There is an empty column. Will be impossible compute cov from this file"
    return matrix_a


def random_one(prob):
    if prob < 0:
        return 0
    seed(time.time())
    return round(random() * prob)


def all_occupied(occupied):
    for i in occupied:
        if i == 0:
            return False
    return True

