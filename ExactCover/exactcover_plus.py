import numpy as np
import compatibility_matrix as cm
import cov

class ExactCoverPlus:
    def __init__(self, matrix_a: list[int], size_m: int, out_filename: str) -> None:
        self.cov = cov.Cover(out_filename, "Exact Cover Plus")
        self.card = []
        self.matrix_a = matrix_a
        self.size_m = size_m
        self.empty_set = 0
        self.full_set = int(b"1"*size_m, 2)
        # self.empty_set = int(b"0"*size_m, 2)
        # self.full_set = int(b"1"*size_m, 2)
        self.compatibility_matrix = cm.CompatibilityMatrix(size_m)

    def ec(self):
        for i, line_i in enumerate(self.matrix_a):
            # Current set is empty
            if line_i == self.empty_set:
                self.compatibility_matrix.append_empty_line(i+1)
                self.card.append(0)
                continue
            
            # Current set has all the elements
            if line_i == self.full_set:
                self.cov.append([i])
                self.compatibility_matrix.append_empty_line(i+1)
                self.card.append(self.size_m)
            
            self.card.append(bin(line_i).count("1"))
            self.compatibility_matrix.append_empty_line(i+1)
            for j, line_j in enumerate(self.matrix_a[:i]):
                # print(f"{i} - {j}")
                if line_j & line_i != self.empty_set:
                    continue
                
                indexes = [i , j]
                card_u = self.card[i] + self.card[j]
                if card_u == self.size_m:
                    self.cov.append(indexes)
                else:
                    self.compatibility_matrix.compatibles(i, j)
                    inter = self.compatibility_matrix.get_inter(i, j)
                    if len(inter) > 0:
                        self.explore(indexes, card_u, inter)
                    
        return self.cov, self.compatibility_matrix
    
    def explore(self, indexes: list, card_u: int, inter: list):
        for k in inter:
            indexes_temp = indexes.copy()
            indexes_temp.append(k)
            card_temp = card_u + bin(self.matrix_a[k]).count("1")
            if card_temp == self.size_m:
                self.cov.append(indexes_temp)
            else:
                intersection_temp = self.compatibility_matrix.get_tmp_inter(inter, k)
                if len(intersection_temp)>0:
                    self.explore(indexes_temp, card_temp, intersection_temp)
