from core.matrix import Matrix
from core.operations.multiplier import multiply_matrices as multiply
from core.operations.inverse import inverse
from core.operations.transpose import transpose
import numpy as np

class LinearRegression:
    def __init__(self):
        self.coef_ = None

    def fit(self, X: Matrix, y: Matrix) -> Matrix:
        """Melatih model regresi linier: beta = (X^T X)^(-1) X^T y"""
        X_T = transpose(X)
        XTX = multiply(X_T, X)

        # Coba inverse biasa, fallback ke pseudo-inverse jika singular
        try:
            XTX_inv = inverse(XTX)
        except ValueError:
            print("⚠️ Matriks singular, gunakan pseudo-inverse.")
            XTX_inv_np = np.linalg.pinv(np.array(XTX.data))
            XTX_inv = Matrix(XTX_inv_np.tolist())

        XTy = multiply(X_T, y)
        beta = multiply(XTX_inv, XTy)

        self.coef_ = beta
        return beta

    def predict(self, X: Matrix) -> Matrix:
        """Prediksi nilai y berdasarkan X dan koefisien yang sudah dilatih"""
        if self.coef_ is None:
            raise ValueError("Model belum dilatih. Jalankan fit() terlebih dahulu.")
        return multiply(X, self.coef_)

    def split_features_target(self, matrix, target_col=-1):
        """
        Memisahkan fitur (X) dan target (y) dari matriks.
        Menambahkan kolom 1 (intercept) di awal X.
        """
        X_data = [row[:target_col] for row in matrix.data]
        y_data = [[row[target_col]] for row in matrix.data]

        # Tambahkan intercept (kolom 1 di depan)
        X_with_intercept = [[1.0] + row for row in X_data]

        return Matrix(X_with_intercept), Matrix(y_data)
