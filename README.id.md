# ConvertMyDocuments

[English](README.md) | **Bahasa Indonesia**

[![Lisensi: Non-Komersial](https://img.shields.io/badge/Lisensi-PolyForm%20NonCommercial-blue.svg)](LICENSE)
[![Privasi: 100% Offline](https://img.shields.io/badge/Privasi-100%25%20Offline%20(Localhost)-10b981.svg)](#jaminan-privasi-dan-model-keamanan)
[![Kepatuhan: UU PDP No. 27/2022](https://img.shields.io/badge/Kepatuhan-UU%20PDP%20No.%2027%2F2022-brightgreen.svg)](#kepatuhan-regulasi-uu-pdp-indonesia)
[![Bahasa: Dwibahasa](https://img.shields.io/badge/UI-English%20%7C%20Bahasa%20Indonesia-blueviolet.svg)](#antarmuka-dwibahasa-dan-penyimpanan-sesi)
[![Platform: Windows 10/11](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20(64--bit)-lightgrey.svg)](#unduh-dan-instalasi)
[![Rilis: v1.1.1](https://img.shields.io/badge/Rilis-v1.1.1-blue.svg)](https://github.com/geadalfa/ConvertMyDocuments/releases/tag/v1.1.1)

ConvertMyDocuments adalah aplikasi desktop Windows mandiri untuk mengonversi berkas PDF, pindaian, dan gambar menjadi dokumen Microsoft Word (`.docx`), teks polos (`.txt`), serta PDF (`.pdf`) tanpa mengirimkan data ke jaringan luar.

---

## Jaminan Privasi dan Model Keamanan

Layanan konversi berbasis web pada umumnya mengunggah berkas pengguna ke server pihak ketiga, yang dapat membuka risiko penyimpanan berkas rahasia tanpa izin atau kebocoran data.

ConvertMyDocuments menghilangkan risiko tersebut melalui pemrosesan lokal penuh:

1. **Pemrosesan Khusus Localhost (`127.0.0.1`):** Seluruh tahapan parsing tata letak, inferensi OCR, rekonstruksi tabel, dan pembuatan dokumen berjalan eksklusif di memori CPU/GPU komputer lokal.
2. **Nol Pengiriman Data (Zero Telemetry):** Aplikasi tidak melakukan panggilan HTTP, DNS, atau koneksi soket ke internet. Aplikasi tetap berfungsi penuh saat komputer berada dalam mode Pesawat (Airplane Mode).
3. **Pembersihan Berkas Sementara:** Seluruh berkas raster sementara dan buffer memori langsung dihapus dari disk segera setelah tugas konversi selesai.

### Kepatuhan Regulasi: UU PDP Indonesia

ConvertMyDocuments dirancang sesuai dengan standar **Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP)**. Dokumen sensitif—seperti KTP, NPWP, slip gaji, rekam medis, rekening koran perbankan, dan dokumen perjanjian hukum—tetap sepenuhnya berada dalam kendali perangkat pengguna tanpa pernah ditransmisikan ke pihak luar.

---

## Fitur Utama

### 1. PDF ke Word (`.docx`) dengan Presisi Tata Letak
- **Rekonstruksi Tata Letak Asli:** Mempertahankan dimensi halaman asli (termasuk format presentasi 16:9 Widescreen, A4, dan Letter), batas margin, spasi baris, dan perataan teks.
- **Tipografi Asli:** Mempertahankan jenis huruf, ukuran font (*pt*), atribut tebal/miring, serta kode warna teks.
- **Ekstraksi Gambar Utuh:** Gambar vektor, diagram alir, logo, dan foto di dalam PDF diekstrak dalam resolusi aslinya dan disematkan langsung sebagai objek gambar Word tanpa diubah menjadi teks acak.
- **Konversi Tabel:** Mengubah garis batas dan sel tabel PDF menjadi tabel asli Microsoft Word (*Table Grid*) yang dapat diedit.
- **Auto-OCR untuk Halaman Pindaian:** Halaman PDF tanpa lapisan teks (hasil foto atau scan) otomatis dialihkan ke mesin inferensi RapidOCR ONNX lokal.

### 2. PDF ke Teks (`.txt`)
- Ekstraksi teks digital dari PDF dengan pembatas halaman terstruktur (`--- Halaman X ---`).
- Dilengkapi penampil pratinjau teks dan tombol salin ke clipboard dalam 1 klik.

### 3. Gambar ke PDF (`.pdf`)
- Menggabungkan berkas gambar (JPEG, PNG, WebP, BMP, TIFF) menjadi satu dokumen PDF.
- Mendukung tiga pilihan tata letak:
  - **Ukuran Asli (Fit Resolution):** Mengikuti aspek rasio asli gambar.
  - **A4 Portrait:** Menyesuaikan gambar ke kertas standar A4 tegak.
  - **A4 Landscape:** Menyesuaikan gambar ke kertas standar A4 mendatar.

### 4. Gambar ke Word (`.docx`) via RapidOCR
- Mengekstrak teks dari foto struk, kwitansi, atau dokumen fisik menjadi berkas Word.
- **Pemutihan Watermark Adaptif:** Menggunakan thresholding OpenCV untuk membersihkan stempel transparan, cap air, atau noda kertas sebelum teks dibaca OCR.

---

## Antarmuka Dwibahasa dan Penyimpanan Sesi

ConvertMyDocuments mendukung antarmuka dalam **Bahasa Inggris** dan **Bahasa Indonesia**:

- **Bahasa Bawaan:** Bahasa Inggris digunakan secara default pada instalasi baru.
- **Pengalih Bahasa di Header:** Pengguna dapat berpindah bahasa secara instan melalui tombol `[ EN | ID ]` di bagian kanan atas antarmuka.
- **Penyimpanan Preferensi:** Bahasa yang dipilih otomatis tersimpan ke `%LOCALAPPDATA%\ConvertMyDocuments\settings.json` dan penyimpanan browser, sehingga tetap aktif saat aplikasi dibuka pada sesi berikutnya.

---

## Unduh dan Instalasi

Berkas biner mandiri untuk Windows 64-bit tersedia di [Halaman GitHub Releases](https://github.com/geadalfa/ConvertMyDocuments/releases/tag/v1.1.1):

| Berkas | Tipe | Keterangan |
| :--- | :--- | :--- |
| **[`ConvertMyDocuments_Setup_v1.1.1.exe`](https://github.com/geadalfa/ConvertMyDocuments/releases/download/v1.1.1/ConvertMyDocuments_Setup_v1.1.1.exe)** | Installer Resmi (Direkomendasikan) | Installer Inno Setup standar. Berjalan pada izin pengguna tanpa memerlukan elevasi Administrator (UAC). Otomatis membuat pintasan Desktop dan Start Menu. |
| **[`ConvertMyDocuments-v1.1.1-portable.zip`](https://github.com/geadalfa/ConvertMyDocuments/releases/download/v1.1.1/ConvertMyDocuments-v1.1.1-portable.zip)** | Berkas Portabel | Cukup ekstrak ke folder mana saja dan jalankan `ConvertMyDocuments.exe` langsung tanpa instalasi. |

### Kebutuhan Sistem
- **Sistem Operasi:** Windows 10 (64-bit) atau Windows 11 (64-bit).
- **Runtime Host:** Microsoft Edge (bawaan Windows 10/11, dijalankan dalam mode App tanpa antarmuka peramban).
- **Koneksi Jaringan:** Tidak diperlukan (100% offline).

---

## Menjalankan dari Kode Sumber

Bagi pengembang yang ingin memeriksa atau menjalankan aplikasi langsung dari kode sumber:

### 1. Prasyarat
- Python 3.10 atau 3.11 (64-bit)
- Git for Windows

### 2. Pemasangan
```powershell
# Clone repositori
git clone https://github.com/geadalfa/ConvertMyDocuments.git
cd ConvertMyDocuments

# Buat dan aktifkan lingkungan virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Pasang dependensi
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi
```powershell
python server.py
```

### 4. Menjalankan Pengujian Otomatis
Repositori ini menyertakan 15 uji unit dan integrasi:
```powershell
python -m unittest discover -s tests
```

---

## Lisensi dan Ketentuan Penggunaan

ConvertMyDocuments dirilis di bawah **[PolyForm Noncommercial License 1.0.0](LICENSE)**.

- **Penggunaan Diizinkan:** Bebas digunakan, dipelajari, dan dimodifikasi untuk keperluan pribadi, pendidikan, riset, serta organisasi nirlaba.
- **Larangan Komersial:** Dilarang keras diperjualbelikan, dimonetisasi, dipaketkan ke dalam produk komersial, atau dijadikan layanan konversi berbayar dalam bentuk apa pun.
