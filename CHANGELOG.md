# Changelog

Semua perubahan penting pada paket **`dapodik-sdk`** (Python) akan didokumentasikan di file ini.

Format changelog ini mengacu pada [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/), dan proyek ini mematuhi [Semantic Versioning](https://semver.org/lang/id/).

---

## [1.0.0] - 2026-08-30

### Ditambahkan
- **Inisialisasi DapodikClient Core**:
  - Arsitektur **Zero Runtime Dependencies** menggunakan modul `urllib` bawaan Python Standard Library.
  - Normalisasi otomatis respons `rows` (objek tunggal `/getSekolah` vs list).
  - Wrapper respons `DapodikResponse` dengan dukungan method chaining `.filter()`, `.pluck()`, `.to_list()`, dan `.to_dataframe()`.
- **Dukungan Endpoint Lengkap (GET)**:
  - `get_sekolah`, `get_pengguna`, `get_gtk`, `get_rombongan_belajar`, `get_peserta_didik`, `get_mata_pelajaran`, `get_matev_nilai`.
- **Dukungan Operasi Tulis (POST)**:
  - `post_nilai` (pengiriman nilai rapor) dan `post_matev_rapor` (mata evaluasi).
- **Auto-Pagination & Streaming Generator**:
  - `fetch_all_peserta_didik`, `fetch_all_gtk` dengan callback `on_progress`.
  - Generator `iterate_peserta_didik` dan `iterate_gtk` untuk efisiensi RAM.
- **Integrasi Analisis Data**:
  - Konversi langsung ke **Pandas DataFrame** via `pip install "dapodik-sdk[dataframe]"`.
- **Pengujian & CI/CD**:
  - 9 Unit Tests menggunakan modul `unittest` dengan kelulusan 100%.
  - Workflow GitHub Actions untuk multi-Python testing (3.9 s.d. 3.13) dan auto-publishing ke PyPI via Trusted Publishing.
