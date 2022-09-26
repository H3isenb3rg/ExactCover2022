import compatibility_matrix as cm
import cov
import time
import matrix_a as ma


class ExactCoverPlus:
    def __init__(self, matrix_a: ma.MatrixA, size_m: int, out_filename: str) -> None:
        self.out_filename = out_filename
        self.cov = cov.Cover(out_filename, "Exact Cover Plus")
        self.card = []
        self.matrix_a = matrix_a
        self.size_m = size_m
        self.compatibility_matrix = cm.CompatibilityMatrix(size_m)
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

        self.cov.execution_ended()
        self.cov.write_comment(f"Number of sets in COV: {len(self.cov)}")
        self.cov.write_comment(f"Exec process time: {etp-stp}s")
        self.cov.write_comment(f"Exec time: {et-st}s")

    def __ec(self):
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
