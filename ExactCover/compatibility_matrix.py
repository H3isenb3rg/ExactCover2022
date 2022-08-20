class CompatibilityMatrix:
    def __init__(self, size_m) -> None:
        self.matrix = []
        self.size_m = size_m
        
    def append_empty_line(self, size: int):
        """Adds a new empty list to the matrix
        """
        self.matrix.append(set())
        
    def compatibles(self, i: int, j: int):
        """Adds set j to the list of sets compatible with set i

        Args:
            i (int): index of the set i
            j (int): index of the set j
        """
        self.matrix[i].add(j)
        
    def get_inter(self, i: int, j: int) -> set:
        """Returns the intersection of the two specified columns

        Args:
            i (int): column index of the first compatibility set
            j (int): column index of the second compatibility set

        Returns:
            set: intersection of the two columns of the compatibility matrix
        """
        return self.matrix[i].intersection(self.matrix[j])
    
    def get_tmp_inter(self, inter: set, k: int) -> set:
        return inter.intersection(self.matrix[k])