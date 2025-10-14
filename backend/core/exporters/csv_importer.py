import csv
from core.matrix import Matrix

def import_from_csv(file_path: str, delimiter: str = ',', skip_header: bool = False) -> Matrix:
    """
    Mengimpor data matriks dari file CSV dan mengembalikannya sebagai objek Matrix.

    Parameters
    ----------
    file_path : str
        Path file CSV yang akan dibaca.
    delimiter : str, default=','
        Karakter pemisah antar kolom (misalnya ',' atau ';' atau '\t').
    skip_header : bool, default=False
        Jika True, baris pertama CSV (header) akan dilewati.

    Returns
    -------
    Matrix
        Objek Matrix berisi data numerik dari CSV.
    """
    data = []
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)

            for i, row in enumerate(reader):
                # Lewati baris pertama kalau skip_header=True
                if skip_header and i == 0:
                    continue

                # Hapus spasi dan ubah ke float jika bisa
                parsed_row = []
                for val in row:
                    val = val.strip()
                    if val == "":
                        continue
                    try:
                        num = float(val)
                        parsed_row.append(num)
                    except ValueError:
                        parsed_row.append(val)  # tetap simpan string jika bukan angka

                if parsed_row:
                    data.append(parsed_row)

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' tidak ditemukan.")
    except Exception as e:
        raise RuntimeError(f"Gagal membaca file CSV: {e}")

    if not data:
        raise ValueError("File CSV kosong atau hanya berisi header.")

    return Matrix(data)
