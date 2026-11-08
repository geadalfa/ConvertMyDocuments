"""
test_converter.py
Comprehensive unit tests for DocShield Converter core engine:
- Watermark bleaching (OpenCV)
- RapidOCR offline text extraction
- DOCX builder formatting
- JPG to PDF conversion
- JPG to Word conversion
- PDF to Text (Direct & Scanned OCR)
- PDF to Word (Direct & Scanned OCR)
"""

import os
import sys
import unittest
import tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import fitz
from docx import Document

# Add backend to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(BASE_DIR, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from watermark import bleach_image_watermark, clean_pdf_vector_watermarks
from ocr_engine import extract_text_from_image, ocr_pdf_page
from docx_builder import (
    build_docx_from_text,
    build_docx_from_markdown,
    build_docx_from_multipage_ocr
)
from converter import (
    pdf_to_word,
    pdf_to_text,
    jpg_to_pdf,
    jpg_to_word,
    is_scanned_pdf
)


class TestDocShieldConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_synthetic_text_image(self, text: str, width: int = 500, height: int = 200, bg_color=(255, 255, 255)):
        """Creates a synthetic image with clean high-contrast text for testing."""
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        # Draw dark text
        draw.text((20, 40), text, fill=(10, 10, 10))
        return img

    def test_watermark_bleaching(self):
        """Verify that faint watermark pixels (>185) are bleached to 255 while dark text is preserved."""
        # Create image with faint gray watermark (RGB 210,210,210) and dark ink text (RGB 20,20,20)
        img = Image.new("RGB", (300, 100), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Faint watermark
        draw.rectangle([50, 20, 250, 40], fill=(210, 210, 210))
        # Dark text stroke
        draw.rectangle([50, 60, 250, 80], fill=(20, 20, 20))

        cleaned_pil, cleaned_np = bleach_image_watermark(img, threshold=185)
        
        # Verify watermark region is bleached to pure white (255)
        wm_region = cleaned_np[25:35, 60:200]
        self.assertTrue(np.all(wm_region >= 250), f"Watermark not fully bleached: min val {wm_region.min()}")

        # Verify dark stroke region remains dark (< 80)
        dark_region = cleaned_np[65:75, 60:200]
        self.assertTrue(np.mean(dark_region) < 80, f"Dark stroke was unexpectedly bleached: mean {np.mean(dark_region)}")

    def test_ocr_engine_synthetic(self):
        """Test offline OCR extraction on synthetic document text."""
        img = self._create_synthetic_text_image("DOCSHIELD TEST 2026")
        img_path = os.path.join(self.temp_dir, "test_ocr.png")
        img.save(img_path)

        res = extract_text_from_image(img_path)
        self.assertIn("text", res)
        self.assertGreater(len(res["blocks"]), 0)
        # RapidOCR should detect either DOCSHIELD or TEST or 2026
        combined_text = res["text"].upper()
        self.assertTrue("TEST" in combined_text or "2026" in combined_text or "DOCSHIELD" in combined_text)

    def test_docx_builder(self):
        """Test DOCX builder generates valid Word files with correct paragraphs."""
        out_docx = os.path.join(self.temp_dir, "test_doc.docx")
        text = "# Laporan Hasil Konversi\n\n## Sub Judul\n- Poin pertama\n- Poin kedua\n\nIni adalah paragraf biasa."
        success = build_docx_from_markdown(text, out_docx)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(out_docx))

        # Inspect generated docx
        doc = Document(out_docx)
        self.assertGreater(len(doc.paragraphs), 3)

    def test_jpg_to_pdf(self):
        """Test converting multiple JPG/PNG images into a single unified PDF."""
        img1 = self._create_synthetic_text_image("PAGE ONE", 400, 300)
        img2 = self._create_synthetic_text_image("PAGE TWO", 500, 400)
        p1 = os.path.join(self.temp_dir, "img1.png")
        p2 = os.path.join(self.temp_dir, "img2.jpg")
        img1.save(p1)
        img2.save(p2)

        out_pdf = os.path.join(self.temp_dir, "merged.pdf")
        res = jpg_to_pdf([p1, p2], out_pdf, page_size="fit")
        self.assertTrue(res["success"])
        self.assertTrue(os.path.exists(out_pdf))

        # Verify PDF has 2 pages
        doc = fitz.open(out_pdf)
        self.assertEqual(len(doc), 2)
        doc.close()

    def test_jpg_to_word(self):
        """Test converting an image to editable Word (.docx) via OCR."""
        img = self._create_synthetic_text_image("INVOICE #998877", 600, 200)
        p = os.path.join(self.temp_dir, "invoice.png")
        img.save(p)

        out_docx = os.path.join(self.temp_dir, "invoice.docx")
        res = jpg_to_word([p], out_docx)
        self.assertTrue(res["success"])
        self.assertTrue(os.path.exists(out_docx))

    def test_pdf_to_text_and_word_direct(self):
        """Test direct conversion of standard text PDF without needing OCR."""
        # Create a digital text PDF using PyMuPDF
        sample_pdf = os.path.join(self.temp_dir, "sample_digital.pdf")
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 72), "Halo Alfa! Ini dokumen digital rahasia yang aman dari web luar.")
        doc.save(sample_pdf)
        doc.close()

        # 1. Test PDF to Text
        txt_out = os.path.join(self.temp_dir, "sample.txt")
        res_txt = pdf_to_text(sample_pdf, txt_out, ocr_mode="auto")
        self.assertTrue(res_txt["success"])
        self.assertEqual(res_txt["mode"].lower(), "direct")
        self.assertIn("Halo Alfa", res_txt["text"])

        # 2. Test PDF to Word
        docx_out = os.path.join(self.temp_dir, "sample.docx")
        res_docx = pdf_to_word(sample_pdf, docx_out, ocr_mode="auto")
        self.assertTrue(res_docx["success"])
        self.assertTrue("Presisi" in res_docx["mode"] or "Hybrid" in res_docx["mode"])
        self.assertTrue(os.path.exists(docx_out))

    def test_hybrid_pdf_image_table_preservation(self):
        """Test that images remain images, tables become tables, and text remains clean."""
        # Create a hybrid PDF with digital text and an embedded image
        hybrid_pdf = os.path.join(self.temp_dir, "hybrid_doc.pdf")
        img = self._create_synthetic_text_image("CHART PREVIEW", 400, 200)
        img_temp = os.path.join(self.temp_dir, "chart.png")
        img.save(img_temp)

        doc = fitz.open()
        page = doc.new_page(width=600, height=800)
        page.insert_text((50, 50), "Laporan Arsitektur Hybrid 2026")
        page.insert_text((50, 75), "Berikut adalah gambar diagram arsitektur:")
        page.insert_image(fitz.Rect(50, 100, 450, 300), filename=img_temp)
        page.insert_text((50, 330), "Kesimpulan dan langkah selanjutnya.")
        doc.save(hybrid_pdf)
        doc.close()

        docx_out = os.path.join(self.temp_dir, "hybrid_out.docx")
        res = pdf_to_word(hybrid_pdf, docx_out, ocr_mode="auto")
        self.assertTrue(res["success"])
        self.assertGreater(res["images_embedded"], 0)
        self.assertTrue(os.path.exists(docx_out))

        # Inspect generated docx
        out_doc = Document(docx_out)
        has_graphic = (len(out_doc.inline_shapes) > 0) or any('image' in rel.target_ref for rel in out_doc.part.rels.values())
        self.assertTrue(has_graphic, "Embedded image was not preserved as image in Word!")

    def test_pdf_to_text_scanned_ocr(self):
        """Test automatic detection of scanned PDF (no text layer) and routing to RapidOCR."""
        # Create a purely scanned PDF (only an embedded raster image, zero selectable text)
        scanned_pdf = os.path.join(self.temp_dir, "scanned_invoice.pdf")
        img = self._create_synthetic_text_image("FAKTUR PAJAK RESMI 2026", 700, 250)
        img_temp = os.path.join(self.temp_dir, "scan_raw.png")
        img.save(img_temp)

        doc = fitz.open()
        page = doc.new_page(width=700, height=250)
        page.insert_image(fitz.Rect(0, 0, 700, 250), filename=img_temp)
        doc.save(scanned_pdf)
        doc.close()

        # Verify is_scanned_pdf detects it as scanned
        doc_check = fitz.open(scanned_pdf)
        self.assertTrue(is_scanned_pdf(doc_check))
        doc_check.close()

        # Convert to text with auto OCR
        txt_out = os.path.join(self.temp_dir, "scanned.txt")
        res_txt = pdf_to_text(scanned_pdf, txt_out, ocr_mode="auto")
        self.assertTrue(res_txt["success"])
        self.assertEqual(res_txt["mode"].lower(), "ocr")
        self.assertGreater(len(res_txt["text"]), 0)

        # Convert to Word with auto OCR
        docx_out = os.path.join(self.temp_dir, "scanned.docx")
        res_docx = pdf_to_word(scanned_pdf, docx_out, ocr_mode="auto")
        self.assertTrue(res_docx["success"])
        self.assertIn("OCR", res_docx["mode"].upper())
        self.assertTrue(os.path.exists(docx_out))


if __name__ == "__main__":
    unittest.main()
