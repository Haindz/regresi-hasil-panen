from flask import Flask, request, jsonify
from core.exporters.csv_importer import import_from_csv
from core.operations.regression import LinearRegression
import os
import tempfile

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API Regresi Linear Hasil Panen aktif 🚀"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    """
    Jalankan regresi linear dari file CSV yang diunggah atau dari path tetap.
    """
    try:
        # Cek apakah file diunggah lewat form
        if 'file' in request.files:
            file = request.files['file']
            file_path = os.path.join("backend/data", file.filename)
            file.save(file_path)
        else:
            # Default: pakai dataset bawaan
            file_path = "backend/data/hasil_panen_id.csv"

        # Import CSV
        matrix = import_from_csv(file_path, skip_header=True)

        # Jalankan regresi
        model = LinearRegression()
        X, y = model.split_features_target(matrix, target_col=-1)
        beta = model.fit(X, y)
        y_pred = model.predict(X, beta)

        # Format hasil ke JSON
        results = {
            "coefficients": beta.data,
            "predictions": [row[0] for row in y_pred.data]
        }

        return jsonify({
            "message": "Regresi linear berhasil dijalankan ✅",
            "file_used": file_path,
            "results": results
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
