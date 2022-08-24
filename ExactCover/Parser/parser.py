def parse_file(input_file: str):
    """
    Parse a file into a bi-dimensional matrix
    Args:
        input_file: the file to parse, in the standard format
    Returns:
        output_matrix: bi-dimensional array of 1 and 0
    """
    file = open(input_file, 'r', encoding='UTF-8')
    lines = file.readlines()
    output_matrix = []
    binary_matrix = []
    m = set()
    for line in lines:
        if line[0] != ';':
            line = clean(line)
            line_bytes = int(line, 2)
            line_set = set(index for index, element in enumerate(line) if element == '1')
            for i, element in enumerate(line_set):
                m.add(element)
            output_matrix.append(line_set)
            binary_matrix.append(line_bytes)
            count = len(line)
    assert void_columns(count, output_matrix), "There is at least one element of M absent in every set of N, " \
                                               "impossible to compute COV "
    return output_matrix, m, binary_matrix


def clean(line: str):
    """
    Remove the unnecessary part of a string
    Args:
        line: the line to clean
    Returns:
        line: cleaned line
    """
    line = line.replace(' ', '')
    line = line.replace('-', '')
    line = line.replace('|', '')
    line = line.replace('\n', '')
    return line


def void_columns(count: int, matrix: list):
    """
       Check if all columns are not empty
       Args:
           count: length of a line of the input file
           matrix: output matrix of the parser
       Returns:
           True if none columns are empty, False if there is an empty column
       """
    max_all_sets = max([max(a_set) for a_set in matrix])
    if max_all_sets + 1 == count:
        return True
    else:
        return False

