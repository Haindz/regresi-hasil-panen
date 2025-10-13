from flask import Flask, request, jsonify
from core.exporters.csv_importer import import_from_csv
from core.operations.regression import LinearRegression
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🚜 API Regresi Linear Hasil Panen Aktif!"

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400

    filepath = os.path.join('/tmp', file.filename)
    file.save(filepath)

    matrix = import_from_csv(filepath, skip_header=True)
    model = LinearRegression()
    X, y = model.split_features_target(matrix)
    beta = model.fit(X, y)
    y_pred = model.predict(X, beta)

    return jsonify({
        'koefisien_regresi': beta.data,
        'hasil_prediksi': [row[0] for row in y_pred.data]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
