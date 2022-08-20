# TODO: Print cov and other info to a file instead of saving it to a variable

def ec(matrix_a: list, size_m: int):
    cov = []
    matrix_b = []
    
    for i, row_i in enumerate(matrix_a):
        set_i = set(row_i)
        # Current set is empty
        if len(row_i) == 0:
            matrix_b.append([0 for i in range(size_m)])
            continue
        
        # Current set has all the elements
        if len(row_i) == size_m:
            cov.append(i)
            matrix_b.append([0 for i in range(size_m)])
        
        matrix_b.append([])
        for j, row_j in enumerate(matrix_a[:i]):
            set_j = set(row_j)
            if len(set_j.intersection(set_i)) == 0:
                matrix_b[i].append(0)
                continue
            
            indexes = (i, j)
            matrix_union = set_i.union(set_j)
            if len(matrix_union) == size_m:
                cov.append(indexes)
                matrix_b[i].append(0)
            else:
                matrix_b[i].append(1)
                inter = set(matrix_b[i][:-1]).intersection(set(matrix_b[j][:-1]))
                if len(inter) > 0:
                    # ESPLORA
                    pass
                
    return cov, matrix_b