"""
converter.py
Core conversion orchestrator for ConvertMyDocuments v1.1.0.
Implements the 4 primary workflows requested by Alfa:
1. PDF to Word (.docx) - Preserves embedded images as real images, converts PDF tables to Word tables,
                         retains text formatting/headings, and routes scanned pages to RapidOCR.
2. PDF to Text (.txt) - Fast direct text extraction or high-res OCR for scanned pages.
3. JPG/Image to PDF (.pdf) - Single or batch image merging, A4 / native fit.
4. JPG/Image to Word (.docx) - Image OCR, watermark suppression, styled Word generation.
"""

import os
import shutil
import tempfile
from typing import List, Dict, Any, Optional, Callable
from PIL import Image
import fitz  # PyMuPDF
import pikepdf

from watermark import bleach_image_watermark
from ocr_engine import extract_text_from_image, ocr_pdf_page
from docx_builder import (
    create_base_document,
    build_docx_from_layout_elements,
    build_docx_from_text,
    build_docx_from_multipage_ocr
)


class UnlockedPdfInfo:
    def __init__(self, path: str, is_temp: bool):
        self.path = path
        self.is_temp = is_temp


def unlock_pdf_if_needed(input_path: str) -> UnlockedPdfInfo:
    """
    Checks if a PDF has permissions/encryption locks.
    If locked, creates an unlocked copy in temp and returns UnlockedPdfInfo(path, is_temp).
    """
    try:
        with pikepdf.open(input_path) as pdf:
            if pdf.is_encrypted:
                temp_dir = tempfile.gettempdir()
                unlocked_path = os.path.join(temp_dir, f"unlocked_{os.path.basename(input_path)}")
                pdf.save(unlocked_path)
                return UnlockedPdfInfo(unlocked_path, True)
    except Exception as e:
        print(f"[*] Pikepdf notice: {e}")
    return UnlockedPdfInfo(input_path, False)


def is_page_scanned(page: fitz.Page) -> bool:
    """
    Determines if an individual page has no selectable text (scanned page).
    Returns True if printable character count is less than 20.
    """
    raw_text = page.get_text("text").strip()
    clean_text = "".join([c for c in raw_text if c.isprintable()])
    return len(clean_text) < 20


def is_scanned_pdf(doc: fitz.Document, sample_pages: int = 5) -> bool:
    """
    Determines if a document is predominantly scanned.
    """
    pages_to_check = min(len(doc), sample_pages)
    if pages_to_check == 0:
        return True
    scanned_count = sum(1 for i in range(pages_to_check) if is_page_scanned(doc[i]))
    return (scanned_count / pages_to_check) > 0.5


def extract_page_hybrid_elements(doc: fitz.Document, page: fitz.Page) -> List[Dict[str, Any]]:
    """
    Extracts structured layout elements (text blocks, tables, and embedded images)
    from a digital/hybrid PDF page with spatial coordinates for proper reading order.
    """
    elements: List[Dict[str, Any]] = []

    # 1. Detect Tables
    table_bboxes = []
    try:
        tabs = page.find_tables()
        for tab in tabs:
            table_bboxes.append(tab.bbox)
            tdata = tab.extract()
            if tdata and len(tdata) > 0:
                elements.append({
                    "type": "table",
                    "y0": tab.bbox[1],
                    "data": tdata
                })
    except Exception as e:
        print(f"[!] Table detection notice: {e}")

    # 2. Extract Text Blocks (excluding text that is already inside tables)
    try:
        for b in page.get_text("blocks"):
            if b[6] == 0:  # block_type 0 = text
                b_x0, b_y0, b_x1, b_y1, b_text = b[0], b[1], b[2], b[3], b[4]
                in_table = False
                for tbox in table_bboxes:
                    if b_x0 >= (tbox[0] - 5) and b_y0 >= (tbox[1] - 5) and b_x1 <= (tbox[2] + 5) and b_y1 <= (tbox[3] + 5):
                        in_table = True
                        break
                if not in_table and b_text.strip():
                    elements.append({
                        "type": "text",
                        "y0": b_y0,
                        "text": b_text.strip()
                    })
    except Exception as e:
        print(f"[!] Text block extraction notice: {e}")

    # 3. Extract Embedded Images (Preserves real images without converting them to OCR text)
    try:
        seen_xrefs = set()
        image_infos = page.get_image_info(xrefs=True)

        for info in image_infos:
            xref = info.get("xref")
            if not xref or xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)

            # Filter out tiny 1x1 icons, lines, or spacers
            w_px = info.get("width", 0)
            h_px = info.get("height", 0)
            f_size = info.get("size", 0)
            if w_px < 25 or h_px < 25 or f_size < 1200:
                continue

            try:
                base_img = doc.extract_image(xref)
                img_bytes = base_img.get("image")
                if img_bytes:
                    bbox = info.get("bbox", (0, 0, 0, 0))
                    pt_w = bbox[2] - bbox[0]
                    elements.append({
                        "type": "image",
                        "y0": bbox[1],
                        "bytes": img_bytes,
                        "width_pt": pt_w
                    })
            except Exception as e:
                print(f"[!] Image extract xref {xref} failed: {e}")

    except Exception as e:
        print(f"[!] Image info inspection notice: {e}")

    # Sort all elements by vertical position (y0)
    elements.sort(key=lambda el: el.get("y0", 0.0))
    return elements


