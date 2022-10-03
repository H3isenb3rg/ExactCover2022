import linecache, re
import Parser.parser as parser
import cov as cv
from InputGenerator.sudoku_gen import pretty_str
import InputGenerator.test_generator as test_generator


def parse_line_set(file_path: str, line_number: int):
    """Gets and cleans the given line of the file and returns the indexes set of the line
    Args:
        file_path (str): Path to the input file
        line_number (int): Line to retrieve from the file
    Returns:
        set: Set of indexes of the 'ones' in the line
    """
    raw_line = linecache.getline(file_path, line_number)
    line = parser.clean(raw_line)
    return set(index for index, element in enumerate(line) if element == '1')
    

class MatrixA(object):
    def __init__(self, file_path: str, chunk_len:int = 50) -> None:
        self.file_path = file_path
        """ Path to the input file """
        
        self.chunk_len = chunk_len
        """ Length of each chunk """
        
        self.curr_chunk_i = 0
        """ Current chunk loaded in memory """

        self.curr_chunk = None
        """ Chunk currently loaded in memory """
        
        self.start_line = None
        """ Line number where the matrix starts in the input file """

        self.matrix_height = 0
        """ Total number of lines of the matrix """

        self.m = set()
        """ Set M """

        # Open input file
        self.init_matrix()
        
        # Load the first chunk
        self.load_chunk_by_number(0)

    def init_matrix(self):
        """Initial check for missing element (Exact cover impossible)"""
        with open(self.file_path, "r", encoding='UTF-8') as input_file:
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
                    self.m = self.m.union(line_set)

            if len_m < len(self.m):
                raise Exception("At least one element doesn't appear in any set. Can't compute COV")

    def __str__(self) -> str:
        return f"|N|: {self.matrix_height}   |M|: {len(self.m)}"

    def __len__(self):
        return self.matrix_height

    def __getitem__(self, key: int):
        # Se indice richiesto dentro chunk attuale allora ritorno set
        # Altrimenti carico chunk richiesto e ritorno set
        if key>=self.matrix_height:
            raise Exception(f"Matrix A element '{key}' out of bounds")

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
        if chunk_start >= self.matrix_height:
            raise Exception(f"Requested chunk '{n}' is not in the matrix")

        if chunk_start + self.chunk_len-1 < self.matrix_height:
            # Not the last chunk we need to load the whole chunk_len
            total_rows = self.chunk_len
        else:
            # It's the last chunk we need to load only the remaining cells
            total_rows = self.matrix_height - chunk_start

        self.curr_chunk = []
        for j in range(total_rows):
            curr_file_line = self.start_line + chunk_start + j + 1  # '+1' because getline counts from 1 (first line is line 1)
            line_set = parse_line_set(self.file_path, curr_file_line)
            self.curr_chunk.append(line_set)
        
        # Save the current chunk number loaded in memeory
        self.curr_chunk_i = n

    def load_chunk_by_index(self, i:int):
        """ Loads a new chunk of the matrix in memory by specifying the desired index
        (args)
            i (int): The desired row of the matrix
        """
        if i>=self.__len__():
            raise Exception(f"Index {i} out of bounds")
        
        n = i // self.chunk_len
        self.load_chunk_by_number(n)

    def parse_cov(self, cov: list[int]):
        return [i+1 for i in cov]
    
    def print_final_matrix(self, cov: cv.Cover):
        """ 
        If [Matrix A] base does nothing.    

        If [Matrix A Sudoku] prints to output the resulting sudoku tables
        """
        pass
    
    def cardinalities_distribution(self) -> dict:
        cards = {}

        for i in range(len(self)):
            curr_card = len(self[i])
            if curr_card in cards:
                cards[curr_card] += 1
            else:
                cards[curr_card] = 1
        
        return cards


