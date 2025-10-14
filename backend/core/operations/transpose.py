from core.matrix import Matrix

def transpose(matrix: Matrix) -> Matrix:
    """
    Mengembalikan transpose dari objek Matrix.
    """
    transposed_data = [
        [matrix.data[j][i] for j in range(matrix.rows)]
        for i in range(matrix.cols)
    ]
    return Matrix(transposed_data)

