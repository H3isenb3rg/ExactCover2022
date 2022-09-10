from distutils.errors import LinkError
import linecache
import re
import os
import Parser.parser as parser

class MatrixA(object):
    def __init__(self, file_path: str, chunk_len:int = 50) -> None:
        self.file_path = file_path
        """ Path to the input file """
        
        self.chunk_len = chunk_len
        """ Lenght of each chunk """
        
        self.curr_chunk_i = 0
        """ Current chunk loaded in memory """

        self.curr_chunk = None
        """ Chunk currently loaded in memory """
        
        self.start_line = None
        """ Line number where the matrix starts in the input file """

        self.matrix_height = 0
        """ Total number of lines of the matrix """

        self.otimised_file_path = os.path.join(os.path.dirname(file_path), "optimised.txt")
        """ Path to temporary file result of sudoku optimisation """

        m = set()
        # Open input file
        with open(file_path, "r", encoding='UTF-8') as input_file:
            # Iterate over every line of the file
            for i, line in enumerate(input_file):
                if line[0] != ";":  # Current line is not a comment
                    line = parser.clean(line)
                    self.matrix_height += 1

                    # If this line is the first line of the matrix
                    if self.start_line is None:
                        self.start_line = i
                        len_m = len(line)

                    line_set = set(index for index, element in enumerate(line) if element == '1')
                    m = m.union(line_set)
            
            assert len_m == len(m), "At least one element doesn't appear in any set. Can't compute COV"
        
        # Load the first chunk
        self.load_chunk_by_number(0)

    def __len__(self):
        return self.matrix_height

    def __getitem__(self, key: int):
        # Se indice richiesto dentro chunk attuale allora ritorno set
        # Altrimenti carico chunk richiesto e ritorno set
        assert key<self.matrix_height

        if key//self.chunk_len!=self.curr_chunk_i:
            # Index is outside the current chunk we need to load the correct one
            self.load_chunk_by_index(key)

        chunk_idx = key - self.chunk_len*self.curr_chunk_i
        return self.curr_chunk[chunk_idx]

    def load_chunk_by_number(self, n: int):
        """ Loads a new chunk of the matrix in memory

        (args)
            n (int): Which chunk to load (first chunk is n=0)
        """
        chunk_start = self.chunk_len * n
        assert chunk_start < self.matrix_height

        if chunk_start + self.chunk_len-1 < self.matrix_height:
            # Not the last chunk we need to load the whole chunk_len
            total_rows = self.chunk_len
        else:
            # It's the last chunk we need to load only the remaining cells
            total_rows = self.matrix_height - chunk_start

        self.curr_chunk = []
        for j in range(total_rows):
            curr_file_line = self.start_line + chunk_start + j + 1  # '+1' because getline counts from 1 (first line is line 1)
            line = linecache.getline(self.file_path, curr_file_line)
            line = parser.clean(line)
            line_set = set(index for index, element in enumerate(line) if element == '1')
            self.curr_chunk.append(line_set)
        
        # Save the current chunk number loaded in memeory
        self.curr_chunk_i = n
    
    def load_chunk_by_index(self, i:int):
        """ Loads a new chunk of the matrix in memory by specifying the desired index

        (args)
            i (int): The desired index
        """
        assert i < self.matrix_height
        n = i // self.chunk_len
        self.load_chunk_by_number(n)
        


    