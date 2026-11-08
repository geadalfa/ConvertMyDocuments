"""
ocr_engine.py
Zero-leakage, 100% offline OCR extraction powered by RapidOCR (ONNX).
Handles scanned PDFs, photos of documents, receipts, watermarked text, and non-selectable PDFs.
"""

import os
from typing import Union, List, Dict, Any, Tuple
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
from watermark import bleach_image_watermark

_RAPID_OCR_INSTANCE = None


def get_ocr_engine():
    """Singleton getter for RapidOCR engine to prevent reloading models."""
    global _RAPID_OCR_INSTANCE
    if _RAPID_OCR_INSTANCE is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            _RAPID_OCR_INSTANCE = RapidOCR()
        except ImportError:
            raise RuntimeError(
                "rapidocr_onnxruntime is not installed. Run `pip install rapidocr_onnxruntime`."
            )
    return _RAPID_OCR_INSTANCE


def extract_text_from_image(
    image_input: Union[str, Image.Image, np.ndarray],
    bleach_watermark: bool = False,
    watermark_threshold: int = 185
) -> Dict[str, Any]:
    """
    Performs high-precision offline OCR on an image.
    
    Args:
        image_input: Image file path, PIL Image, or numpy array.
        bleach_watermark: If True, applies OpenCV thresholding to erase watermarks before OCR.
        watermark_threshold: Grayscale cutoff for watermark bleaching.
        
    Returns:
        Dict with:
          - 'text': Formatted full text with reconstructed paragraph breaks
          - 'blocks': List of individual detected text segments with bounding boxes and confidence
          - 'confidence': Average confidence score (0.0 to 1.0)
    """
    if bleach_watermark:
        _, img_for_ocr = bleach_image_watermark(image_input, threshold=watermark_threshold)
    else:
        if isinstance(image_input, str):
            img_for_ocr = cv2_load_or_pil(image_input)
        elif isinstance(image_input, Image.Image):
            img_for_ocr = np.array(image_input.convert("RGB"))
        elif isinstance(image_input, np.ndarray):
            img_for_ocr = image_input
        else:
            raise ValueError("Unsupported image input type")

    engine = get_ocr_engine()
    results, elapse = engine(img_for_ocr)

    if not results:
        return {
            "text": "",
            "blocks": [],
            "confidence": 0.0,
            "lines": []
        }

    # Format and reconstruct paragraphs
    structured_blocks = []
    total_conf = 0.0

    for item in results:
        box, text, score = item[0], str(item[1]).strip(), float(item[2])
        if not text:
            continue
        # box: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        ys = [pt[1] for pt in box]
        xs = [pt[0] for pt in box]
        min_y, max_y = min(ys), max(ys)
        min_x, max_x = min(xs), max(xs)
        center_y = (min_y + max_y) / 2.0
        line_height = max_y - min_y

        structured_blocks.append({
            "text": text,
            "confidence": score,
            "box": box,
            "min_x": min_x,
            "max_x": max_x,
            "min_y": min_y,
            "max_y": max_y,
            "center_y": center_y,
            "height": line_height
        })
        total_conf += score

    # Sort blocks primarily by vertical position (center_y) with tolerance, then by min_x
    # Sort top to bottom
    structured_blocks.sort(key=lambda b: (round(b["center_y"] / 10) * 10, b["min_x"]))

    # Group into lines and paragraphs
    lines: List[str] = []
    current_line: List[Dict[str, Any]] = []
    current_y = None
    avg_height = (
        sum(b["height"] for b in structured_blocks) / len(structured_blocks)
        if structured_blocks else 20.0
    )

    for b in structured_blocks:
        if current_y is None:
            current_y = b["center_y"]
            current_line.append(b)
        else:
            # Check if block belongs on the same horizontal line (within 0.6 * avg_height)
            if abs(b["center_y"] - current_y) <= (avg_height * 0.6):
                current_line.append(b)
            else:
                # Flush current line
                current_line.sort(key=lambda x: x["min_x"])
                line_str = " ".join([x["text"] for x in current_line])
                lines.append(line_str)
                current_line = [b]
                current_y = b["center_y"]

    if current_line:
        current_line.sort(key=lambda x: x["min_x"])
        lines.append(" ".join([x["text"] for x in current_line]))

    full_text = "\n".join(lines)
    avg_conf = (total_conf / len(structured_blocks)) if structured_blocks else 0.0

    return {
        "text": full_text,
        "blocks": structured_blocks,
        "confidence": avg_conf,
        "lines": lines
    }


def cv2_load_or_pil(path: str) -> np.ndarray:
    """Helper to safely read image file with Unicode paths on Windows."""
    pil_img = Image.open(path).convert("RGB")
    return np.array(pil_img)


def ocr_pdf_page(
    page: fitz.Page,
    dpi: int = 300,
    bleach_watermark: bool = False,
    watermark_threshold: int = 185
) -> Dict[str, Any]:
    """
    Renders a PyMuPDF PDF page to high-res bitmap and runs RapidOCR.
    """
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    img_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
    return extract_text_from_image(
        img_np,
        bleach_watermark=bleach_watermark,
        watermark_threshold=watermark_threshold
    )