def pdf_to_word(
    input_path: str,
    output_path: str,
    ocr_mode: str = "auto",  # 'auto', 'force_ocr', 'direct_only'
    bleach_watermark: bool = False,
    watermark_threshold: int = 185,
    unlock: bool = True,
    progress_callback: Optional[Callable[[int, str], None]] = None
) -> Dict[str, Any]:
    """
    Converts PDF to Word (.docx) with full layout intelligence:
    - Embedded images remain REAL images (diagrams, game art, screenshots, photos).
    - PDF tables are converted into real Word tables.
    - Digital text is extracted directly with typography and lists.
    - Scanned/non-selectable pages are processed via RapidOCR.
    """
    def report(pct: int, msg: str):
        if progress_callback:
            progress_callback(pct, msg)

    report(5, "Memeriksa dokumen dan status enkripsi...")

    target_pdf = input_path
    is_temp = False
    if unlock:
        unlocked_info = unlock_pdf_if_needed(input_path)
        target_pdf = unlocked_info.path
        is_temp = unlocked_info.is_temp

    try:
        doc = fitz.open(target_pdf)
        total_pages = len(doc)
        if total_pages == 0:
            raise ValueError("Dokumen PDF kosong (0 halaman).")

        report(12, f"Dokumen dibuka: {total_pages} halaman. Memeriksa tipe dokumen...")

        total_images_in_pdf = sum(len(p.get_image_info()) for p in doc)
        total_tables_in_pdf = sum(len(p.find_tables().tables) for p in doc)
        is_scanned = is_scanned_pdf(doc)
        doc.close()

        # If document is digital/hybrid and not forced OCR, use pdf2docx for exact layout reconstruction
        if not is_scanned and ocr_mode != "force_ocr":
            try:
                report(25, "Menganalisis layout, padding, font, dan geometri dokumen...")
                from pdf2docx import Converter
                cv = Converter(target_pdf)
                report(50, "Merekonstruksi tata letak, gambar, dan tabel persis seperti PDF...")
                
                actual_output = output_path
                try:
                    cv.convert(actual_output)
                except PermissionError:
                    dir_name = os.path.dirname(os.path.abspath(output_path))
                    stem, ext = os.path.splitext(os.path.basename(output_path))
                    actual_output = os.path.join(dir_name, f"{stem}_v1.1{ext}")
                    cv.convert(actual_output)
                cv.close()

                report(100, "Konversi selesai dengan layout persis seperti PDF!")
                return {
                    "success": True,
                    "mode": "Presisi Tinggi (Identik PDF - Font, Padding & Gambar)",
                    "pages": total_pages,
                    "images_embedded": total_images_in_pdf,
                    "tables_embedded": total_tables_in_pdf,
                    "output_path": actual_output,
                    "message": f"Berhasil dikonversi persis seperti PDF ({total_pages} halaman, {total_images_in_pdf} gambar, {total_tables_in_pdf} tabel)."
                }
            except Exception as e:
                print(f"[!] pdf2docx fallback notice: {e}, falling back to hybrid builder...")

        # Fallback / Scanned PDF path
        doc = fitz.open(target_pdf)
        wdoc = create_base_document()
        scanned_pages_count = 0
        digital_pages_count = 0
        total_images_embedded = 0
        total_tables_embedded = 0

        for page_idx in range(total_pages):
            page = doc[page_idx]
            curr_pct = 15 + int((page_idx / total_pages) * 75)
            report(curr_pct, f"Memproses Halaman {page_idx + 1} dari {total_pages}...")

            page_is_scan = is_page_scanned(page)
            use_ocr = (ocr_mode == "force_ocr") or (ocr_mode != "direct_only" and page_is_scan)

            if use_ocr:
                scanned_pages_count += 1
                ocr_res = ocr_pdf_page(
                    page,
                    dpi=300,
                    bleach_watermark=bleach_watermark,
                    watermark_threshold=watermark_threshold
                )
                ocr_text = ocr_res.get("text", "")
                elements = [{"type": "text", "y0": 0.0, "text": ocr_text}]
                build_docx_from_layout_elements(wdoc, elements, is_first_page=(page_idx == 0))

            else:
                digital_pages_count += 1
                elements = extract_page_hybrid_elements(doc, page)
                
                # Count stats
                for el in elements:
                    if el["type"] == "image":
                        total_images_embedded += 1
                    elif el["type"] == "table":
                        total_tables_embedded += 1

                build_docx_from_layout_elements(wdoc, elements, is_first_page=(page_idx == 0))

            # Page break between pages (except last)
            if page_idx < total_pages - 1:
                wdoc.add_page_break()

        report(92, "Menyimpan berkas Word (.docx)...")
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        try:
            wdoc.save(output_path)
        except PermissionError:
            dir_name = os.path.dirname(os.path.abspath(output_path))
            stem, ext = os.path.splitext(os.path.basename(output_path))
            alt_path = os.path.join(dir_name, f"{stem}_v1.1{ext}")
            wdoc.save(alt_path)
            output_path = alt_path

        doc.close()

        report(100, "Konversi selesai dengan sukses!")

        mode_desc = "Hybrid (Teks, Gambar & Tabel)" if digital_pages_count > 0 else "RapidOCR Scanned"
        return {
            "success": True,
            "mode": mode_desc,
            "pages": total_pages,
            "digital_pages": digital_pages_count,
            "scanned_pages": scanned_pages_count,
            "images_embedded": total_images_embedded,
            "tables_embedded": total_tables_embedded,
            "output_path": output_path,
            "message": f"Berhasil dikonversi ({total_pages} halaman, {total_images_embedded} gambar, {total_tables_embedded} tabel)."
        }

    finally:
        if is_temp and os.path.exists(target_pdf):
            try:
                os.remove(target_pdf)
            except Exception:
                pass


