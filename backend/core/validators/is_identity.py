# matriks/validators/is_identity.py

from matriks.matrix import Matrix
def is_identity(matriks):
    # 1. Cek matriks persegi
    jumlah_baris = len(matriks)
    jumlah_kolom = len(matriks[0]) if matriks else 0

    if jumlah_baris != jumlah_kolom:
        return False

    # 2. Periksa elemen
    for i in range(jumlah_baris):
        for j in range(jumlah_kolom):
            if i == j:
                # Elemen diagonal harus 1
                if matriks[i][j] != 1:
                    return False
            else:
                # Elemen non-diagonal harus 0
                if matriks[i][j] != 0:
                    return False

    # 3. Kalau semua sesuai, berarti identitas
    return True
