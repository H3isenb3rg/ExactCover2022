# TODO: Print cov and other info to a file instead of saving it to a variable
import numpy as np

class ExactCoverBase:
    def __init__(self, matrix_a: list[set], size_m: int) -> None:
        self.cov = []
        self.matrix_a = matrix_a
        self.size_m = size_m
        self.compatibility_matrix = CompatibilityMatrix(size_m)

    def ec(self):
        for i, set_i in enumerate(self.matrix_a):
            # Current set is empty
            if len(set_i) == 0:
                self.compatibility_matrix.append_empty_line(i+1)
                continue
            
            # Current set has all the elements
            if len(set_i) == self.size_m:
                self.cov.append(i)
                self.compatibility_matrix.append_empty_line(i+1)
            
            self.compatibility_matrix.append_empty_line(i+1)
            for j, set_j in enumerate(self.matrix_a[:i]):
                if len(set_j.intersection(set_i)) == 0:
                    continue
                
                indexes = (i , j)
                matrix_union = set_i.union(set_j)
                if len(matrix_union) == self.size_m:
                    self.cov.append(indexes)
                else:
                    self.compatibility_matrix.compatibles(i, j)
                    inter = self.compatibility_matrix.get_inter(i, j)
                    if len(inter) > 0:
                        self.explore(indexes, matrix_union, inter)
                        pass
                    
        return self.cov, self.compatibility_matrix
    
    def explore(self, indexes: list, union: set, intersection: list):
        for k in intersection:
            indexes_temp = indexes.append(k)
            union_temp = union.union(self.matrix_a[k])
            if len(union_temp) == self.size_m:
                self.cov.append(indexes_temp)
            else:
                k_compatible = self.get_compatibles(self.compatibility_matrix, k)
                intersection_temp = list(set(intersection).intersection(k_compatible))
                if intersection_temp:
                    self.explore(indexes_temp, union_temp, intersection_temp)


    def get_compatibles(self, comp_matrix, i):
        compatible = []
        for j in range(len(comp_matrix[i])) - 1:
            line = comp_matrix[j]
            if line[i] == 1:
                compatible.append(j)
        return compatible
    

class CompatibilityMatrix:
    def __init__(self, size_m) -> None:
        self.matrix = []
        self.size_m = size_m
        
    def append_empty_line(self, size: int):
        """Adds a new line of only '0' to the matrix

        Args:
            size (int): the length of the new line
        """
        self.matrix.append(np.zeros(size, dtype=int))
        
    def compatibles(self, i: int, j: int):
        self.matrix[i][j] = 1
        
    def get_inter(self, i: int, j: int):
        first = self.matrix[i][:j-1]
        second = self.matrix[j][:j-1]
        return np.bitwise_and(first, second)