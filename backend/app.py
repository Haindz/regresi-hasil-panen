from flask import Flask, request, jsonify
from core.exporters.csv_importer import import_from_csv
from core.operations.regression import LinearRegression

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "File CSV tidak ditemukan"}), 400

    file = request.files['file']
    file_path = f"data/{file.filename}"
    file.save(file_path)

    try:
        matrix = import_from_csv(file_path, skip_header=True)
        model = LinearRegression()
        X, y = model.split_features_target(matrix)
        beta = model.fit(X, y)
        y_pred = model.predict(X)

        return jsonify({
            "koefisien": beta.data,
            "prediksi": y_pred.data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)

