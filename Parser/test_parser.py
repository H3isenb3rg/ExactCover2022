from InputGenerator.app import app
import parser
import os


def gen_matrix(file):
    matrix = parser.parse_file(file)
    return matrix


def check_dimension(matrix, dim) -> bool:
    """
    Verifies that the dimension of the parsed matrix are the same of the expected from the file.
    Args:
        matrix: parsed matrix, a list
        dim: array with 2 elements, n of row and column
    Returns:
        bool: True if the dimension are compatible
    """
    if len(matrix[0]) != dim[1]:
        return False
    if len(matrix) != dim[0]:
        return False
    return True


def check_binary(matrix) -> bool:
    """
    Verifies that all the element of the matrix are either 1 or 0.
    Args:
        matrix: parsed matrix, a list
    Returns:
        bool: True if all elements are 0 or 1
    """
    for row in matrix:
        for element in row:
            if element != 0 and element != 1:
                return False
    return True


def test_parser():
    """
    Launch all the tests
    """
    """ genera e prende l'ultimo
    app.run()
    input_dir = '../InputGenerator/GeneratedInputs'
    files = os.listdir(input_dir)
    paths = [os.path.join(input_dir, basename) for basename in files]
    file = max(paths, key=os.path.getctime)
    """
    file = '../InputGenerator/GeneratedInputs/3_75_05082022203316.txt'
    matrix = gen_matrix(file)
    dimension = file_dim(file)

    assert check_binary(matrix)
    assert check_dimension(matrix, dimension)


def file_dim(file):
    """
    Compute the expected dimensions of the parsed array from the file.
    Args:
        file: the file to parse
    Returns:
        dimension: array that contain two elements, n of row and n of column
    """
    dimension = [0,0]
    file = open(file, 'r')
    lines = file.readlines()
    for line in lines:
        if line[0] != ';':
            dimension[0] = dimension[0] + 1
            dimension[1] = int((len(line) - 1) / 2)
    return dimension


#test al volo
test_parser()

