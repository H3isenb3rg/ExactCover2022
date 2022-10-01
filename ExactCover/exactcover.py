import numpy as np
import compatibility_matrix as cm
import cov
import time
import matrix_a as ma


class ExactCover:
    def __init__(self, matrix_a: ma.MatrixA, m: set, out_filename: str):
        self.out_filename = out_filename
        self.matrix_a = matrix_a
        self.compatibility_matrix = cm.CompatibilityMatrix(len(m))
        self.time = None
        """Execution time"""
        self.finish_init(out_filename, m)
    
    def finish_init(self, out_filename: str, m: set):
        self.cov = cov.Cover(out_filename)
        self.alg_name = "Exact Cover Base"
        self.m = m

    def ec(self, verbose:bool = True):
        self.cov.init_out_file(self.alg_name)

        start = time.time()
        self._ec(verbose)
        self.time = time.time() - start

        if verbose:
            self.cov.write_comment("", begin="")
            self.cov.write_comment(f"Number of sets in COV: {len(self.cov)}")
            self.cov.write_comment(f"Execution Time: {self.time}s")
            self.matrix_a.print_final_matrix(self.cov)

    def _ec(self, verbose: bool = True):
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

                if verbose:
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


class ExactCoverPlus(ExactCover):
    def __init__(self, matrix_a: ma.MatrixA, m: set, out_filename: str):
        super().__init__(matrix_a, m, out_filename)

    def finish_init(self, out_filename: str, m: set):
        self.cov = cov.Cover(out_filename)
        self.alg_name = "Exact Cover Plus"
        self.card = []
        self.size_m = len(m)

    def _ec(self, verbose: bool = True):
        for i in range(0, len(self.matrix_a)):
            set_i = self.matrix_a[i]
            # Current set is empty
            if len(set_i) == 0:
                self.compatibility_matrix.append_empty_line(i+1)
                self.card.append(0)
                continue
            
            # Current set has all the elements
            if len(set_i) == self.size_m:
                self.cov.append(self.matrix_a.parse_cov([i]))
                self.compatibility_matrix.append_empty_line(i+1)
                self.card.append(self.size_m)
            
            self.card.append(len(set_i))
            self.compatibility_matrix.append_empty_line(i+1)
            for j in range(i):
                set_j = self.matrix_a[j]

                if verbose:
                    print(f"EC Plus: {i} - {j}   ", end="\r")

                if len(set_j.intersection(set_i)) != 0:
                    continue
                
                indexes = [i , j]
                card_u = self.card[i] + self.card[j]
                if card_u == self.size_m:
                    self.cov.append(self.matrix_a.parse_cov(indexes))
                else:
                    self.compatibility_matrix.compatibles(i, j)
                    inter = self.compatibility_matrix.get_inter(i, j)
                    if len(inter) > 0:
                        self.explore(indexes, card_u, inter)
    
    def explore(self, indexes: list, card_u: int, inter: list):
        for k in inter:
            indexes_temp = indexes.copy()
            indexes_temp.append(k)
            card_temp = card_u + len(self.matrix_a[k])
            if card_temp == self.size_m:
                self.cov.append(self.matrix_a.parse_cov(indexes_temp))
            else:
                intersection_temp = self.compatibility_matrix.get_tmp_inter(inter, k)
                if len(intersection_temp)>0:
                    self.explore(indexes_temp, card_temp, intersection_temp)

