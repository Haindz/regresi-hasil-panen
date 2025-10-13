# matriks/exporters/json_exporter.py
import json
def export_to_json(matriks, nama_file):
    # pastikan matriks bisa dikonversi ke list of lists
    data = matriks.data
    with open(nama_file, mode="w") as file:
        json.dump(data, file, indent=4)
    print(f"Sukses: Data matriks berhasil diekspor ke file JSON '{nama_file}'")
