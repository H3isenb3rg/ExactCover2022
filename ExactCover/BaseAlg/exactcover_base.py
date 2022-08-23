# TODO: Print cov and other info to a file instead of saving it to a variable
import numpy as np
import ExactCover.compatibility_matrix as cm


class ExactCoverBase:
    def __init__(self, matrix_a: list[set], m: set) -> None:
        self.cov = []
        self.matrix_a = matrix_a
        self.m = m
        self.compatibility_matrix = cm(len(m))

    def ec(self):
        for i, set_i in enumerate(self.matrix_a):
            # Current set is empty
            if len(set_i) == 0:
                self.compatibility_matrix.append_empty_line(i+1)
                continue
            
            # Current set has all the elements
            if set_i == self.m:
                self.cov.append(i)
                self.compatibility_matrix.append_empty_line(i+1)
            
            self.compatibility_matrix.append_empty_line(i+1)
            for j, set_j in enumerate(self.matrix_a[:i]):
                if not set_j.intersection(set_i).isEmpty():
                    continue
                indexes = (i, j)
                matrix_union = set_i.union(set_j)
                if matrix_union == self.m:
                    self.cov.append(indexes)
                else:
                    self.compatibility_matrix.compatibles(i, j)
                    inter = self.compatibility_matrix.get_inter(i, j)
                    if inter:
                        self.explore(indexes, matrix_union, inter)
                        pass
        return self.cov, self.compatibility_matrix

    def explore(self, indexes: list, matrix_union: set, inter: list):
        for k in inter:
            indexes_temp = indexes.append(k)
            union_temp = matrix_union.union(self.matrix_a[k])
            if union_temp == self.m:
                self.cov.append(indexes_temp)
            else:
                k_compatible = self.get_compatibles(self.compatibility_matrix, k)
                intersection_temp = list(set(inter).intersection(k_compatible))
                if intersection_temp:
                    self.explore(indexes_temp, union_temp, intersection_temp)

    def get_compatibles(self, comp_matrix, i):
        compatible = []
        for j in range(len(comp_matrix[i])) - 1:
            line = comp_matrix[j]
            if line[i] == 1:
                compatible.append(j)
        return compatible

"""
class CompatibilityMatrix:
    def __init__(self, size_m) -> None:
        self.matrix = []
        self.size_m = size_m
        
    def append_empty_line(self, size: int):

        self.matrix.append(np.zeros(size, dtype=int))
        
    def compatibles(self, i: int, j: int):
        self.matrix[i][j] = 1
        
    def get_inter(self, i: int, j: int):
        first = self.matrix[i][:j-1]
        second = self.matrix[j][:j-1]
        return np.bitwise_and(first, second)
    
"""