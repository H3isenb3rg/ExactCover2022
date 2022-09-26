import numpy as np
import compatibility_matrix as cm
import cov
import time
import matrix_a as ma


class ExactCoverBase:
    def __init__(self, matrix_a: ma.MatrixA, m: set, out_filename: str) -> None:
        self.cov = cov.Cover(out_filename, "Exact Cover Base")
        self.matrix_a = matrix_a
        self.m = m
        self.compatibility_matrix = cm.CompatibilityMatrix(len(m))
        self.out_filename = out_filename
        self.pt = None
        """CPU time"""
        self.et = None
        """Effective time"""

    def ec(self):
        stp = time.process_time()
        st = time.time()
        self.__ec()
        et = time.time()
        etp = time.process_time()

        self.pt = etp-stp
        self.et = et-st

        self.cov.write_comment("", begin="")
        self.cov.write_comment(f"Number of sets in COV: {len(self.cov)}")
        self.cov.write_comment(f"Exec process time: {etp-stp}s")
        self.cov.write_comment(f"Exec time: {et-st}s")
        self.matrix_a.print_final_matrix(self.cov)

    def __ec(self):
        for i in range(len(self.matrix_a)):
            set_i = self.matrix_a[i]
            # Current set is empty
            if len(set_i) == 0:
                self.compatibility_matrix.append_empty_line(i+1)
                continue
            
            # Current set has all the elements
            if set_i == self.m:
                self.cov.append(self.matrix_a.parse_cov([i]))
                self.compatibility_matrix.append_empty_line(i+1)
            
            self.compatibility_matrix.append_empty_line(i+1)
            for j in range(i):
                set_j = self.matrix_a[j]
                print(f"EC Base: {i} - {j}   ", end="\r")
                if set_j.intersection(set_i):
                    continue
                indexes = [i, j]
                matrix_union = set_i.union(set_j)
                if matrix_union == self.m:
                    self.cov.append(self.matrix_a.parse_cov(indexes))
                else:
                    self.compatibility_matrix.compatibles(i, j)
                    inter = self.compatibility_matrix.get_inter(i, j)
                    if inter:
                        self.explore(indexes, matrix_union, inter)
                        pass

    def explore(self, indexes: list, matrix_union: set, inter: list):
        for k in inter:
            indexes_temp = indexes.copy()
            indexes_temp.append(k)
            union_temp = matrix_union.union(self.matrix_a[k])
            if union_temp == self.m:
                self.cov.append(self.matrix_a.parse_cov(indexes_temp))
            else:
                intersection_temp = self.compatibility_matrix.get_tmp_inter(inter, k)
                if intersection_temp:
                    self.explore(indexes_temp, union_temp, intersection_temp)

