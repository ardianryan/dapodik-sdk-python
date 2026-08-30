<p align="center">
  <img src="https://dapo.kemendikdasmen.go.id/assets/logo-dapodik-BZDG7c6h.png" alt="Dapodik Logo" width="140" />
</p>

<h1 align="center">dapodik-sdk (Python)</h1>

<p align="center">
  <a href="https://pypi.org/project/dapodik-sdk/"><img src="https://img.shields.io/pypi/v/dapodik-sdk.svg?style=flat-square" alt="PyPI version" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License: MIT" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-%3E%3D3.9-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python Version" /></a>
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/Pandas-Ready-150458.svg?style=flat-square&logo=pandas&logoColor=white" alt="Pandas Ready" /></a>
  <a href="https://www.instagram.com/smansagewithai/"><img src="https://img.shields.io/badge/Instagram-@smansagewithai-E4405F.svg?style=flat-square&logo=instagram&logoColor=white" alt="Instagram" /></a>
</p>

<p align="center">
  SDK Python modern, ringan (<i>Zero Runtime Dependencies</i>), dan <i>type-safe</i> untuk integrasi penarikan data <b>WebService Dapodik Kemendikdasmen</b> (port 5774).
</p>

<p align="center">
  Dipublikasikan dan dikelola oleh <b>SMA Negeri 1 Gedeg (<a href="https://www.instagram.com/smansagewithai/">@smansagewithai</a>)</b><br />
  Dikembangkan oleh <b>Ryan Ardian</b>
</p>

---

> [!IMPORTANT]
> ### 📢 Pernyataan Penyangkalan (Disclaimer) & Misi Terbuka
> **`dapodik-sdk` adalah pustaka *Unofficial* (tidak resmi) dan independen.** Pustaka ini dikembangkan sebagai inisiatif komunitas sumber terbuka (*open-source*) oleh **SMA Negeri 1 Gedeg** dan **Ryan Ardian**, tanpa afiliasi langsung secara struktural dengan Kementerian Pendidikan Dasar dan Menengah (Kemendikdasmen).
>
> **Tujuan & Misi Pengembangan**:
> Pustaka ini lahir atas semangat memajukan transformasi digital dan interoperabilitas sistem pendidikan di Indonesia. Tujuan utamanya adalah **memberdayakan para pengembang perangkat lunak lintas platform dan multi-bahasa pemrograman** (Python, TypeScript, Node.js, PHP, Laravel, dll.) agar dapat mengintegrasikan sistem informasi sekolah, LMS, E-Rapor, presensi cerdas, serta analitik data pendidikan secara lebih cepat, aman, terstandarisasi, dan terbebas dari kompleksitas teknis protokol WebService lokal Dapodik.
>
> Seluruh hak cipta nama, logo, dan merek dagang **Dapodik (Data Pokok Pendidikan)** adalah milik sah **Kementerian Pendidikan Dasar dan Menengah Republik Indonesia**.

---

## 🏛️ Latar Belakang & Referensi