def pdf_to_text(
    input_path: str,
    output_path: str,
    ocr_mode: str = "auto",
    bleach_watermark: bool = False,
    watermark_threshold: int = 185,
    unlock: bool = True,
    progress_callback: Optional[Callable[[int, str], None]] = None
) -> Dict[str, Any]:
    """
    Converts PDF to clean UTF-8 text (.txt). Automatically runs RapidOCR if pages are scanned.
    """
    def report(pct: int, msg: str):
        if progress_callback:
            progress_callback(pct, msg)

    report(5, "Memeriksa dokumen PDF...")

    target_pdf = input_path
    is_temp = False
    if unlock:
        unlocked_info = unlock_pdf_if_needed(input_path)
        target_pdf = unlocked_info.path
        is_temp = unlocked_info.is_temp

    try:
        doc = fitz.open(target_pdf)
        total_pages = len(doc)
        if total_pages == 0:
            raise ValueError("Dokumen PDF kosong.")

        report(20, f"Menganalisis {total_pages} halaman PDF...")

        all_text_pages = []
        ocr_count = 0

        for i, page in enumerate(doc):
            curr_pct = 20 + int((i / total_pages) * 70)
            report(curr_pct, f"Mengekstrak Halaman {i+1} dari {total_pages}...")

            page_is_scan = is_page_scanned(page)
            use_ocr = (ocr_mode == "force_ocr") or (ocr_mode != "direct_only" and page_is_scan)

            if use_ocr:
                ocr_count += 1
                res = ocr_pdf_page(
                    page,
                    dpi=300,
                    bleach_watermark=bleach_watermark,
                    watermark_threshold=watermark_threshold
                )
                txt = res.get("text", "").strip()
                all_text_pages.append(f"--- Halaman {i+1} (OCR) ---\n{txt}")
            else:
                txt = page.get_text("text").strip()
                all_text_pages.append(f"--- Halaman {i+1} ---\n{txt}")

        final_text = "\n\n".join(all_text_pages)
        report(92, "Menyimpan file teks (.txt)...")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_text)

        doc.close()
        report(100, "Ekstraksi teks selesai!")

        mode_used = "OCR" if ocr_count == total_pages else ("Direct" if ocr_count == 0 else "Hybrid")
        return {
            "success": True,
            "mode": mode_used,
            "pages": total_pages,
            "text": final_text,
            "char_count": len(final_text),
            "output_path": output_path,
            "message": f"Berhasil diekstrak ({len(final_text)} karakter, {total_pages} halaman)."
        }

    finally:
        if is_temp and os.path.exists(target_pdf):
            try:
                os.remove(target_pdf)
            except Exception:
                pass


