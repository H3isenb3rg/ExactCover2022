
cov = []
compatibility_matrix = []
symbols = []
matrix_parsed = []


def explore(indexes: list, union: list, intersection: list):
    for k in intersection:
        indexes_temp = indexes.append(k)
        union_temp = union.append(matrix_parsed[k])
        if union_temp == symbols:
            cov.append(indexes_temp)
        else:
            k_compatible = get_compatibles(compatibility_matrix, k)
            intersection_temp = list(set(intersection).intersection(k_compatible))
            if intersection_temp:
                explore(indexes_temp, union_temp, intersection_temp)


def get_compatibles(comp_matrix, i):
    compatible = []
    for j in range(len(comp_matrix[i])) - 1:
        line = comp_matrix[j]
        if line[i] == 1:
            compatible.append(j)
    return compatible


def all_symbols(matrix: list):
    m = []
    for row in matrix:
        for element in row:
            if element not in m:
                m.append(element)
    return m




