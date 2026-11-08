# ConvertMyDocuments

[ **English Version** ](#convertmydocuments) &nbsp;•&nbsp; [ **Versi Bahasa Indonesia** ](#convertmydocuments---bahasa-indonesia)

[![License: Non-Commercial](https://img.shields.io/badge/License-PolyForm%20NonCommercial-blue.svg)](LICENSE)
[![Privacy: 100% Offline](https://img.shields.io/badge/Privacy-100%25%20Offline%20(Localhost)-10b981.svg)](#privacy-guarantee-and-threat-model)
[![Compliance: UU PDP No. 27/2022](https://img.shields.io/badge/Compliance-Indonesia%20UU%20PDP%20No.%2027%2F2022-brightgreen.svg)](#regulatory-compliance-indonesia-uu-pdp)
[![Language: Bilingual](https://img.shields.io/badge/UI-English%20%7C%20Bahasa%20Indonesia-blueviolet.svg)](#bilingual-interface-and-session-persistence)
[![Platform: Windows 10/11](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20(64--bit)-lightgrey.svg)](#installation-and-download)
[![Release: v1.1.1](https://img.shields.io/badge/Release-v1.1.1-blue.svg)](https://github.com/geadalfa/ConvertMyDocuments/releases/tag/v1.1.1)

ConvertMyDocuments is a standalone, offline Windows desktop application that converts PDF documents, scans, and images into editable Microsoft Word (`.docx`), plain text (`.txt`), and PDF (`.pdf`) formats with zero network data transmission.

---

## Privacy Guarantee and Threat Model

Public web-based document conversion utilities routinely upload user files to external cloud infrastructures, exposing confidential records to remote persistence, third-party inspection, and potential exfiltration.

ConvertMyDocuments mitigates this risk by enforcing a strict local-execution boundary:

1. **Localhost Execution Only (`127.0.0.1`):** All document parsing, OCR inference, image rendering, and document compilation execute exclusively in local CPU/GPU memory and local process space.
2. **Zero Outbound Telemetry:** The application makes no external HTTP, DNS, or socket requests. It operates without an active network connection or during Airplane Mode.
3. **Automated Buffer Purging:** Intermediate raster buffers and temporary decode files are deleted from storage immediately upon job completion.

### Regulatory Compliance: Indonesia UU PDP

ConvertMyDocuments is structured to comply with the statutory standards of **Republic of Indonesia Law No. 27 of 2022 on Personal Data Protection (UU PDP)**. Because no documents, personal identifiers, biometric scans, or confidential payloads leave the host workstation, data controllers and end-users maintain total custody of confidential assets, including identity cards (KTP), tax records (NPWP), payroll statements, medical files, banking documents, and legal agreements.

---

## Core Capabilities

### 1. PDF to Word (`.docx`) with Layout Preservation
- **True Layout Reconstruction:** Preserves original page dimensions (including 16:9 widescreen presentation slides, A4, and US Letter), page margins, paragraph padding, line spacing, and horizontal alignment.
- **Typography Retention:** Preserves font family mappings, point sizes, bold, italic styles, and text color codes.
- **Non-Destructive Image Embedding:** Vector shapes, diagrams, logos, and raster photographs within the PDF are extracted at native resolution and inserted into the target Word document as native image shapes rather than being flattened or discarded.
- **Native Table Reconstruction:** Converts PDF vector rules and bounding boxes into true editable Microsoft Word table grids.
- **Automated Fallback to RapidOCR:** If a page lacks a selectable text stream (e.g., photographed or scanned documents), the processing pipeline automatically routes that page through the local RapidOCR ONNX inference engine.

### 2. PDF to Text (`.txt`)
- Extracts plain text from digital PDFs or scanned pages with structured page demarcations (`--- Page X ---`).
- Includes an in-app preview viewer and a one-click clipboard copying mechanism.

### 3. Images to PDF (`.pdf`)
- Merges multiple images (JPEG, PNG, WebP, BMP, TIFF) into a unified PDF document.
- Provides three layout projection modes:
  - **Fit Resolution:** Retains each image's native pixel aspect ratio.
  - **A4 Portrait:** Projects images into standardized A4 portrait pages.
  - **A4 Landscape:** Projects images into standardized A4 landscape pages.

### 4. Images to Word (`.docx`) via RapidOCR
- Extracts textual content from photo receipts, physical document scans, or book captures.
- **Adaptive Watermark Bleaching:** Employs OpenCV thresholding to filter out background stamps, watermarks, or paper discoloration before OCR analysis.

---

## Bilingual Interface and Session Persistence

ConvertMyDocuments provides a native bilingual interface supporting **English** and **Bahasa Indonesia**:

- **Default Language:** English is the default setting for fresh installations.
- **Header Toggle:** Users can switch languages instantly using the `[ EN | ID ]` selector located in the top header.
- **Persistent Preferences:** Selected language settings are preserved across application restarts by persisting state to `%LOCALAPPDATA%\ConvertMyDocuments\settings.json` and browser storage.

---

## Installation and Download

Pre-compiled standalone binaries for 64-bit Windows are distributed through [GitHub Releases](https://github.com/geadalfa/ConvertMyDocuments/releases/tag/v1.1.1):

| Package | Type | Description |
| :--- | :--- | :--- |
| **[`ConvertMyDocuments_Setup_v1.1.1.exe`](https://github.com/geadalfa/ConvertMyDocuments/releases/download/v1.1.1/ConvertMyDocuments_Setup_v1.1.1.exe)** | Official Installer (Recommended) | Standard Inno Setup installer. Installs per-user without requiring administrative (UAC) elevation. Creates Desktop and Start Menu shortcuts. |
| **[`ConvertMyDocuments-v1.1.1-portable.zip`](https://github.com/geadalfa/ConvertMyDocuments/releases/download/v1.1.1/ConvertMyDocuments-v1.1.1-portable.zip)** | Standalone Portable Archive | Extract to any folder and execute `ConvertMyDocuments.exe` directly without installation. |

### System Requirements
- **Operating System:** Windows 10 (64-bit) or Windows 11 (64-bit).
- **Runtime Host:** Microsoft Edge (pre-installed on Windows 10/11, utilized in chromeless App Mode).
- **Network Requirement:** None (100% offline).

---

## Technical Architecture

```
ConvertMyDocuments/
├── backend/
│   ├── converter.py       # Core conversion dispatcher & layout router
│   ├── docx_builder.py    # python-docx layout synthesizer & DPI sanitizer
│   ├── ocr_engine.py      # RapidOCR ONNX inference wrapper
│   └── watermark.py       # OpenCV watermark bleaching & thresholding
├── static/
│   ├── index.html         # Application markup with i18n data bindings
│   ├── style.css          # Zinc design tokens & desktop UI styling
│   └── app.js             # Client-side controller, bilingual dictionary, & state
├── tests/
│   ├── test_converter.py  # Unit tests for OCR, formatting, & layout logic
│   └── test_api.py        # Integration tests for server REST endpoints & settings
├── server.py              # Localhost multi-threaded HTTP server & Edge App launcher
├── ConvertMyDocuments.spec# PyInstaller packaging configuration
└── installer.iss          # Inno Setup 6 compilation script
```

### Key Libraries
- **`pdf2docx` & `PyMuPDF` (`fitz`):** Digital vector parsing, font metrics extraction, and image extraction.
- **`rapidocr_onnxruntime`:** Offline deep learning OCR inference utilizing lightweight ONNX models.
- **`python-docx`:** Programmatic generation of OpenXML `.docx` files.
- **`pikepdf`:** PDF structure repair and removal of arbitrary print/copy permissions locks.
- **`OpenCV` (`cv2`) & `Pillow` (`PIL`):** Watermark bleaching, DPI normalization, and image pre-processing.

---

## Running from Source

Developers wishing to inspect, modify, or run the application directly from source code:

### 1. Prerequisites
- Python 3.10 or 3.11 (64-bit)
- Git for Windows

### 2. Setup
```powershell
# Clone the repository
git clone https://github.com/geadalfa/ConvertMyDocuments.git
cd ConvertMyDocuments

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt
```

### 3. Launch Application
```powershell
python server.py
```

### 4. Execute Test Suite
The codebase includes a comprehensive 15-case test suite covering unit operations and API endpoints:
```powershell
python -m unittest discover -s tests
```

---

## Building the Executable and Installer

To reproduce the distribution packages locally:

### 1. Compile Standalone Bundle via PyInstaller
```powershell
python -m PyInstaller ConvertMyDocuments.spec --noconfirm
```
The output directory will be created at `dist\ConvertMyDocuments\`.

### 2. Compile Windows Installer via Inno Setup
Ensure Inno Setup 6 is installed, then run:
```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```
The compiled installer will be saved to `installer_output\ConvertMyDocuments_Setup_v1.1.1.exe`.

---

## License and Terms of Use

ConvertMyDocuments is released under the **[PolyForm Noncommercial License 1.0.0](LICENSE)**.

- **Permitted Use:** Free to run, inspect, and modify for personal, educational, research, and non-profit purposes.
- **Commercial Restriction:** Strictly prohibited from being sold, monetized, bundled into commercial software, or hosted as a paid conversion service.

---
---

# ConvertMyDocuments - Bahasa Indonesia

[ **Kembali ke Atas (English Version)** ](#convertmydocuments)

[![Lisensi: Non-Komersial](https://img.shields.io/badge/Lisensi-PolyForm%20NonCommercial-blue.svg)](LICENSE)
[![Privasi: 100% Offline](https://img.shields.io/badge/Privasi-100%25%20Offline%20(Localhost)-10b981.svg)](#jaminan-privasi-dan-model-keamanan)
[![Kepatuhan: UU PDP No. 27/2022](https://img.shields.io/badge/Kepatuhan-UU%20PDP%20No.%2027%2F2022-brightgreen.svg)](#kepatuhan-regulasi-uu-pdp-indonesia)
[![Bahasa: Dwibahasa](https://img.shields.io/badge/UI-English%20%7C%20Bahasa%20Indonesia-blueviolet.svg)](#antarmuka-dwibahasa-dan-penyimpanan-sesi-1)
[![Platform: Windows 10/11](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20(64--bit)-lightgrey.svg)](#unduh-dan-instalasi-1)
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
