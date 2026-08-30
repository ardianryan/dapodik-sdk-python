"""
Contoh Penggunaan Cepat Dapodik Python SDK
"""

import os
from dapodik import DapodikClient

# Ambil konfigurasi dari environment variable
NPSN = os.getenv("DAPODIK_NPSN", "20300001")
TOKEN = os.getenv("DAPODIK_TOKEN", "your_token_here")
HOST = os.getenv("DAPODIK_HOST", "127.0.0.1")
PORT = int(os.getenv("DAPODIK_PORT", 5774))

def main():
    print("🚀 Menginisialisasi DapodikClient...")
    client = DapodikClient(npsn=NPSN, token=TOKEN, host=HOST, port=PORT)

    print(f"Base URL: {client.base_url}")
    print(f"NPSN: {client.npsn}")

    # Catatan: Pemanggilan di bawah membutuhkan server Dapodik Desktop aktif di port 5774
    try:
        sekolah = client.get_sekolah()
        print("Nama Sekolah:", sekolah.first.get("nama") if sekolah.first else "N/A")

        pd = client.get_peserta_didik(page=1, limit=10)
        print("Jumlah Siswa Ditarik:", len(pd))
    except Exception as e:
        print("Info:", str(e))

if __name__ == "__main__":
    main()
