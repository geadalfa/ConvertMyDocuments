# ConvertMyDocuments (v1.1.1)
### Zero-Leakage Offline Document & OCR Desktop Suite for Windows

[![License: Non-Commercial](https://img.shields.io/badge/License-PolyForm%20NonCommercial-blue.svg)](LICENSE)
[![Privacy: 100% Offline](https://img.shields.io/badge/Privacy-100%25%20Offline%20(Localhost)-emerald.svg)](#-jaminan-privasi-mutlak-kami-tidak-mengambil-data-anda)
[![Compliance: UU PDP RI](https://img.shields.io/badge/Kepatuhan-UU%20PDP%20No.%2027%2F2022-brightgreen.svg)](#-kepatuhan-undang-undang-perlindungan-data-pribadi-uu-pdp)
[![Language: Bilingual](https://img.shields.io/badge/Language-English%20%7C%20Indonesia-blueviolet.svg)](#-fitur-unggulan)
[![Platform: Windows 10/11](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20(64--bit)-lightgrey.svg)](#-unduh--instalasi)
[![Release: v1.1.1](https://img.shields.io/badge/Release-v1.1.1-blue.svg)](https://github.com/geadalfa/ConvertMyDocuments/releases/tag/v1.1.1)

Aplikasi desktop Windows mandiri, modern, dan berkecepatan tinggi untuk mengonversi dokumen PDF, gambar, scan berkas, dan faktur ber-watermark menjadi Word (`.docx`), teks (`.txt`), dan PDF (`.pdf`) **tanpa mengunggah satu byte pun data ke internet**.

---

> ## 🛡️ Jaminan Privasi Mutlak: KAMI TIDAK MENGAMBIL DATA ANDA
>
> Banyak situs web converter online gratis di internet diam-diam menyimpan, menganalisis, atau berpotensi mengekspos isi dokumen rahasia Anda ke server pihak ketiga di luar negeri.
>
> **ConvertMyDocuments dibangun dengan filosofi *Privacy-First & Zero-Leakage*:**
>
> 1. **100% Pemrosesan Lokal (Localhost `127.0.0.1`):** Seluruh proses pembacaan tata letak, ekstraksi teks, konversi tabel, dan rekonstruksi gambar berjalan murni di memori RAM dan CPU/GPU komputer lokal Anda.
> 2. **Tanpa Koneksi Cloud / Web Luar:** Aplikasi tidak memerlukan koneksi internet untuk bekerja. Anda bahkan dapat menggunakannya saat komputer dalam mode *Airplane Mode* (Offline total).
> 3. **Pembersihan Memori Otomatis:** Semua berkas raster sementara (*temporary buffer*) dimusnahkan secara aman dari disk seketika proses selesai.
>
> ### 🇮🇩 Kepatuhan Undang-Undang Perlindungan Data Pribadi (UU PDP)
> Aplikasi ini dirancang untuk memenuhi ketentuan **Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP)**. Hak atas kerahasiaan dokumen rahasia—seperti KTP, NPWP, slip gaji, rekam medis, dokumen perbankan, dan surat perjanjian hukum—sepenuhnya terlindungi karena **data tidak pernah ditransmisikan, dikumpulkan, atau dibagikan kepada siapa pun**.

---

## ✨ Fitur Unggulan

### 🌐 Antarmuka Dwibahasa (Bilingual: English & Bahasa Indonesia)
- **Default Bahasa Inggris (English):** Menyesuaikan standar perangkat lunak internasional.
- **Dukungan Penuh Bahasa Indonesia:** Seluruh menu, teks bantuan, status konversi, dan pratinjau diterjemahkan secara akurat.
- **Penyimpanan Pengaturan Otomatis (Persistent Session):** Saat Anda beralih bahasa (EN atau ID), preferensi Anda otomatis disimpan di profil pengguna komputer. Ketika aplikasi dibuka kembali di sesi berikutnya, bahasa yang Anda pilih akan tetap aktif tanpa perlu diatur ulang.

### 1. PDF ke Word (.docx) — Presisi Tinggi & Identik PDF
- **Tata Letak Identik:** Mempertahankan ukuran halaman asli (termasuk format presentasi 16:9 Widescreen, A4, atau Letter), margin, padding, perataan, dan spasi antar baris.
- **Font & Tipografi Asli:** Mempertahankan jenis huruf, ukuran font (*pt*), ketebalan (*bold*), miring (*italic*), serta warna teks asli.
- **Gambar Tetap Gambar:** Diagram, screenshot, logo, dan karya seni visual di dalam PDF diekstrak dalam resolusi aslinya dan disematkan langsung sebagai gambar di Word—tidak rusak atau diubah menjadi teks acak.
- **Tabel Otomatis:** Garis pembatas dan sel tabel PDF dikonversi menjadi tabel asli Word (*Table Grid*) yang rapi dan terstruktur.
- **Teks 100% Dapat Diedit:** Bebas diedit, ditambah, atau disalin di Microsoft Word.
- **Auto-OCR untuk Scanned PDF:** Jika halaman tidak memiliki layer teks (hasil foto/scan), mesin AI RapidOCR offline otomatis membaca teks gambar tersebut.

### 2. PDF ke Teks (.txt)
- Ekstraksi teks digital secepat kilat dengan pemisah halaman yang jelas (`--- Halaman X ---`).
- Dilengkapi **Pratinjau Teks Langsung** di aplikasi dan tombol 1-klik **"Salin ke Clipboard"**.

### 3. JPG / Gambar ke PDF (.pdf)
- Menggabungkan banyak gambar/foto (*batch merge*) format JPG, PNG, WebP, BMP, dan TIFF menjadi satu dokumen PDF berkualitas tinggi.
- Pilihan tata letak: **Ukuran Asli Gambar (Fit Resolution)**, **Kertas A4 Portrait**, atau **Kertas A4 Landscape**.

### 4. JPG / Gambar ke Word (.docx)
- Mengekstrak teks dari foto struk, kwitansi, dokumen fisik, atau tangkapan layar ber-watermark menggunakan teknologi RapidOCR offline.
- Dilengkapi fitur **Pemutihan Watermark** (OpenCV thresholding) untuk membersihkan latar belakang kertas kotor/stempel transparan.

---

## 🚀 Unduh & Instalasi

Pilih salah satu cara instalasi di bawah ini dari [Halaman GitHub Releases](https://github.com/geadalfa/ConvertMyDocuments/releases/tag/v1.1.1):

| Berkas Unduhan | Tipe | Keterangan |
| :--- | :--- | :--- |
| **[`ConvertMyDocuments_Setup_v1.1.1.exe`](https://github.com/geadalfa/ConvertMyDocuments/releases/download/v1.1.1/ConvertMyDocuments_Setup_v1.1.1.exe)** | **Installer Resmi (Direkomendasikan)** | Cukup unduh dan jalankan. Otomatis membuat ikon di Desktop & Start Menu. Tidak butuh akses administrator (UAC). |
| **[`ConvertMyDocuments-v1.1.1-portable.zip`](https://github.com/geadalfa/ConvertMyDocuments/releases/download/v1.1.1/ConvertMyDocuments-v1.1.1-portable.zip)** | **Versi Portable** | Ekstrak berkas ZIP di folder mana saja dan langsung jalankan `ConvertMyDocuments.exe`. |

### Kebutuhan Sistem
- **Sistem Operasi:** Windows 10 atau Windows 11 (64-bit)
- **Browser Pendukung:** Microsoft Edge (bawaan Windows untuk menjalankan mode Desktop App)
- **Koneksi Internet:** Tidak diperlukan (100% Offline)

---

## 🛠️ Menjalankan dari Source Code (Bagi Pengembang)

Jika Anda ingin menjalankan aplikasi langsung dari *source code*:

```powershell
# 1. Clone repositori
git clone https://github.com/geadalfa/ConvertMyDocuments.git
cd ConvertMyDocuments

# 2. Install dependensi Python (Python 3.10 / 3.11 direkomendasikan)
pip install -r requirements.txt

# 3. Jalankan aplikasi
python server.py
```

### Menjalankan Pengujian (Unit Test & QA Test Suite)
```powershell
python -m unittest discover -s tests
```

---

## 📜 Lisensi & Ketentuan Penggunaan (Non-Commercial Open Source)

Aplikasi ini berlisensi di bawah **[PolyForm Noncommercial License 1.0.0](LICENSE)**.

- ✅ **Bebas Digunakan:** Untuk keperluan pribadi, keluarga, riset akademis, edukasi, dan organisasi nirlaba secara gratis.
- ✅ **Bebas Dimodifikasi & Dikembangkan:** Kode sumber terbuka bagi siapa saja yang ingin belajar atau berkontribusi.
- ❌ **DILARANG KERAS DIKOMERSIALKAN:** Aplikasi ini **TIDAK BOLEH** dijual, diperjualbelikan, dipaketkan ke dalam produk berbayar, atau dijadikan layanan konversi berbayar komersial dalam bentuk apa pun.

---

<p align="center">
  Dibuat dengan ❤️ untuk menjaga privasi dokumen pengguna Indonesia.<br>
  <b>ConvertMyDocuments</b> — <i>Zero-Leakage Local Document & OCR Suite</i>
</p>
