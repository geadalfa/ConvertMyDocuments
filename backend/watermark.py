"""
watermark.py
Bleaches raster watermarks and cleans vector watermark artifacts from documents.
Zero-leakage local OpenCV and PyMuPDF processing.
"""

import os
from typing import Union, Tuple
import numpy as np
from PIL import Image
import cv2
import fitz  # PyMuPDF


def bleach_image_watermark(
    image_input: Union[str, Image.Image, np.ndarray],
    threshold: int = 185,
    contrast_boost: bool = True
) -> Tuple[Image.Image, np.ndarray]:
    """
    Bleaches translucent/faint watermarks and paper background discoloration
    to pure white (#FFFFFF) while preserving dark ink text strokes.
    
    Args:
        image_input: Filepath, PIL Image, or numpy array.
        threshold: Luminance cutoff (0-255). Pixels > threshold become 255. Default 185.
        contrast_boost: If True, stretches contrast of remaining ink.
        
    Returns:
        Tuple of (cleaned_pil_image, cleaned_rgb_numpy_array)
    """
    if isinstance(image_input, str):
        if not os.path.exists(image_input):
            raise FileNotFoundError(f"Image file not found: {image_input}")
        pil_img = Image.open(image_input).convert("RGB")
        img_np = np.array(pil_img)
    elif isinstance(image_input, Image.Image):
        pil_img = image_input.convert("RGB")
        img_np = np.array(pil_img)
    elif isinstance(image_input, np.ndarray):
        img_np = image_input
        if len(img_np.shape) == 2:
            img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
        elif img_np.shape[2] == 4:
            img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
    else:
        raise ValueError("Unsupported image input type")

    # 1. Convert to grayscale for luminance threshold analysis
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # 2. Bleach background & translucent watermarks (luminance > threshold -> 255)
    # Mask pixels brighter than threshold
    bleached = gray.copy()
    bleached[gray > threshold] = 255

    # 3. Contrast stretch ink (protecting dark strokes)
    if contrast_boost:
        # Normalize range to 0-255
        bleached = cv2.normalize(bleached, None, 0, 255, cv2.NORM_MINMAX)

    # 4. Convert back to RGB
    cleaned_rgb = cv2.cvtColor(bleached, cv2.COLOR_GRAY2RGB)
    cleaned_pil = Image.fromarray(cleaned_rgb)

    return cleaned_pil, cleaned_rgb


def clean_pdf_vector_watermarks(input_pdf_path: str, output_pdf_path: str) -> bool:
    """
    Removes vector watermarks, annotations, and artifacts from a PDF file.
    """
    try:
        doc = fitz.open(input_pdf_path)
        for page in doc:
            for annot in list(page.annots() or []):
                page.delete_annot(annot)
            page.clean_contents()
        os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
        doc.save(output_pdf_path, deflate=True)
        doc.close()
        return True
    except Exception as e:
        print(f"[ERR] Failed to clean vector watermarks: {e}")
        return False