class MatrixA_Sudoku(MatrixA):
    def __init__(self, file_path: str, chunk_len: int = 50) -> None:
        super().__init__(file_path, chunk_len)

    def init_matrix(self):
        super().init_matrix()
        self.base = self.get_base()
        
        # Build set of filled Sudoku cells             
        self.filled_set, self.index_filled, self.index_empty = self.get_filled_set()

    def get_base(self):
        finds = re.findall(";;; Base:\s([0-9]+)", linecache.getline(self.file_path, 2))
        return int(finds[0])

    def get_filled_set(self):
        i=self.start_line+1
        filled_set = set()
        index_filled = []
        index_empty = []
        while i <= (self.matrix_height + self.start_line):
            cur_set = parse_line_set(self.file_path, i)
            try:
                next_set = parse_line_set(self.file_path, i+1)
                if min(cur_set) == min(next_set):
                    # Empty Sudoku Cell
                    index_empty.extend([k for k in range(i, i+self.base**2)])
                    i += self.base**2
                else:
                    # Filled Sudoku cell
                    filled_set = filled_set.union(cur_set)
                    index_filled.append(i)
                    i+=1
            except ValueError:
                # current line is the last line of the matrix
                # filled cell for sure
                filled_set = filled_set.union(cur_set)
                index_filled.append(i)
                i+=1

        # print(len(index_empty))
        index_empty = self.clean_empties(index_empty, filled_set)
        # print(len(index_empty))

        return filled_set, index_filled, index_empty
    
    def clean_empties(self, empties: list[int], filled_set: set[int]):
        tb_removed = []
        for index in empties:
            cur_set = parse_line_set(self.file_path, index)
            if len(filled_set.intersection(cur_set)) > 0:
                # Cur empty is not compatible with the filled set. Remove it
                tb_removed.append(index)
        
        for index in tb_removed:
            empties.remove(index)

        return empties

    def __str__(self) -> str:
        return f"|N| -> Initial: {self.matrix_height}   Optimised for Sudoku: {len(self)}\n|M|: {len(self.m)}"

    def __len__(self):
        return len(self.index_empty) + 1

    def __getitem__(self, key: int) -> set:
        # Se indice richiesto dentro chunk attuale allora ritorno set
        # Altrimenti carico chunk richiesto e ritorno set
        if key>=self.__len__():
            raise Exception(f"Index {key} out of bounds")

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
        if chunk_start >= self.__len__():
            raise Exception("Out of bound Error")

        if chunk_start + self.chunk_len-1 < self.__len__():
            # Not the last chunk we need to load the whole chunk_len
            total_rows = self.chunk_len
        else:
            # It's the last chunk we need to load only the remaining cells
            total_rows = self.__len__() - chunk_start

        self.curr_chunk = []
        if chunk_start == 0:
            self.curr_chunk.append(self.filled_set)
            j=1
        else:
            j=0
        
        while j<total_rows:
            curr_file_line = self.index_empty[chunk_start + j-1]  # '+1' because getline counts from 1 (first line is line 1)
            line_set = parse_line_set(self.file_path, curr_file_line)
            self.curr_chunk.append(line_set)
            j+=1
        
        # Save the current chunk number loaded in memeory
        self.curr_chunk_i = n
    
    def parse_cov(self, cov: list[int]):
        """Convert indexes in cov received from EC alg into indexes of the original matrix"""
        new_cov = []

        if 0 in cov:
            new_cov.extend([k-self.start_line for k in self.index_filled])
            cov.remove(0)

        for index in cov:
            new_cov.append(self.index_empty[index-1] - self.start_line)

        return new_cov

    def print_final_matrix(self, cov: cv.Cover):
        # Build Sudoku Table
        side = self.base**2
        area = side**2

        empty_row = [0 for j in range(side)]
        initial_table = [empty_row.copy() for k in range(side)]

        for index in self.index_filled:
            line_set = sorted(parse_line_set(self.file_path, int(index)))
            cur_cell = line_set[0]
            cell_number = (line_set[1]-area) + 1 - (cur_cell // side)*side

            y = cur_cell//side
            x = cur_cell - y*side
            initial_table[y][x] = cell_number
        
        out = f"Starting Sudoku Table:\n{pretty_str(self.base, initial_table, begin='')}\n"

        out += "Resulting Sudoku Tables:\n"
        for solution in cov.cov:
            table = [[] for k in range(side)]
            for index in solution:
                line_set = sorted(parse_line_set(self.file_path, int(index)+self.start_line))
                cur_cell = line_set[0]
                cell_number = (line_set[1]-area) + 1 - (cur_cell // side)*side
                y = cur_cell//side
                table[y].append(cell_number)
            
            # Check if feasible solution
            test_generator.assert_rules(table, self.base)

            str_table = pretty_str(self.base, table, begin="")
            out += f"{str_table}\n"
        
        cov.write_comment(out, begin="", end="")
    
    def cardinalities_distribution(self) -> dict:
        if len(self.index_filled) == 1:
            return {4: self.matrix_height}
        
        return {
            4: len(self.index_empty),
            len(self.index_filled)*4: 1
        }
        
