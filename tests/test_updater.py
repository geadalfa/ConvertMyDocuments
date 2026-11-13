"""
test_updater.py
Unit tests and integration tests for ConvertMyDocuments updater engine and settings APIs.
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from updater import parse_version, compare_versions, is_newer_version, UpdateManager
import server


class TestVersionParsing(unittest.TestCase):
    def test_parse_version(self):
        self.assertEqual(parse_version("v1.1.2"), (1, 1, 2))
        self.assertEqual(parse_version("1.2.0"), (1, 2, 0))
        self.assertEqual(parse_version("v2.0.0-beta"), (2, 0, 0))
        self.assertEqual(parse_version(""), (0, 0, 0))
        self.assertEqual(parse_version(None), (0, 0, 0))

    def test_compare_versions(self):
        self.assertEqual(compare_versions("1.2.0", "1.1.2"), 1)
        self.assertEqual(compare_versions("v1.1.2", "1.1.2"), 0)
        self.assertEqual(compare_versions("1.0.9", "1.1.2"), -1)

    def test_is_newer_version(self):
        self.assertTrue(is_newer_version("1.2.0", "1.1.2"))
        self.assertFalse(is_newer_version("1.1.2", "1.1.2"))
        self.assertFalse(is_newer_version("1.1.0", "1.1.2"))


class TestUpdateManager(unittest.TestCase):
    def setUp(self):
        self.mgr = UpdateManager(app_name="ConvertMyDocuments", current_version="1.1.2")

    def test_initial_status(self):
        status = self.mgr.get_status()
        self.assertEqual(status["status"], "idle")
        self.assertEqual(status["current_version"], "1.1.2")
        self.assertFalse(status["update_available"])

    @patch("urllib.request.urlopen")
    def test_check_for_updates_available(self, mock_urlopen):
        fake_release = {
            "tag_name": "v1.2.0",
            "name": "ConvertMyDocuments v1.2.0",
            "body": "Fitur baru konversi ultra cepat",
            "html_url": "https://github.com/geadalfa/ConvertMyDocuments/releases/tag/v1.2.0",
            "published_at": "2026-11-13T12:00:00Z",
            "assets": [
                {
                    "name": "ConvertMyDocuments_Setup_v1.2.0.exe",
                    "browser_download_url": "https://github.com/geadalfa/ConvertMyDocuments/releases/download/v1.2.0/ConvertMyDocuments_Setup_v1.2.0.exe",
                    "size": 135000000
                },
                {
                    "name": "ConvertMyDocuments-v1.2.0-portable.zip",
                    "browser_download_url": "https://github.com/geadalfa/ConvertMyDocuments/releases/download/v1.2.0/ConvertMyDocuments-v1.2.0-portable.zip",
                    "size": 179000000
                }
            ]
        }
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps(fake_release).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        res = self.mgr.check_for_updates(force=True)
        self.assertEqual(res["status"], "available")
        self.assertTrue(res["update_available"])
        self.assertEqual(res["latest_version"], "1.2.0")
        self.assertEqual(res["release_info"]["download_url"], "https://github.com/geadalfa/ConvertMyDocuments/releases/download/v1.2.0/ConvertMyDocuments_Setup_v1.2.0.exe")

    @patch("urllib.request.urlopen")
    def test_check_for_updates_up_to_date(self, mock_urlopen):
        fake_release = {
            "tag_name": "v1.1.2",
            "name": "ConvertMyDocuments v1.1.2",
            "assets": []
        }
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps(fake_release).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        res = self.mgr.check_for_updates(force=True)
        self.assertEqual(res["status"], "up_to_date")
        self.assertFalse(res["update_available"])

    def test_settings_auto_update_default(self):
        settings = server.load_settings()
        self.assertIn("auto_update", settings)
        self.assertTrue(settings["auto_update"])


if __name__ == "__main__":
    unittest.main()
