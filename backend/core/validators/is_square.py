# matriks/validator/is_square.py

from matriks.matrix import Matrix
def is_square(matrix):
    """
    Mengecek apakah matriks berbentuk persegi
    """
    if not matrix:
        return False
    jumlah_baris = len(matrix)
    jumlah_kolom = len(matrix[0])
    return jumlah_baris == jumlah_kolom
