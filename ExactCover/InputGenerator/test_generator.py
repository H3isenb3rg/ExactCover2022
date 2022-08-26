import sudoku_gen

def generate_full_sudoku_board(base):
    return sudoku_gen.Sudoku(base=base).full_board

def rule1(board) -> bool:
    """Verifies the first rule of the sudoku table: Every cell contains exactly one of the symbols.

    Args:
        board (list): The board to check

    Returns:
        bool: True if the first rule is respected False otherwise
    """
    side = len(board)

    for row in board:
        for cell in row:
            if cell < 1 or cell > side:
                return False

    return True

def rule2(board) -> bool:
    """Verifies the second rule of the sudoku table: Every column has exactly one occurrence of each symbol.

    Args:
        board (list): The board to check

    Returns:
        bool: True if the second rule is respected False otherwise
    """    
    side = len(board)

    for i in range(0, side):
        cur_found = []
        for j in range(0, side):
            if board[j][i] in cur_found:
                return False
            cur_found.append(board[j][i])

    return True

def rule3(board) -> bool:
    """Verifies the third rule of the sudoku table: Every row has exactly one occurrence of each symbol.

    Args:
        board (list): The board to check

    Returns:
        bool: True if the third rule is respected False otherwise
    """

    for row in board:
        cur_found = []
        for cell in row:
            if cell in cur_found:
                return False
            cur_found.append(cell)

    return True

def rule4(board, base) -> bool:
    """Verifies the fourth rule of the sudoku table: Every base by base box has exactly one occurrence of each symbol.

    Args:
        board (list): The board to check
        base (int): The lenght of a single box of the sudoku table.

    Returns:
        bool: True if the fourth rule is respected False otherwise
    """
    curr_box = 0
    side = len(board)

    # 'side' boxes to check
    # curr_box%base -> curr col of boxes
    # curr_box//base -> curr row of boxes
    # first cell of the box -> board[curr_box//base+1][curr_box%base+1]
    while curr_box < side:
        col_box = curr_box%base
        row_box = curr_box//base
        first_cell = (row_box*base, col_box*base)
        curr_found = []
        for i in range(0, base):
            for j in range(0, base):
                curr_index = (first_cell[0]+i, first_cell[1]+j)
                cell = board[curr_index[0]][curr_index[1]]
                if cell in curr_found:
                    return False
                curr_found.append(cell)
        curr_box+=1

    return True


def test_dimensions():
    bases = [2, 3, 4, 6, 10, 30]

    for base in bases:
        curr_board = generate_full_sudoku_board(base)
        side = base*base
        assert len(curr_board) == side
        for i in range(0, side):
            assert len(curr_board[i]) == side


def test_sudoku_rules():
    bases = [2, 3, 4, 6, 10, 30]

    for base in bases:
        curr_board = generate_full_sudoku_board(base)
        assert rule1(curr_board)
        assert rule2(curr_board)
        assert rule3(curr_board)
        assert rule4(curr_board, base)