def jpg_to_pdf(
    image_paths: List[str],
    output_path: str,
    page_size: str = "fit",  # 'fit', 'a4_portrait', 'a4_landscape'
    progress_callback: Optional[Callable[[int, str], None]] = None
) -> Dict[str, Any]:
    """
    Converts one or more image files (JPG, PNG, WEBP, BMP, etc.) into a single high-quality PDF.
    """
    def report(pct: int, msg: str):
        if progress_callback:
            progress_callback(pct, msg)

    if not image_paths:
        raise ValueError("Daftar gambar kosong.")

    report(10, f"Menyiapkan {len(image_paths)} gambar untuk dikonversi ke PDF...")

    out_doc = fitz.open()
    total_imgs = len(image_paths)

    A4_W, A4_H = 595.0, 842.0

    for i, img_path in enumerate(image_paths):
        curr_pct = 10 + int((i / total_imgs) * 80)
        report(curr_pct, f"Menyusun gambar {i+1} dari {total_imgs} ke PDF...")

        if not os.path.exists(img_path):
            continue

        with Image.open(img_path) as pil_img:
            img_w, img_h = pil_img.size

        if page_size == "fit":
            page = out_doc.new_page(width=img_w, height=img_h)
            rect = fitz.Rect(0, 0, img_w, img_h)
            page.insert_image(rect, filename=img_path)

        elif page_size == "a4_portrait":
            page = out_doc.new_page(width=A4_W, height=A4_H)
            margin = 36.0
            avail_w = A4_W - (margin * 2)
            avail_h = A4_H - (margin * 2)
            ratio = min(avail_w / img_w, avail_h / img_h)
            draw_w = img_w * ratio
            draw_h = img_h * ratio
            x0 = margin + (avail_w - draw_w) / 2.0
            y0 = margin + (avail_h - draw_h) / 2.0
            rect = fitz.Rect(x0, y0, x0 + draw_w, y0 + draw_h)
            page.insert_image(rect, filename=img_path)

        elif page_size == "a4_landscape":
            page = out_doc.new_page(width=A4_H, height=A4_W)
            margin = 36.0
            avail_w = A4_H - (margin * 2)
            avail_h = A4_W - (margin * 2)
            ratio = min(avail_w / img_w, avail_h / img_h)
            draw_w = img_w * ratio
            draw_h = img_h * ratio
            x0 = margin + (avail_w - draw_w) / 2.0
            y0 = margin + (avail_h - draw_h) / 2.0
            rect = fitz.Rect(x0, y0, x0 + draw_w, y0 + draw_h)
            page.insert_image(rect, filename=img_path)

    report(92, "Menyimpan dan mengompresi file PDF...")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    out_doc.save(output_path, deflate=True)
    out_doc.close()

    report(100, "Konversi JPG ke PDF selesai!")

    return {
        "success": True,
        "images_count": total_imgs,
        "output_path": output_path,
        "message": f"Berhasil menggabungkan {total_imgs} gambar ke PDF."
    }


def jpg_to_word(
    image_paths: List[str],
    output_path: str,
    bleach_watermark: bool = False,
    watermark_threshold: int = 185,
    progress_callback: Optional[Callable[[int, str], None]] = None
) -> Dict[str, Any]:
    """
    Performs OCR on one or more images (scans, receipts, documents, photos) and compiles
    the recognized text into a beautifully structured Word document (.docx).
    """
    def report(pct: int, msg: str):
        if progress_callback:
            progress_callback(pct, msg)

    if not image_paths:
        raise ValueError("Daftar gambar kosong.")

    total_imgs = len(image_paths)
    report(10, f"Memulai OCR untuk {total_imgs} gambar...")

    pages_data = []

    for i, img_path in enumerate(image_paths):
        curr_pct = 10 + int((i / total_imgs) * 75)
        report(curr_pct, f"Menganalisis & OCR gambar {i+1} dari {total_imgs}...")

        ocr_res = extract_text_from_image(
            img_path,
            bleach_watermark=bleach_watermark,
            watermark_threshold=watermark_threshold
        )
        pages_data.append(ocr_res)

    report(88, "Menyusun dokumen Word (.docx) berformat rapi...")
    doc_title = os.path.splitext(os.path.basename(image_paths[0]))[0].replace("_", " ").title()
    build_docx_from_multipage_ocr(pages_data, output_path, title=doc_title)

    report(100, "Konversi Gambar ke Word selesai!")

    return {
        "success": True,
        "images_count": total_imgs,
        "output_path": output_path,
        "message": f"Berhasil mengekstrak teks dari {total_imgs} gambar ke Word."
    }
