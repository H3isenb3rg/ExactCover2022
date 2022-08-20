
cov = []
matrix_b = []
symbols = []
matrix_parsed = []


def explore(indexes: list, matrix_union: list, inter: list):
    for k in inter:
        indexes_temp = indexes.append(k)
        union_temp = matrix_union.append(matrix_parsed[k])
        if union_temp == symbols:
            cov.append(indexes_temp)
        else:
            intersection_temp = list(set(inter).intersection(set(matrix_b[k][:-1])))
            if intersection_temp:
                explore(indexes_temp, union_temp, intersection_temp)


