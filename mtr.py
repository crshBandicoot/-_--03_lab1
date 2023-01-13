matrix = []
m = 431
p = m*2+1
for i in range(m):
    row = []
    for j in range(m):
        if (2**i + 2**j) % p == 1 or (2**i - 2**j) % p == 1 or (-2**i + 2**j) % p == 1 or (-2**i - 2**j) % p == 1:
            row.append('1')
        else:
            row.append('0')
    row = tuple(row)
    matrix.append(row)

matrix = tuple(matrix)

with open('mul_matrix.txt', 'w+') as fout:
    fout.write(str(matrix))

