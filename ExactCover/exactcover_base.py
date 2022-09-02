import numpy as np
import compatibility_matrix as cm
import cov
import time


class ExactCoverBase:
    def __init__(self, matrix_a: list, m: set, out_filename: str) -> None:
        self.cov = cov.Cover(out_filename, "Exact Cover Base")
        self.matrix_a = matrix_a
        self.m = m
        self.compatibility_matrix = cm.CompatibilityMatrix(len(m))
        self.out_filename = out_filename

    def ec(self):
        stp = time.process_time()
        st = time.time()
        self.__ec()
        et = time.time()
        etp = time.process_time()

        with open(self.out_filename, "a") as out_file:
            out_file.write(f"\n;;; Number of sets in COV: {len(self.cov)}\n")
            out_file.write(f";;; Exec process time: {etp-stp}s\n")
            out_file.write(f";;; Exec time: {et-st}s\n")

    def __ec(self):
        for i, set_i in enumerate(self.matrix_a):
            # Current set is empty
            if len(set_i) == 0:
                self.compatibility_matrix.append_empty_line(i+1)
                continue
            
            # Current set has all the elements
            if set_i == self.m:
                self.cov.append([i])
                self.compatibility_matrix.append_empty_line(i+1)
            
            self.compatibility_matrix.append_empty_line(i+1)
            for j, set_j in enumerate(self.matrix_a[:i]):
                print(f"EC Base: {i} - {j}", end="\r")
                if set_j.intersection(set_i):
                    continue
                indexes = [i, j]
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
            indexes_temp = indexes.copy()
            indexes_temp.append(k)
            union_temp = matrix_union.union(self.matrix_a[k])
            if union_temp == self.m:
                self.cov.append(indexes_temp)
            else:
                intersection_temp = self.compatibility_matrix.get_tmp_inter(inter, k)
                if intersection_temp:
                    self.explore(indexes_temp, union_temp, intersection_temp)

