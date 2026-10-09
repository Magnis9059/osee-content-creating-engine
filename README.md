# 🚀 OSEE Content Studio Web App

Web Application & Automation Engine untuk produksi konten multi-brand OSEE (`osee.co.id`, `One Stop English Education`, `osee digital`), auto-stamping logo resmi, scraping hari besar nasional, dan integrasi penjadwalan Aidelly.

---

## 🌟 Fitur Utama
1. **Frontend Dashboard Responsif**:
   * Pemisahan workspace tab (`osee.co.id`, `One Stop English Education`, `osee digital`).
   * Input custom keyword / topik spesifik.
   * Generate draft konten lengkap (headline, subheadline, 4 badge/bullet points, CTA, caption IG/FB/Threads, dan locked visual prompt).
2. **Scraping Hari Besar Indonesia**:
   * Scraper kalender hari libur nasional & momentum nasional/internasional tiap bulan.
   * Rekomendasi otomatis angle topik konten yang cocok dengan niche masing-masing workspace (1-klik langsung masuk ke form).
3. **Upcoming / Scheduled Content Preview**:
   * Monitoring jadwal postingan yang sudah antre di Aidelly secara live.
4. **Cloud-Ready Deployment**:
   * Konfigurasi lengkap untuk Railway via Dockerfile / Procfile.

---

## 🛠️ Menjalankan Lokal

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Jalankan server lokal
python app.py
# atau: uvicorn app:app --reload --port 8080
```
Buka browser di: `http://localhost:8080`

---

## ☁️ Tutorial Push ke GitHub & Deploy ke Railway

### Langkah 1: Push ke GitHub Anda
1. Buat repository baru di [GitHub](https://github.com/new), misalnya beri nama: `osee-content-studio`.
2. Di terminal PowerShell pada folder ini, jalankan:
```powershell
# Ganti URL di bawah dengan repository GitHub Anda
git remote add origin https://github.com/USERNAME-ANDA/osee-content-studio.git
git push -u origin main
```

### Langkah 2: Deploy ke Railway
1. Buka [Railway.app](https://railway.app/) dan login.
2. Klik tombol **New Project** -> pilih **Deploy from GitHub repo**.
3. Pilih repository `osee-content-studio`.
4. Masuk ke tab **Variables** pada service di Railway, tambahkan environment variable:
   * `AIDELLY_TOKEN` = `aidelly_live_CB3CiaBjfAc3pK5sK_bcHP5e489QS6Az`
   * `PREFERRED_IMAGE_MODEL` = `gemini-3.8-flash`
   * `PORT` = `8080`
5. Masuk ke tab **Settings** -> bagian **Networking** -> klik **Generate Domain**.
6. Web app Anda langsung aktif dan live di internet!