Pustaka ini merupakan modernisasi dan porting ekosistem **Python** yang mengadaptasi spesifikasi integrasi WebService Dapodik dari repositori referensi karya **Ade Reksi Susanto** ([`adereksisusanto/dapodik-api-php`](https://github.com/adereksisusanto/dapodik-api-php)).

Versi Python ini dirancang khusus untuk pengolahan data analitik, AI/Machine Learning, integrasi backend (**FastAPI, Django, Flask**), data pipeline (**Airflow, Celery**), maupun otomasi skrip harian dengan dukungan konversi langsung ke **Pandas DataFrame** dan **Excel**.

---

## ⚡ Keunggulan Utama

- 🪶 **Zero Runtime Dependencies**: Bekerja murni menggunakan *Python Standard Library* bawaan tanpa mewajibkan instalasi paket luar.
- 🐼 **Integrasi Instan Pandas & Excel**: Ekspor data siswa, guru, atau rombel langsung ke Pandas DataFrame (`.to_dataframe()`) atau file `.xlsx` / `.csv`.
- 🔄 **Auto-Pagination Generator**: Tarik ribuan data siswa tanpa khawatir kehabisan memori RAM dengan generator streaming.
- 🛡️ **Kepatuhan UU PDP No. 27/2022**: Dilengkapi panduan kepatuhan perlindungan data pribadi siswa/guru Indonesia.
- 🧩 **Dukungan Operasi Tulis (POST)**: Mengirim nilai rapor (`post_nilai`) dan mata evaluasi (`post_matev_rapor`).

---

## ⚠️ Kepatuhan UU Perlindungan Data Pribadi (UU PDP No. 27/2022)

Aplikasi Dapodik memproses **Data Pribadi Siswa dan Guru** (NIK, NISN, no kontak, data orang tua). Pengembang wajib mematuhi **UU Perlindungan Data Pribadi No. 27 Tahun 2022 Pasal 67**. Jaga kerahasiaan token dan dilarang memublikasikan atau menyalahgunakan data tanpa hak.

---

## 📥 Instalasi

Pasang paket melalui pip:

```bash
pip install dapodik-sdk
```

*(Opsional) Jika ingin menggunakan fitur konversi Pandas DataFrame:*
```bash
pip install "dapodik-sdk[dataframe]"
```

---

## 🚀 Quickstart & Contoh Penggunaan

### 1. Inisialisasi Klien Dasar

```python
from dapodik import DapodikClient

# Inisialisasi client
client = DapodikClient(
    npsn="20300001",
    token="TOKEN_WEBSERVICE_DAPODIK",
    host="192.168.1.100",  # IP Komputer Dapodik
    port=5774              # Default port Dapodik
)

# 1. Ambil Profil Sekolah
sekolah = client.get_sekolah()
print(f"Sekolah: {sekolah.first['nama']}")

# 2. Ambil Data Siswa (50 baris pertama)
siswa = client.get_peserta_didik(page=1, limit=50)
print(f"Total ditarik: {len(siswa)} siswa")

# 3. Filter data bawaan SDK
siswa_laki = siswa.filter(jenis_kelamin="L")
print(f"Jumlah siswa laki-laki: {len(siswa_laki)}")
```

---

### 2. Ekspor Instan ke Pandas DataFrame & Excel 📊

```python
from dapodik import DapodikClient

client = DapodikClient(npsn="20300001", token="TOKEN_DAPODIK")

# Tarik seluruh siswa sekolah secara otomatis
semua_siswa = client.fetch_all_peserta_didik(limit=100)

# Konversi langsung ke Pandas DataFrame
df = semua_siswa.to_dataframe()

print(df[["nama", "nisn", "jenis_kelamin", "tempat_lahir"]].head())

# Ekspor ke Excel
df.to_excel("data_siswa_dapodik.xlsx", index=False)
print("Berhasil diekspor ke data_siswa_dapodik.xlsx!")
```

---

### 3. Integrasi ke Backend Modern (FastAPI) ⚡

```python
from fastapi import FastAPI, HTTPException
from dapodik import DapodikClient, DapodikAuthError

app = FastAPI(title="Dapodik API Service")

client = DapodikClient(
    npsn="20300001",
    token="TOKEN_DAPODIK",
    host="127.0.0.1"
)

@app.get("/api/sekolah")
def get_sekolah():
    try:
        resp = client.get_sekolah()
        return resp.first
    except DapodikAuthError:
        raise HTTPException(status_code=401, detail="Token Dapodik tidak valid")

@app.get("/api/siswa")
def get_siswa(page: int = 1, limit: int = 50):
    return client.get_peserta_didik(page=page, limit=limit).to_list()
```

---

## 🔄 Auto-Pagination & Streaming (RAM Efisien)

Untuk sekolah dengan ribuan data, gunakan Generator Stream:

```python
# Stream per-batch 100 siswa (hemat RAM)
for batch in client.iterate_peserta_didik(limit=100):
    print(f"Memproses batch berisi {len(batch)} siswa...")
    for siswa in batch:
        print(f" - {siswa['nama']} ({siswa['nisn']})")
```

---

## 📋 Daftar Endpoint Lengkap

| Endpoint WebService | Method Standar | Method Alias | Deskripsi |
| :--- | :--- | :--- | :--- |
| **`/getSekolah`** | `client.get_sekolah()` | `client.sekolah()` | Profil & izin operasional sekolah |
| **`/getPengguna`** | `client.get_pengguna()` | `client.pengguna()` | Akun operator & pengguna Dapodik |
| **`/getGtk`** | `client.get_gtk(page, limit)` | `client.gtk()` | Data Guru & Tenaga Kependidikan |
| **`/getRombonganBelajar`** | `client.get_rombongan_belajar(sem)` | `client.rombel()` | Data rombel beserta anggota & mapel |
| **`/getPesertaDidik`** | `client.get_peserta_didik(page, limit)` | `client.pd()` | Data seluruh siswa lengkap |
| **`/getMataPelajaran`** | `client.get_mata_pelajaran(sem)` | `client.mata_pelajaran()` | Referensi mata pelajaran nasional |
| **`/getMatevNilai`** | `client.get_matev_nilai(sem)` | `client.matev_nilai()` | Referensi mata evaluasi nilai |
| **`/postNilai`** | `client.post_nilai(body, table)` | - | Pengiriman nilai rapor (HTTP POST) |
| **`/postMatevRapor`** | `client.post_matev_rapor(body)` | - | Pengiriman mata evaluasi (HTTP POST)|

---

## 📄 Lisensi & Kontributor

- **Lisensi**: [MIT License](LICENSE) &copy; 2026 **Ryan Ardian, SMA Negeri 1 Gedeg (smansage)**.
- **Pengembang**: **Ryan Ardian** ([inisaya@ardianryan.com](mailto:inisaya@ardianryan.com)).
- **Inspirasi & Atribusi**: Adaptasi pustaka PHP Dapodik oleh **Ade Reksi Susanto** ([`adereksisusanto/dapodik-api-php`](https://github.com/adereksisusanto/dapodik-api-php)).
