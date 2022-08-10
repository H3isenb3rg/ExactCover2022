def ec(matrix_a: list, size_m: int):
    cov = []
    
    for i, row in enumerate(matrix_a):
        if len(row) == 0:
            continue
        if len(row) == size_m:
            cov.append(i)
        
##TODO: continuare funzione EC