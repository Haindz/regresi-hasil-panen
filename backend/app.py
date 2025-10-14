from flask import Flask, request, jsonify
from core.exporters.csv_importer import import_from_csv
from core.operations.regression import LinearRegression
import os
import tempfile

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "API berhasil"}), 200


@app.route("/regresi", methods=["POST"])
def regresi():
    # Cek apakah ada file yang dikirim
    if "file" not in request.files:
        return jsonify({"error": "File CSV tidak ditemukan"}), 400

    file = request.files["file"]

    # Pastikan file CSV
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "File harus berformat .csv"}), 400

    # Simpan sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp:
        file.save(temp.name)
        temp_path = temp.name

    try:
        # Import file CSV jadi Matrix
        matrix = import_from_csv(temp_path, skip_header=True)

        # Jalankan regresi
        model = LinearRegression()
        X, y = model.split_features_target(matrix, target_col=-1)
        beta = model.fit(X, y)
        y_pred = model.predict(X, beta)

        # Format hasil jadi JSON
        response = {
            "koefisien_regresi": beta.data,
            "hasil_prediksi": y_pred.data
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Hapus file sementara
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
