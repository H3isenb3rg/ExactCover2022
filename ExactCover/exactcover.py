import numpy as np
import compatibility_matrix as cm
import cov
import time
import matrix_a as ma

# FIXME: per il random i risultati non corrispondono
class ExactCover:
    def __init__(self, matrix_a: ma.MatrixA, m: set, input_filename: str, out_dir: str):
        self.matrix_a = matrix_a
        self.compatibility_matrix = cm.CompatibilityMatrix(len(m))
        self.time = None
        """Execution time"""
        self.m = m
        self.finish_init(out_dir, input_filename, m)

        self.total_nodes = 2**(len(self.matrix_a))-1
        self.visited_nodes = 0
    
    def finish_init(self, out_dir: str, input_filename: str, m: set):
        self.cov = cov.Cover(out_dir, input_filename, "Exact Cover Base")

    def ec(self, verbose:bool = True):
        self.cov.init_out_file()
        self.cov.write_comment(str(self.matrix_a))

        start = time.time()
        self._ec(verbose)
        self.time = time.time() - start

        if verbose:
            self.cov.write_comment(begin="\n", comment=f"Number of sets in COV: {len(self.cov)}")
            self.cov.write_comment(f"Execution Time: {round(self.time, 6)}s", end="\n\n")
            self._print_cardinalities("Cardinalities Distribution (cardinality -> occurrences):", self.cov.cardinalities_distribution())
            self._print_cardinalities("Matrix A Cardinalities Distribution:", self.matrix_a.cardinalities_distribution(), True)
            self.cov.write_comment(comment=f"Visited nodes: {round(self.visited_nodes*100/self.total_nodes, 2)}% ({self.visited_nodes:,}/{self.total_nodes:,})", end="\n\n")
            self.matrix_a.print_final_matrix(self.cov)

    def _print_cardinalities(self, title: str, cards: dict, skip_base: bool = False):
        if not skip_base:
            self.print_cardinalities(title, cards)
    
    def print_cardinalities(self, title: str, cards: dict):
        self.cov.write_comment(title)
        for card in sorted(cards.keys()):
            self.cov.write_comment(f"{card} -> {cards[card]}")
        self.cov.write_comment("")

    def new_node(self):
        self.visited_nodes += 1

    def _ec(self, verbose: bool = True):
        for i in range(len(self.matrix_a)):
            set_i = self.matrix_a[i]

            self.new_node()
            
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
                self.new_node()

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

    def explore(self, indexes: list, matrix_union: set, inter: list):
        for k in inter:
            indexes_temp = indexes.copy()
            indexes_temp.append(k)
            union_temp = matrix_union.union(self.matrix_a[k])
            self.new_node()
            if union_temp == self.m:
                self.cov.append(self.matrix_a.parse_cov(indexes_temp))
            else:
                intersection_temp = self.compatibility_matrix.get_tmp_inter(inter, k)
                if intersection_temp:
                    self.explore(indexes_temp, union_temp, intersection_temp)


class ExactCoverPlus(ExactCover):
    def __init__(self, matrix_a: ma.MatrixA, m: set, input_filename: str, out_dir: str):
        super().__init__(matrix_a, m, input_filename, out_dir)

    def finish_init(self, out_dir: str, input_filename: str, m: set):
        self.cov = cov.Cover(out_dir, input_filename, "Exact Cover Plus")
        self.size_m = len(self.m)
        self.card = []

    def _print_cardinalities(self, title: str, cards: dict, skip_base: bool = False):
        self.print_cardinalities(title, cards)

    def _ec(self, verbose: bool = True):
        for i in range(0, len(self.matrix_a)):
            set_i = self.matrix_a[i]
            self.new_node()

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
                self.new_node()

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
            self.new_node()
            if card_temp == self.size_m:
                self.cov.append(self.matrix_a.parse_cov(indexes_temp))
            else:
                intersection_temp = self.compatibility_matrix.get_tmp_inter(inter, k)
                if len(intersection_temp)>0:
                    self.explore(indexes_temp, card_temp, intersection_temp)

