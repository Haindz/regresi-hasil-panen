from core.matrix import Matrix
from core.operations.transpose import transpose
from core.operations.multiplier import multiply_matrices
from core.operations.inverse import inverse

class LinearRegression:
    """
    Implementasi sederhana regresi linear multivariat berbasis matriks.
    """
    def __init__(self):
        self.beta = None

    def fit(self, X, y):
        """
        Melatih model regresi linear: menghitung koefisien beta.
        """
        XT = transpose(X)
        XTX = multiply_matrices(XT, X)
        XTX_inv = inverse(XTX)
        XTy = multiply_matrices(XT, y)
        self.beta = multiply_matrices(XTX_inv, XTy)
        return self.beta

    def predict(self, X):
        """
        Melakukan prediksi berdasarkan koefisien beta yang sudah dilatih.
        """
        if self.beta is None:
            raise ValueError("Model belum dilatih. Jalankan .fit(X, y) terlebih dahulu.")
        return multiply_matrices(X, self.beta)

    def split_features_target(self, matrix, target_col=-1):
        """
        Memisahkan X (fitur) dan y (target) dari matriks CSV.
        Secara otomatis menangani jumlah kolom fitur berapa pun.
        """
        X_data = [row[:target_col] for row in matrix.data]
        y_data = [[row[target_col]] for row in matrix.data]

        # Tambahkan bias (kolom 1 di awal)
        X_with_bias = [[1.0] + row for row in X_data]

        X = Matrix(X_with_bias)
        y = Matrix(y_data)
        return X, y

