# matriks/operations/find_determinant.py

from matriks.matrix import Matrix
def find_determinant(matrix):
    """
    Menghitung determinan matriks persegi
    (menggunakan ekspansi Laplace rekursif)
    """
    if not is_square(matrix):
        raise ValueError("Matriks harus persegi untuk menghitung determinan")

    n = len(matrix)

    # Basis 1x1
    if n == 1:
        return matrix[0][0]

    # Basis 2x2
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    # Rekursi untuk nxn
    det = 0
    for col in range(n):
        submatrix = [row[:col] + row[col+1:] for row in matrix[1:]]
        det += ((-1) ** col) * matrix[0][col] * find_determinant(submatrix)

    return det
