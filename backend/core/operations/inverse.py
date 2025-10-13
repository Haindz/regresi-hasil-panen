from matrix import Matrix

def inverse (matrix: Matrix) -> Matrix:
    """
    Menghitung matriks inverse dari objek Matrix menggunakan metode eliminasi Gauss-Jordan.
    Raises:
        ValueError: Jika matriks tidak bujur sangkar atau singular.
    """

    if matrix.rows != matrix.cols:
        raise ValueError("Matriks harus bujur sangkar (square) untuk di-inverse.")

    n = matrix.rows
    A = [row[:] for row in matrix.data]
    I = [[float(i == j) for j in range(n)] for i in range(n)]

    for i in range(n):
        diag = A[i][i]
        if diag == 0:
            raise ValueError("Matriks singular, tidak dapat di-invers.")
        for j in range(n):
            A[i][j] /= diag
            I[i][j] /= diag
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    I[k][j] -= factor * I[i][j]

    # Pastikan return objek Matrix!
    return Matrix(I)
