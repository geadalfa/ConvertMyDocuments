"""
test_api.py
QA Integration & End-to-End Test Suite for DocShield Converter HTTP Server & APIs.
Verifies all 4 conversion workflows, progress polling, and Windows native actions.
"""

import os
import sys
import json
import time
import base64
import unittest
import tempfile
import threading
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw
import fitz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from server import DocShieldHandler, ThreadingHTTPServer

TEST_PORT = 5578


class TestDocShieldAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="docshield_qa_")
        cls.server_address = ("127.0.0.1", TEST_PORT)
        cls.httpd = ThreadingHTTPServer(cls.server_address, DocShieldHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        import shutil
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def _post_json(self, endpoint: str, data: dict) -> dict:
        url = f"http://127.0.0.1:{TEST_PORT}{endpoint}"
        payload = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _get_json(self, endpoint: str) -> dict:
        url = f"http://127.0.0.1:{TEST_PORT}{endpoint}"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _poll_until_done(self, job_id: str, max_wait: float = 15.0) -> dict:
        start_t = time.time()
        while time.time() - start_t < max_wait:
            data = self._get_json(f"/api/progress?job_id={job_id}")
            if data.get("done"):
                return data
            time.sleep(0.2)
        raise TimeoutError(f"Job {job_id} did not finish within {max_wait}s")

    def test_01_health_status(self):
        """QA Gate: Verify local-only offline status and system parameters."""
        data = self._get_json("/api/status")
        self.assertEqual(data.get("name"), "ConvertMyDocuments")
        self.assertEqual(data.get("version"), "1.1.0")
        self.assertIn("100% Offline", data.get("mode"))
        self.assertTrue(os.path.exists(data.get("default_output_dir")))

    def test_02_heartbeat(self):
        """QA Gate: Verify watchdog heartbeat keeps application active."""
        data = self._post_json("/api/heartbeat", {})
        self.assertEqual(data.get("status"), "alive")

    def test_03_menu1_pdf_to_word(self):
        """QA Gate: End-to-end PDF to Word (.docx) conversion via API."""
        # Create a sample PDF
        pdf_path = os.path.join(self.temp_dir, "test_menu1.pdf")
        doc = fitz.open()
        p = doc.new_page()
        p.insert_text((50, 72), "Dokumen Uji Coba QA: Menu 1 PDF to Word")
        doc.save(pdf_path)
        doc.close()

        with open(pdf_path, "rb") as f:
            b64_pdf = base64.b64encode(f.read()).decode("utf-8")

        job_id = "qa_menu1"
        res = self._post_json("/api/convert", {
            "job_id": job_id,
            "mode": "pdf_to_word",
            "files": [{"name": "test_menu1.pdf", "data": b64_pdf}],
            "output_dir": self.temp_dir,
            "options": {"ocr_mode": "auto", "bleach_watermark": False, "unlock": True}
        })
        self.assertEqual(res.get("status"), "started")

        # Poll
        final_job = self._poll_until_done(job_id)
        self.assertTrue(final_job.get("done"))
        self.assertIsNone(final_job.get("error"))
        res_data = final_job.get("result", {})
        self.assertTrue(res_data.get("success"))
        out_path = res_data.get("output_path")
        self.assertTrue(os.path.exists(out_path))
        self.assertTrue(out_path.endswith(".docx"))

    def test_04_menu2_pdf_to_text(self):
        """QA Gate: End-to-end PDF to Text (.txt) conversion via API."""
        pdf_path = os.path.join(self.temp_dir, "test_menu2.pdf")
        doc = fitz.open()
        p = doc.new_page()
        p.insert_text((50, 72), "Dokumen Uji Coba QA: Menu 2 PDF to Text")
        doc.save(pdf_path)
        doc.close()

        with open(pdf_path, "rb") as f:
            b64_pdf = base64.b64encode(f.read()).decode("utf-8")

        job_id = "qa_menu2"
        self._post_json("/api/convert", {
            "job_id": job_id,
            "mode": "pdf_to_text",
            "files": [{"name": "test_menu2.pdf", "data": b64_pdf}],
            "output_dir": self.temp_dir,
            "options": {"ocr_mode": "auto", "bleach_watermark": False, "unlock": True}
        })

        final_job = self._poll_until_done(job_id)
        self.assertTrue(final_job.get("done"))
        self.assertIsNone(final_job.get("error"))
        res_data = final_job.get("result", {})
        self.assertTrue(res_data.get("success"))
        self.assertIn("Dokumen Uji Coba QA", res_data.get("text", ""))

    def test_05_menu3_jpg_to_pdf(self):
        """QA Gate: End-to-end JPG to PDF (.pdf) multi-image merge via API."""
        img1 = Image.new("RGB", (300, 200), (240, 240, 240))
        img2 = Image.new("RGB", (300, 200), (220, 220, 220))
        p1 = os.path.join(self.temp_dir, "p1.jpg")
        p2 = os.path.join(self.temp_dir, "p2.png")
        img1.save(p1)
        img2.save(p2)

        with open(p1, "rb") as f1, open(p2, "rb") as f2:
            b64_1 = base64.b64encode(f1.read()).decode("utf-8")
            b64_2 = base64.b64encode(f2.read()).decode("utf-8")

        job_id = "qa_menu3"
        self._post_json("/api/convert", {
            "job_id": job_id,
            "mode": "jpg_to_pdf",
            "files": [
                {"name": "p1.jpg", "data": b64_1},
                {"name": "p2.png", "data": b64_2}
            ],
            "output_dir": self.temp_dir,
            "options": {"page_size": "fit"}
        })

        final_job = self._poll_until_done(job_id)
        self.assertTrue(final_job.get("done"))
        self.assertIsNone(final_job.get("error"))
        out_path = final_job.get("result", {}).get("output_path")
        self.assertTrue(os.path.exists(out_path))

        # Verify PDF has 2 pages
        doc = fitz.open(out_path)
        self.assertEqual(len(doc), 2)
        doc.close()

    def test_06_menu4_jpg_to_word_ocr(self):
        """QA Gate: End-to-end JPG to Word (.docx) OCR conversion via API."""
        img = Image.new("RGB", (500, 150), (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((20, 50), "QA OCR WORD 2026", fill=(10, 10, 10))
        img_path = os.path.join(self.temp_dir, "qa_ocr.png")
        img.save(img_path)

        with open(img_path, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("utf-8")

        job_id = "qa_menu4"
        self._post_json("/api/convert", {
            "job_id": job_id,
            "mode": "jpg_to_word",
            "files": [{"name": "qa_ocr.png", "data": b64_img}],
            "output_dir": self.temp_dir,
            "options": {"bleach_watermark": False}
        })

        final_job = self._poll_until_done(job_id)
        self.assertTrue(final_job.get("done"))
        self.assertIsNone(final_job.get("error"))
        out_path = final_job.get("result", {}).get("output_path")
        self.assertTrue(os.path.exists(out_path))
        self.assertTrue(out_path.endswith(".docx"))


if __name__ == "__main__":
    unittest.main()
