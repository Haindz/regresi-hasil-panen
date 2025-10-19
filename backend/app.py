from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from core.exporters.csv_importer import import_from_csv
from core.operations.regression import LinearRegression

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Aplikasi Regresi Hasil Panen</title>
            <style>
                body { font-family: Arial; background-color: #f4f4f4; text-align: center; margin-top: 100px; }
                h1 { color: #2c3e50; }
                button {
                    padding: 12px 24px;
                    font-size: 16px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                }
                button:hover { background-color: #2980b9; }
            </style>
        </head>
        <body>
            <h1>Selamat Datang di Aplikasi Regresi Hasil Panen</h1>
            <p>Klik tombol di bawah ini untuk memulai analisis Anda.</p>
            <button onclick="window.location.href='http://127.0.0.1:8080'">Mulai Analisis</button>
        </body>
    </html>
    """

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "File CSV tidak ditemukan"}), 400

    file = request.files['file']
    file_path = f"data/{file.filename}"
    file.save(file_path)

    try:
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)

        matrix = import_from_csv(file_path, skip_header=True)
        model = LinearRegression()
        X, y = model.split_features_target(matrix)
        beta = model.fit(X, y)
        y_pred = model.predict(X)

        return jsonify({
            "header": header,
            "koefisien": beta.data,
            "prediksi": y_pred.data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

