"""
docx_builder.py
High-taste, professional Word document (.docx) builder for ConvertMyDocuments v1.1.0.
Preserves embedded images, structured tables, heading hierarchies, lists, and typography.
Safely sanitizes image metadata (preventing zero-DPI ZeroDivisionError crashes).
"""

import os
import io
import re
from typing import List, Dict, Any, Optional
from PIL import Image
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


def create_base_document() -> Document:
    """Initializes a python-docx Document with clean 1-inch margins and default styles."""
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Configure Normal style
    style_normal = doc.styles["Normal"]
    style_normal.font.name = "Calibri"
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(0x18, 0x18, 0x1B)  # Zinc-900
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

    return doc


def apply_heading_styles(heading, level: int):
    """Applies clean typography to headings."""
    heading.paragraph_format.keep_with_next = True
    heading.paragraph_format.space_before = Pt(12)
    heading.paragraph_format.space_after = Pt(4)
    run = heading.runs[0] if heading.runs else heading.add_run()
    run.font.name = "Calibri"
    if level == 1:
        run.font.size = Pt(18)
        run.bold = True
        run.font.color.rgb = RGBColor(0x09, 0x09, 0x0B)
    elif level == 2:
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(0x18, 0x18, 0x1B)
    elif level == 3:
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = RGBColor(0x27, 0x27, 0x2A)


def sanitize_image_bytes(img_bytes: bytes) -> Optional[bytes]:
    """
    Sanitizes image bytes with Pillow:
    - Fixes zero-DPI metadata (e.g. dpi=(0,0)) which crashes python-docx with ZeroDivisionError.
    - Converts CMYK or non-standard color modes to RGB/PNG.
    """
    try:
        pil_img = Image.open(io.BytesIO(img_bytes))
        dpi = pil_img.info.get("dpi")

        needs_reencode = False
        if dpi is None or dpi[0] <= 0 or dpi[1] <= 0:
            needs_reencode = True
        if pil_img.mode not in ("RGB", "RGBA"):
            needs_reencode = True

        if needs_reencode:
            buf = io.BytesIO()
            if pil_img.mode in ("RGBA", "LA") or (pil_img.mode == "P" and "transparency" in pil_img.info):
                pil_img = pil_img.convert("RGBA")
                pil_img.save(buf, format="PNG", dpi=(96, 96))
            else:
                pil_img = pil_img.convert("RGB")
                pil_img.save(buf, format="JPEG", quality=95, dpi=(96, 96))
            return buf.getvalue()

        return img_bytes
    except Exception as e:
        print(f"[!] Warning: image sanitization failed: {e}")
        return img_bytes


def add_image_to_docx(doc: Document, img_bytes: bytes, width_pt: Optional[float] = None) -> bool:
    """
    Embeds an image into the Word document centered, scaled proportionally to fit the page.
    """
    try:
        clean_bytes = sanitize_image_bytes(img_bytes)
        if not clean_bytes:
            return False

        # Standard text width on 8.5x11 inch page with 1-inch margins is 6.5 inches
        max_width_in = 6.2
        if width_pt and width_pt > 0:
            calc_w = width_pt / 72.0
            target_w_in = min(max_width_in, max(2.0, calc_w))
        else:
            target_w_in = 5.0

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run()
        r.add_picture(io.BytesIO(clean_bytes), width=Inches(target_w_in))
        return True
    except Exception as e:
        print(f"[!] Failed to insert picture into docx: {e}")
        return False


def add_table_to_docx(doc: Document, table_data: List[List[str]]) -> bool:
    """
    Inserts a structured, styled grid table into the Word document.
    """
    try:
        if not table_data or len(table_data) == 0:
            return False

        num_rows = len(table_data)
        num_cols = max(len(row) for row in table_data)
        if num_cols == 0:
            return False

        table = doc.add_table(rows=num_rows, cols=num_cols)
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        for r_idx, row in enumerate(table_data):
            for c_idx in range(num_cols):
                cell_val = row[c_idx] if c_idx < len(row) else ""
                cell = table.cell(r_idx, c_idx)
                cell.text = (cell_val or "").strip()

                if r_idx == 0:
                    for p in cell.paragraphs:
                        p.paragraph_format.space_before = Pt(3)
                        p.paragraph_format.space_after = Pt(3)
                        for r in p.runs:
                            r.bold = True
                            r.font.name = "Calibri"
                            r.font.size = Pt(10.5)
                else:
                    for p in cell.paragraphs:
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.space_after = Pt(2)
                        for r in p.runs:
                            r.font.name = "Calibri"
                            r.font.size = Pt(10)

        doc.add_paragraph()
        return True
    except Exception as e:
        print(f"[!] Failed to insert table into docx: {e}")
        return False


