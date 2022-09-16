from random import sample
import copy

class Sudoku:
    def __init__(self, base=3, rate=0.75, p=0):
        """
        Args:
            base (int): The lenght of the side of a single box
            rate (float): 0<rate<1 The percentual of numbers to remove
        """
        self.base = base
        self.rate = rate
        self.p = p
        self.full_board = gen_sudoku(base)
        self.base_board = self.remove_numbers()

    def __str__(self) -> str:
        out = ";;; Sudoku\n"
        out += f";;; Base: {self.base} Rate: {self.rate}\n"
        out += self.str_board(self.full_board)
        out += self.str_board(self.base_board)

        return out

    def str_board(self, board):
        if self.base*self.base > 36:
            out = ""
            for line in board: 
                out += ";;; " + str(line) + "\n"
        else:
            out = pretty_str(self.base, board)
        
        return out
    
    def remove_numbers(self):
        side = self.base * self.base
        squares = side*side
        empties = int(squares * self.rate)
        base_board = copy.deepcopy(self.full_board)
        for p in sample(range(squares),empties):
            base_board[p//side][p%side] = 0
        
        return base_board


def shuffle(s): 
    return sample(s,len(s)) 


def pattern(r, c, base):
    """Pattern for a baseline valid solution
    """
    side = base*base
    return (base*(r%base)+r//base+c)%side


def gen_sudoku(base: int):
    """Generates a random sudoku solution

    Args:
        base (int): lenght of the side of a single box

    Returns:
        list: Complete board as list of lists (of lenght base*base) of numbers representing the sudoku table
    """

    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    board = [ [nums[pattern(r,c,base)] for c in cols] for r in rows ]

    return board


def expandLine(line, base):
    return line[0]+line[5:9].join([line[1:5]*(base-1)]*base)+line[9:13]


def pretty_str(base, board):
    out=""
    side = base*base
    line0  = expandLine("╔═══╤═══╦═══╗", base)
    line1  = expandLine("║ . │ . ║ . ║", base)
    line2  = expandLine("╟───┼───╫───╢", base)
    line3  = expandLine("╠═══╪═══╬═══╣", base)
    line4  = expandLine("╚═══╧═══╩═══╝", base)

    symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums   = [ [""]+[symbol[n] for n in row] for row in board ]
    out += ";;; " + line0 + "\n"
    for r in range(1,side+1):
        out += ";;; " + "".join(n+s for n,s in zip(nums[r-1],line1.split("."))) + "\n"
        out += ";;; " + [line2,line3,line4][(r%side==0)+(r%base==0)] + "\n"

    return out


def gen_print_board():
    base = 3
    rate = 0.75
    sudoku = Sudoku(base, rate)

    print(sudoku)
    

if __name__ == '__main__':
    gen_print_board()