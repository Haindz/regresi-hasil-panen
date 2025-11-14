from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from core.exporters.csv_importer import import_from_csv
from core.operations.regression import LinearRegression
from core.matrix import Matrix # <-- PENTING: Tambahkan import ini

app = Flask(__name__)
# Pastikan CORS mengizinkan semua origin untuk pengembangan
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    """ Halaman landing sederhana untuk backend. """
    return """
    <html>
        <head><title>Backend Regresi</title></head>
        <body>
            <h1>Server Backend Regresi Aktif</h1>
            <p>Endpoint /predict sedang menunggu kiriman POST.</p>
        </body>
    </html>
    """

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "File CSV tidak ditemukan"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nama file kosong"}), 400

    # Simpan file sementara
    file_path = f"data/{file.filename}"
    file.save(file_path)

    try:
        # --- 1. PERSIAPAN DATA ---
        # Impor data asli (untuk dikirim kembali ke frontend)
        matrix_full = import_from_csv(file_path, skip_header=True)
        # Impor data dengan header
        header_full = import_from_csv(file_path, skip_header=False).data[0]
        
        # --- 2. PERHITUNGAN REGRESI BERGANDA (UNTUK TEKS ANALISIS) ---
        model_multi = LinearRegression()
        X_multi, y_multi = model_multi.split_features_target(matrix_full)
        beta_multi = model_multi.fit(X_multi, y_multi)
        
        # --- 3. PERHITUNGAN REGRESI SEDERHANA (UNTUK GRAFIK VISUALISASI) ---
        # Ini adalah logika baru untuk memperbaiki masalah grafik Anda
        
        simple_visual_coeffs = {}
        feature_headers = header_full[:-1] # Semua header kecuali target (terakhir)
        target_col_index = matrix_full.cols - 1 # Indeks kolom target

        for i, feature_name in enumerate(feature_headers):
            # Buat matriks 2-kolom baru: [fitur_saat_ini, target]
            data_simple = []
            for row in matrix_full.data:
                feature_val = row[i]
                target_val = row[target_col_index]
                data_simple.append([feature_val, target_val])
            
            matrix_simple = Matrix(data_simple)
            
            # Latih model regresi sederhana (2D)
            model_simple = LinearRegression()
            # split_features_target akan otomatis mengambil kolom 0 sbg X, kolom 1 sbg Y
            X_simple, y_simple = model_simple.split_features_target(matrix_simple)
            beta_simple = model_simple.fit(X_simple, y_simple)
            
            # Simpan koefisien [intercept, slope] untuk fitur ini
            # .data akan berbentuk [[intercept], [slope]]
            simple_visual_coeffs[feature_name] = beta_simple.data

        # --- 4. KIRIM SEMUA HASIL KE FRONTEND ---
        return jsonify({
            "header": header_full,
            "original_data": matrix_full.data,         # Data mentah untuk plot titik
            "koefisien_multivariate": beta_multi.data, # Untuk teks "Hasil Analisis"
            "koefisien_visual": simple_visual_coeffs   # <-- Data baru untuk dropdown grafik
        })
    except Exception as e:
        # Berikan pesan error yang lebih jelas
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": f"Terjadi kesalahan di server: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
