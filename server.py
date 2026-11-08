"""
server.py
ConvertMyDocuments v1.1.0 - High Performance Standalone Windows Desktop Server.
Runs 100% offline on localhost (127.0.0.1) with zero external network connectivity.
Launches native Windows Edge App Mode with automatic lifecycle watchdog.
"""

import os
import sys
import json
import time
import base64
import tempfile
import threading
import subprocess
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import urllib.parse
from typing import Dict, Any

# Ensure stdout/stderr do not crash when running in windowed mode (--noconsole / pythonw)
if sys.stdout is None:
    try:
        sys.stdout = open(os.devnull, "w")
    except Exception:
        pass
if sys.stderr is None:
    try:
        sys.stderr = open(os.devnull, "w")
    except Exception:
        pass

# Determine base directory
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

backend_path = os.path.join(BASE_DIR, "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from converter import (
    pdf_to_word,
    pdf_to_text,
    jpg_to_pdf,
    jpg_to_word
)

PORT = 5570
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Job status tracking for live progress bar
jobs_lock = threading.Lock()
active_jobs: Dict[str, Dict[str, Any]] = {}

last_heartbeat = time.time()
has_received_heartbeat = False


def get_default_output_dir() -> str:
    """Returns the default Windows Downloads directory for saved conversions."""
    user_home = os.path.expanduser("~")
    downloads_dir = os.path.join(user_home, "Downloads")
    if os.path.exists(downloads_dir):
        return downloads_dir
    documents_dir = os.path.join(user_home, "Documents")
    if os.path.exists(documents_dir):
        return documents_dir
    return user_home


class DocShieldHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def end_headers(self):
        # Strict anti-cache headers for instant UI updates & localhost privacy
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Health & System Status API
        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status_data = {
                "name": "ConvertMyDocuments",
                "version": "1.1.0",
                "status": "online",
                "mode": "100% Offline (Localhost)",
                "default_output_dir": get_default_output_dir(),
                "port": PORT
            }
            self.wfile.write(json.dumps(status_data).encode("utf-8"))
            return

        # Job Progress Polling API
        if path == "/api/progress":
            job_id = query.get("job_id", [""])[0]
            with jobs_lock:
                job_data = active_jobs.get(job_id, {"percent": 0, "status": "Menunggu...", "done": False})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(job_data).encode("utf-8"))
            return

        # Direct file download API
        if path == "/api/download":
            file_path = query.get("file", [""])[0]
            if file_path and os.path.exists(file_path):
                filename = os.path.basename(file_path)
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
                self.send_header("Content-Length", str(os.path.getsize(file_path)))
                self.end_headers()
                with open(file_path, "rb") as f:
                    while chunk := f.read(65536):
                        self.wfile.write(chunk)
                return
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
                return

        # Serve static assets or fallback to index.html
        super().do_GET()

    def do_POST(self):
        global last_heartbeat, has_received_heartbeat
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Heartbeat endpoint
        if path == "/api/heartbeat":
            last_heartbeat = time.time()
            has_received_heartbeat = True
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"alive"}')
            return

        # Open File in Default Windows App API
        if path == "/api/open-file":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            data = json.loads(body)
            file_path = data.get("file_path", "")
            if file_path and os.path.exists(file_path):
                try:
                    os.startfile(file_path)
                    res = {"success": True}
                except Exception as e:
                    res = {"success": False, "error": str(e)}
            else:
                res = {"success": False, "error": "File does not exist"}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Open in Windows Explorer Highlight API
        if path == "/api/open-folder":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            data = json.loads(body)
            file_path = data.get("file_path", "")
            if file_path and os.path.exists(file_path):
                try:
                    # Windows Explorer /select
                    subprocess.Popen(f'explorer /select,"{os.path.normpath(file_path)}"')
                    res = {"success": True}
                except Exception as e:
                    res = {"success": False, "error": str(e)}
            else:
                res = {"success": False, "error": "File does not exist"}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Main Conversion Execution API
        if path == "/api/convert":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            payload = json.loads(body)

            job_id = payload.get("job_id", str(int(time.time() * 1000)))
            mode = payload.get("mode", "pdf_to_word")  # pdf_to_word, pdf_to_text, jpg_to_pdf, jpg_to_word
            files_payload = payload.get("files", [])
            options = payload.get("options", {})
            output_dir = payload.get("output_dir", get_default_output_dir())

            with jobs_lock:
                active_jobs[job_id] = {
                    "percent": 0,
                    "status": "Memproses berkas di memori lokal...",
                    "done": False,
                    "result": None,
                    "error": None
                }

            # Spawn conversion in a background worker thread
            def worker():
                try:
                    def update_progress(pct, msg):
                        with jobs_lock:
                            if job_id in active_jobs:
                                active_jobs[job_id]["percent"] = pct
                                active_jobs[job_id]["status"] = msg

                    # Extract options
                    ocr_mode = options.get("ocr_mode", "auto")
                    bleach_wm = options.get("bleach_watermark", False)
                    wm_threshold = int(options.get("watermark_threshold", 185))
                    unlock_pdf = options.get("unlock", True)
                    page_size = options.get("page_size", "fit")

                    # Decode input files into temporary directory
                    temp_dir = tempfile.mkdtemp(prefix="docshield_")
                    temp_paths = []

                    try:
                        for idx, fobj in enumerate(files_payload):
                            fname = fobj.get("name", f"file_{idx}")
                            b64data = fobj.get("data", "")
                            if "," in b64data:
                                b64data = b64data.split(",", 1)[1]
                            raw_bytes = base64.b64decode(b64data)
                            tpath = os.path.join(temp_dir, fname)
                            with open(tpath, "wb") as f_out:
                                f_out.write(raw_bytes)
                            temp_paths.append(tpath)

                        if not temp_paths:
                            raise ValueError("Tidak ada berkas yang diterima.")

                        # Determine primary output path
                        primary_input = temp_paths[0]
                        base_stem = os.path.splitext(os.path.basename(files_payload[0].get("name", "document")))[0]

                        result_data = {}

                        if mode == "pdf_to_word":
                            out_name = f"{base_stem}_converted.docx"
                            out_path = os.path.join(output_dir, out_name)
                            res = pdf_to_word(
                                input_path=primary_input,
                                output_path=out_path,
                                ocr_mode=ocr_mode,
                                bleach_watermark=bleach_wm,
                                watermark_threshold=wm_threshold,
                                unlock=unlock_pdf,
                                progress_callback=update_progress
                            )
                            result_data = res

                        elif mode == "pdf_to_text":
                            out_name = f"{base_stem}_extracted.txt"
                            out_path = os.path.join(output_dir, out_name)
                            res = pdf_to_text(
                                input_path=primary_input,
                                output_path=out_path,
                                ocr_mode=ocr_mode,
                                bleach_watermark=bleach_wm,
                                watermark_threshold=wm_threshold,
                                unlock=unlock_pdf,
                                progress_callback=update_progress
                            )
                            result_data = res

                        elif mode == "jpg_to_pdf":
                            out_name = f"{base_stem}_merged.pdf"
                            out_path = os.path.join(output_dir, out_name)
                            res = jpg_to_pdf(
                                image_paths=temp_paths,
                                output_path=out_path,
                                page_size=page_size,
                                progress_callback=update_progress
                            )
                            result_data = res

                        elif mode == "jpg_to_word":
                            out_name = f"{base_stem}_ocr.docx"
                            out_path = os.path.join(output_dir, out_name)
                            res = jpg_to_word(
                                image_paths=temp_paths,
                                output_path=out_path,
                                bleach_watermark=bleach_wm,
                                watermark_threshold=wm_threshold,
                                progress_callback=update_progress
                            )
                            result_data = res
                        else:
                            raise ValueError(f"Mode konversi tidak dikenal: {mode}")

                        with jobs_lock:
                            active_jobs[job_id]["percent"] = 100
                            active_jobs[job_id]["status"] = "Konversi selesai dengan sukses!"
                            active_jobs[job_id]["done"] = True
                            active_jobs[job_id]["result"] = result_data

                    finally:
                        # Clean up temporary decoded input files
                        try:
                            import shutil
                            shutil.rmtree(temp_dir, ignore_errors=True)
                        except Exception:
                            pass

                except Exception as ex:
                    import traceback
                    traceback.print_exc()
                    with jobs_lock:
                        active_jobs[job_id]["percent"] = 100
                        active_jobs[job_id]["status"] = f"Gagal: {str(ex)}"
                        active_jobs[job_id]["done"] = True
                        active_jobs[job_id]["error"] = str(ex)

            threading.Thread(target=worker, daemon=True).start()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"job_id": job_id, "status": "started"}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def launch_app_window(url: str):
    """
    Launches Microsoft Edge in dedicated App Mode with zero browser chrome,
    providing a seamless native desktop window experience.
    """
    edge_paths = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]

    user_data_dir = os.path.join(os.environ.get("LOCALAPPDATA", "."), "ConvertMyDocuments_Profile")
    os.makedirs(user_data_dir, exist_ok=True)

    for edge_exe in edge_paths:
        if os.path.exists(edge_exe):
            try:
                cmd = [
                    edge_exe,
                    f"--app={url}",
                    f"--user-data-dir={user_data_dir}",
                    "--window-size=1120,820",
                    "--disable-extensions",
                    "--disable-plugins",
                    "--disable-http-cache",
                    "--disk-cache-size=0",
                ]
                subprocess.Popen(cmd)
                return
            except Exception:
                pass

    # Fallback to default browser
    webbrowser.open(url)


def is_server_already_running(port: int) -> bool:
    """Checks if ConvertMyDocuments is already running on this port."""
    import urllib.request
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/status", method="GET")
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            if resp.status == 200:
                return True
    except Exception:
        return False
    return False


def run_server(open_browser: bool = True):
    global PORT
    if is_server_already_running(PORT):
        if open_browser:
            launch_app_window(f"http://127.0.0.1:{PORT}")
        return

    server_address = ("127.0.0.1", PORT)
    try:
        httpd = ThreadingHTTPServer(server_address, DocShieldHandler)
    except OSError:
        PORT = 5571
        httpd = ThreadingHTTPServer(("127.0.0.1", PORT), DocShieldHandler)

    active_port = httpd.server_port
    url = f"http://127.0.0.1:{active_port}"
    print(f"[*] ConvertMyDocuments Server active at {url}")

    if open_browser:
        threading.Timer(0.4, launch_app_window, args=[url]).start()

    # Watchdog thread: cleanly terminate server when window is closed
    def watchdog_loop():
        global last_heartbeat, has_received_heartbeat
        time.sleep(20)  # Initial startup grace period
        while True:
            time.sleep(3)
            if has_received_heartbeat:
                if time.time() - last_heartbeat > 12:
                    print("[*] Window closed by user. Terminating DocShield server...")
                    os._exit(0)

    threading.Thread(target=watchdog_loop, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == "__main__":
    run_server(open_browser=True)
