from core.matrix import Matrix

def inverse(matrix: Matrix) -> Matrix:
    """
    Menghitung matriks inverse dari objek Matrix menggunakan eliminasi Gauss-Jordan
    DENGAN PARTIAL PIVOTING untuk stabilitas numerik.
    """

    if matrix.rows != matrix.cols:
        raise ValueError("Matriks harus bujur sangkar (square) untuk di-inverse.")

    n = matrix.rows
    # Buat salinan data untuk diubah (augmented matrix A)
    A = [row[:] for row in matrix.data] 
    # Buat matriks identitas yang akan menjadi inverse (augmented matrix I)
    I = [[float(i == j) for j in range(n)] for i in range(n)]

    for i in range(n):
        # ===============================================
        # BLOK PARTIAL PIVOTING (INI YANG BARU)
        # ===============================================
        # Cari baris dengan nilai absolut terbesar di kolom i, mulai dari baris i
        max_row = i
        max_val = abs(A[i][i])
        
        for k in range(i + 1, n):
            if abs(A[k][i]) > max_val:
                max_val = abs(A[k][i])
                max_row = k

        # Jika max_row bukan baris saat ini (i), tukar barisnya
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]  # Tukar baris di matriks A
            I[i], I[max_row] = I[max_row], I[i]  # Tukar baris di matriks I
        # ===============================================
        # AKHIR BLOK PIVOTING
        # ===============================================

        # Ambil nilai diagonal (pivot) SETELAH ditukar
        diag = A[i][i]

        # Sekarang cek singularitas. Jika masih 0, berarti benar-benar singular
        if abs(diag) < 1e-10: # Gunakan toleransi kecil, jangan '== 0'
            raise ValueError("Matriks singular, tidak dapat di-invers.")

        # 1. Jadikan elemen diagonal menjadi 1 (normalisasi baris pivot)
        # Bagilah seluruh baris (A dan I) dengan nilai diagonal
        for j in range(n):
            A[i][j] /= diag
            I[i][j] /= diag

        # 2. Jadikan elemen lain di kolom pivot ini menjadi 0
        for k in range(n):
            if k != i:  # Untuk semua baris LAIN (k) selain baris pivot (i)
                # Dapatkan faktor pengali (nilai di baris k, kolom pivot i)
                factor = A[k][i] 
                
                # Kurangkan (faktor * baris_pivot) dari baris_k
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    I[k][j] -= factor * I[i][j]

    # Matriks A sekarang sudah menjadi matriks identitas
    # Matriks I sekarang sudah menjadi matriks inverse
    return Matrix(I)