def add_text_to_docx(doc: Document, text: str, is_first_page: bool = False):
    """
    Adds text paragraphs, headings, and lists cleanly to the document.
    """
    lines = text.splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("●") or stripped.startswith("•") or stripped.startswith("- ") or stripped.startswith("* "):
            content = stripped.lstrip("●•-* ").strip()
            doc.add_paragraph(content, style="List Bullet")
        elif re.match(r"^\d+[\.\)]\s", stripped):
            m = re.match(r"^\d+[\.\)]\s", stripped)
            doc.add_paragraph(stripped[m.end():], style="List Number")
        elif stripped.startswith("### "):
            h = doc.add_heading(stripped[4:], level=3)
            apply_heading_styles(h, 3)
        elif stripped.startswith("## "):
            h = doc.add_heading(stripped[3:], level=2)
            apply_heading_styles(h, 2)
        elif stripped.startswith("# "):
            h = doc.add_heading(stripped[2:], level=1)
            apply_heading_styles(h, 1)
        elif len(stripped) < 65 and (is_first_page and not stripped.endswith(".")):
            h = doc.add_heading(stripped, level=1)
            apply_heading_styles(h, 1)
        elif len(stripped) < 50 and stripped.isupper() and not stripped.endswith("."):
            h = doc.add_heading(stripped.title(), level=2)
            apply_heading_styles(h, 2)
        else:
            doc.add_paragraph(line)


def build_docx_from_layout_elements(
    doc: Document,
    elements: List[Dict[str, Any]],
    is_first_page: bool = False
):
    """
    Adds mixed layout elements (text, tables, and images) to a Word document
    in their natural top-to-bottom reading order.
    """
    elements.sort(key=lambda el: el.get("y0", 0.0))

    for el in elements:
        el_type = el.get("type")
        if el_type == "text":
            add_text_to_docx(doc, el.get("text", ""), is_first_page=is_first_page)
        elif el_type == "table":
            add_table_to_docx(doc, el.get("data", []))
        elif el_type == "image":
            add_image_to_docx(doc, el.get("bytes", b""), width_pt=el.get("width_pt"))


def build_docx_from_text(
    text: str,
    output_docx_path: str,
    title: Optional[str] = None
) -> bool:
    """Constructs a Word document from plain text."""
    try:
        doc = create_base_document()
        if title:
            h = doc.add_heading(title, level=1)
            apply_heading_styles(h, 1)
        add_text_to_docx(doc, text, is_first_page=True)
        os.makedirs(os.path.dirname(os.path.abspath(output_docx_path)), exist_ok=True)
        doc.save(output_docx_path)
        return True
    except Exception as e:
        print(f"[ERR] Failed to build docx: {e}")
        return False


def build_docx_from_multipage_ocr(
    pages_data: List[Dict[str, Any]],
    output_docx_path: str,
    title: Optional[str] = None
) -> bool:
    """Constructs a Word document from multi-page OCR outputs with page breaks."""
    try:
        doc = create_base_document()
        if title:
            h = doc.add_heading(title, level=1)
            apply_heading_styles(h, 1)

        total = len(pages_data)
        for i, page_info in enumerate(pages_data):
            page_text = page_info.get("text", "")
            add_text_to_docx(doc, page_text, is_first_page=(i == 0))
            if i < total - 1:
                doc.add_page_break()

        os.makedirs(os.path.dirname(os.path.abspath(output_docx_path)), exist_ok=True)
        doc.save(output_docx_path)
        return True
    except Exception as e:
        print(f"[ERR] Failed to build multipage docx: {e}")
        return False


def build_docx_from_markdown(
    md_content: str,
    output_docx_path: str
) -> bool:
    """Transforms structured markdown into Word (.docx)."""
    return build_docx_from_text(md_content, output_docx_path)
