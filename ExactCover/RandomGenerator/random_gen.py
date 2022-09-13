import random
import time
from random import seed
from random import random


def gen_matrix(row, column):
    matrix_a = [[0 for x in range(column)] for y in range(row)]
    occupied = [0 for x in range(column)]
    for i in range(row):
        for j in range(column):
            matrix_a[i][j] = random_one(1 - occupied[j] * 0.01)
            if matrix_a[i][j] == 1:
                occupied[j] += 1
    return matrix_a


def random_one(prob):
    if prob < 0:
        return 0
    seed(time.time())
    return round(random() * prob)

