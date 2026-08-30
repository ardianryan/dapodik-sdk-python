# Panduan Kontribusi (Contributing Guidelines)

Terima kasih telah tertarik berkontribusi pada pengembangan **`dapodik-sdk`** untuk Python!

---

## 🛠️ Pengembangan Lokal

1. **Fork** repositori ini ke akun GitHub Anda.
2. **Clone** hasil fork:
   ```bash
   git clone https://github.com/ardianryan/dapodik-sdk-python.git
   cd dapodik-sdk-python
   ```
3. **Jalankan Pengujian Unit**:
   ```bash
   python3 -m unittest discover -s tests -p "test_*.py"
   ```

---

## 🌿 Standar Kode & Pull Request

1. Ikuti kaidah **PEP 8** dan sertakan type annotations (*PEP 484*).
2. Pastikan seluruh pengujian unit lulus 100%.
3. Gunakan pesan commit deskriptif (*Conventional Commits*).
