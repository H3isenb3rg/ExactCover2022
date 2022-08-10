
def parse_file(input_file):
    """
    Parse a file into a bi-dimensional matrix
    Args:
        input_file: the file to parse, in the standard format
    Returns:
        output_matrix: bi-dimensional array of 1 and 0
    """
    file = open(input_file, 'r')
    lines = file.readlines()
    output_matrix = []
    for line in lines:
        if line[0] != ';':
            line = clean(line)
            line_list = list(line)
            line_list = [int(i) for i in line_list]
            output_matrix.append(line_list)

    return output_matrix


def clean(line):
    """
    Remove the unnecessary part of a string
    Args:
        line: the line to clean
    Returns:
        line: cleaned line
    """
    line = line.replace(' ', '')
    line = line.replace('-', '')
    line = line.replace('\n', '')
    return line


