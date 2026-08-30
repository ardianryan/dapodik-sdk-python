"""
Unit tests untuk Dapodik Python SDK
"""

import json
import unittest
from unittest.mock import MagicMock, patch
import urllib.error

from dapodik import Dapodik, DapodikClient, DapodikResponse
from dapodik.errors import (
    DapodikAuthError,
    DapodikConnectionError,
    DapodikError,
    DapodikHttpError,
)


class TestDapodikClient(unittest.TestCase):

    def setUp(self):
        self.client = DapodikClient(
            npsn="20300001",
            token="secret-token-12345",
            host="192.168.1.50",
            port=5774,
        )

    def test_validation_empty_config(self):
        with self.assertRaises(DapodikError):
            DapodikClient(npsn="", token="123")
        with self.assertRaises(DapodikError):
            DapodikClient(npsn="20300001", token="")

    @patch("urllib.request.urlopen")
    def test_get_sekolah_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.read.return_value = json.dumps({
            "status": "success",
            "rows": [{"sekolah_id": "s1", "nama": "SMA Negeri 1 Gedeg", "npsn": "20300001"}]
        }).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        res = self.client.get_sekolah()
        self.assertEqual(len(res), 1)
        self.assertEqual(res.first["nama"], "SMA Negeri 1 Gedeg")
        self.assertEqual(res.count, 1)

    @patch("urllib.request.urlopen")
    def test_get_sekolah_single_object_normalization(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.read.return_value = json.dumps({
            "status": "success",
            "rows": {"sekolah_id": "s1", "nama": "SMA Negeri 1 Gedeg"}
        }).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        res = self.client.sekolah()
        self.assertEqual(len(res), 1)
        self.assertEqual(res.first["nama"], "SMA Negeri 1 Gedeg")

    @patch("urllib.request.urlopen")
    def test_get_peserta_didik_alias_and_filtering(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.read.return_value = json.dumps({
            "status": "success",
            "rows": [
                {"peserta_didik_id": "p1", "nama": "Budi", "jenis_kelamin": "L"},
                {"peserta_didik_id": "p2", "nama": "Siti", "jenis_kelamin": "P"},
            ]
        }).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        res = self.client.pd(page=1, limit=50)
        self.assertEqual(len(res), 2)
        self.assertEqual(res.pluck("nama"), ["Budi", "Siti"])

        filtered = res.filter(jenis_kelamin="L")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.first["nama"], "Budi")

    @patch("urllib.request.urlopen")
    def test_auth_error_on_401(self, mock_urlopen):
        mock_err = urllib.error.HTTPError(
            url="http://test", code=401, msg="Unauthorized", hdrs={}, fp=None
        )
        mock_urlopen.side_effect = mock_err

        with self.assertRaises(DapodikAuthError):
            self.client.get_sekolah()

    @patch("urllib.request.urlopen")
    def test_http_error_on_500(self, mock_urlopen):
        mock_err = urllib.error.HTTPError(
            url="http://test", code=500, msg="Internal Server Error", hdrs={}, fp=None
        )
        mock_urlopen.side_effect = mock_err

        with self.assertRaises(DapodikHttpError):
            self.client.get_gtk()

    @patch("urllib.request.urlopen")
    def test_post_nilai(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.read.return_value = json.dumps({
            "status": "success",
            "message": "Tersimpan"
        }).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        res = self.client.post_nilai([{"nilai": 90}], semester_id="20241")
        self.assertEqual(res.first["message"], "Tersimpan")

    @patch("urllib.request.urlopen")
    def test_fetch_all_peserta_didik(self, mock_urlopen):
        page1 = json.dumps({"status": "success", "rows": [{"nama": "A"}, {"nama": "B"}]}).encode("utf-8")
        page2 = json.dumps({"status": "success", "rows": [{"nama": "C"}]}).encode("utf-8")

        mock1 = MagicMock()
        mock1.getcode.return_value = 200
        mock1.read.return_value = page1
        mock1.__enter__.return_value = mock1

        mock2 = MagicMock()
        mock2.getcode.return_value = 200
        mock2.read.return_value = page2
        mock2.__enter__.return_value = mock2

        mock_urlopen.side_effect = [mock1, mock2]

        all_pd = self.client.fetch_all_peserta_didik(limit=2)
        self.assertEqual(len(all_pd), 3)
        self.assertEqual(all_pd.pluck("nama"), ["A", "B", "C"])

    def test_factory_class(self):
        dapodik = Dapodik("127.0.0.1", 5774)
        client = dapodik.api(token="tok", npsn="20300001")
        self.assertIsInstance(client, DapodikClient)
        self.assertEqual(client.npsn, "20300001")


if __name__ == "__main__":
    unittest.main()
