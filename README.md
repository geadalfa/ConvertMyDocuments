# ConvertMyDocuments

**English** | [Bahasa Indonesia](README.id.md)

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
