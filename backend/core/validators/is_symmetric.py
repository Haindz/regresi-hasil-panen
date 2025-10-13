# matriks/validators/is_symmetric.py

from matriks.matrix import Matrix
def is_symmetric(matriks):
    # 1. Cek matriks persegi
    jumlah_baris = len(matriks)
    jumlah_kolom = len(matriks[0]) if matriks else 0

    if jumlah_baris != jumlah_kolom:
        return False

    # 2. Cek kesimetrian elemen
    for i in range(jumlah_baris):
        for j in range(jumlah_kolom):
            if matriks[i][j] != matriks[j][i]:
                return False

    # 3. Kalau semua sesuai, berarti simetris
    return True

