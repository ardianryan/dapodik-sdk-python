"""
Core Dapodik Client untuk WebService Dapodik Kemendikdasmen (Python 3.9+)
"""

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, Generator, List, Optional, Union

from dapodik.errors import (
    DapodikAuthError,
    DapodikConnectionError,
    DapodikError,
    DapodikHttpError,
)
from dapodik.models import DapodikResponse


class DapodikClient:
    """
    Client resmi untuk berkomunikasi dengan WebService Dapodik Kemendikdasmen (port 5774).
    Menggunakan standard library `urllib` (Zero Runtime Dependencies).
    """

    def __init__(
        self,
        npsn: str,
        token: str,
        host: Optional[str] = "127.0.0.1",
        port: Optional[Union[int, str]] = 5774,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        if not npsn or not str(npsn).strip():
            raise DapodikError("NPSN wajib diisi")
        if "\r" in str(npsn) or "\n" in str(npsn):
            raise DapodikError("NPSN tidak boleh mengandung karakter newline")

        if not token or not str(token).strip():
            raise DapodikError("Token WebService Dapodik wajib diisi")
        if "\r" in str(token) or "\n" in str(token):
            raise DapodikError("Token tidak boleh mengandung karakter newline (CRLF injection prevention)")

        self.npsn = str(npsn).strip()
        self.token = str(token).strip()
        self.timeout = float(timeout)

        if base_url:
            self.base_url = base_url.rstrip("/")
        else:
            host_str = str(host or "127.0.0.1").strip()
            if not host_str.startswith("http://") and not host_str.startswith("https://"):
                host_str = f"http://{host_str}"
            self.base_url = f"{host_str}:{port}/WebService"

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
    ) -> DapodikResponse:
        """
        Mengirim HTTP Request ke endpoint WebService Dapodik.
        """
        clean_endpoint = endpoint.lstrip("/")
        if ".." in clean_endpoint or "\\" in clean_endpoint:
            raise DapodikError("Endpoint tidak valid (path traversal detected)")

        query_dict = {"npsn": self.npsn}
        if params:
            query_dict.update({k: v for k, v in params.items() if v is not None})

        query_string = urllib.parse.urlencode(query_dict)
        url = f"{self.base_url}/{clean_endpoint}?{query_string}"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "dapodik-sdk-python/1.0.0",
        }

        data_bytes = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data_bytes = json.dumps(body).encode("utf-8")

        req = urllib.request.Request(
            url=url,
            data=data_bytes,
            headers=headers,
            method=method.upper(),
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                status_code = response.getcode()
                raw_bytes = response.read()
                raw_text = raw_bytes.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            status_code = e.code
            raw_text = e.read().decode("utf-8", errors="replace") if e.fp else ""

            if status_code in (401, 403):
                raise DapodikAuthError(
                    f"Akses ditolak ({status_code}). Periksa token atau whitelist IP client di Pengaturan WebService Dapodik."
                ) from e
            raise DapodikHttpError(status_code, e.reason, clean_endpoint, raw_text) from e
        except urllib.error.URLError as e:
            raise DapodikConnectionError(
                f"Gagal terhubung ke server Dapodik ({self.base_url}): {e.reason}", e
            ) from e
        except Exception as e:
            raise DapodikConnectionError(f"Request timeout / connection error: {str(e)}", e) from e

        if not raw_text.strip():
            return DapodikResponse([], {})

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise DapodikError(f"Respons bukan JSON yang valid dari Dapodik: {raw_text[:200]}") from exc

        # Ekstraksi dan normalisasi rows
        rows: List[Dict[str, Any]] = []
        if isinstance(parsed, list):
            rows = parsed
        elif isinstance(parsed, dict):
            if "rows" in parsed:
                if isinstance(parsed["rows"], dict):
                    # Penanganan respons single object (seperti getSekolah)
                    rows = [parsed["rows"]]
                elif isinstance(parsed["rows"], list):
                    rows = parsed["rows"]
            elif "data" in parsed and isinstance(parsed["data"], list):
                rows = parsed["data"]
            else:
                rows = [parsed]

        return DapodikResponse(rows, parsed if isinstance(parsed, dict) else {})

    # =========================================================================
    # Endpoint Standar (GET)
    # =========================================================================

    def get_sekolah(self, semester_id: Optional[str] = None, **params: Any) -> DapodikResponse:
        """Menarik profil dan perizinan operasional sekolah."""
        q = dict(params)
        if semester_id:
            q["semester_id"] = semester_id
        return self.request("GET", "getSekolah", q)

    def get_pengguna(self, **params: Any) -> DapodikResponse:
        """Menarik akun operator dan pengguna Dapodik."""
        return self.request("GET", "getPengguna", params)

    def get_gtk(self, page: int = 1, limit: Optional[int] = None, **params: Any) -> DapodikResponse:
        """Menarik data Guru dan Tenaga Kependidikan (GTK)."""
        q = {"page": page}
        if limit:
            q["limit"] = limit
        q.update(params)
        return self.request("GET", "getGtk", q)

    def get_rombongan_belajar(self, semester_id: Optional[str] = None, **params: Any) -> DapodikResponse:
        """Menarik data rombongan belajar (kelas) beserta anggota dan pembelajaran."""
        q = dict(params)
        if semester_id:
            q["semester_id"] = semester_id
        return self.request("GET", "getRombonganBelajar", q)

    def get_peserta_didik(self, page: int = 1, limit: Optional[int] = None, **params: Any) -> DapodikResponse:
        """Menarik data siswa / peserta didik."""
        q = {"page": page}
        if limit:
            q["limit"] = limit
        q.update(params)
        return self.request("GET", "getPesertaDidik", q)

    def get_mata_pelajaran(self, semester_id: Optional[str] = None, **params: Any) -> DapodikResponse:
        """Menarik data referensi mata pelajaran nasional."""
        q = dict(params)
        if semester_id:
            q["semester_id"] = semester_id
        return self.request("GET", "getMataPelajaran", q)

    def get_matev_nilai(self, semester_id: Optional[str] = None, **params: Any) -> DapodikResponse:
        """Menarik referensi mata evaluasi nilai."""
        q = dict(params)
        if semester_id:
            q["semester_id"] = semester_id
        return self.request("GET", "getMatevNilai", q)

    # =========================================================================
    # Endpoint Tulis (POST)
    # =========================================================================

    def post(self, endpoint: str, body: Any, **params: Any) -> DapodikResponse:
        """Mengirim data via HTTP POST ke WebService Dapodik."""
        return self.request("POST", endpoint, params, body)

    def post_matev_rapor(self, body: Any, **params: Any) -> DapodikResponse:
        """Mengirim data mata evaluasi rapor."""
        return self.post("postMatevRapor", body, **params)

    def post_nilai(self, body: Any, table: str = "rapor", **params: Any) -> DapodikResponse:
        """Mengirim data nilai rapor ke tabel rapor."""
        p = dict(params)
        p["table"] = table
        return self.post("postNilai", body, **p)

    # =========================================================================
    # Auto-Pagination & Streaming Generators
    # =========================================================================

    def iterate_peserta_didik(self, limit: int = 100, **params: Any) -> Generator[List[Dict[str, Any]], None, None]:
        """Generator stream per-batch halaman siswa untuk efisiensi RAM."""
        page = 1
        while True:
            resp = self.get_peserta_didik(page=page, limit=limit, **params)
            if not resp.rows:
                break
            yield resp.rows
            if len(resp.rows) < limit:
                break
            page += 1

    def fetch_all_peserta_didik(
        self,
        limit: int = 100,
        delay_seconds: float = 0.0,
        on_progress: Optional[Callable[[int, int, int], None]] = None,
        **params: Any,
    ) -> DapodikResponse:
        """Menarik seluruh data siswa secara otomatis melintasi banyak halaman."""
        all_rows: List[Dict[str, Any]] = []
        page = 1

        while True:
            resp = self.get_peserta_didik(page=page, limit=limit, **params)
            count = len(resp.rows)
            if count == 0:
                break

            all_rows.extend(resp.rows)
            if on_progress:
                on_progress(page, count, len(all_rows))

            if count < limit:
                break

            page += 1
            if delay_seconds > 0:
                time.sleep(delay_seconds)

        return DapodikResponse(all_rows)

    def fetch_all_gtk(
        self,
        limit: int = 100,
        delay_seconds: float = 0.0,
        on_progress: Optional[Callable[[int, int, int], None]] = None,
        **params: Any,
    ) -> DapodikResponse:
        """Menarik seluruh data GTK secara otomatis melintasi banyak halaman."""
        all_rows: List[Dict[str, Any]] = []
        page = 1

        while True:
            resp = self.get_gtk(page=page, limit=limit, **params)
            count = len(resp.rows)
            if count == 0:
                break

            all_rows.extend(resp.rows)
            if on_progress:
                on_progress(page, count, len(all_rows))

            if count < limit:
                break

            page += 1
            if delay_seconds > 0:
                time.sleep(delay_seconds)

        return DapodikResponse(all_rows)

    # =========================================================================
    # Aliases
    # =========================================================================

    def sekolah(self, semester_id: Optional[str] = None, **params: Any) -> DapodikResponse:
        return self.get_sekolah(semester_id=semester_id, **params)

    def pengguna(self, **params: Any) -> DapodikResponse:
        return self.get_pengguna(**params)

    def gtk(self, page: int = 1, limit: Optional[int] = None, **params: Any) -> DapodikResponse:
        return self.get_gtk(page=page, limit=limit, **params)

    def rombel(self, semester_id: Optional[str] = None, **params: Any) -> DapodikResponse:
        return self.get_rombongan_belajar(semester_id=semester_id, **params)

    def pd(self, page: int = 1, limit: Optional[int] = None, **params: Any) -> DapodikResponse:
        return self.get_peserta_didik(page=page, limit=limit, **params)

    def mata_pelajaran(self, semester_id: Optional[str] = None, **params: Any) -> DapodikResponse:
        return self.get_mata_pelajaran(semester_id=semester_id, **params)

    def matev_nilai(self, semester_id: Optional[str] = None, **params: Any) -> DapodikResponse:
        return self.get_matev_nilai(semester_id=semester_id, **params)


class Dapodik:
    """Factory helper class."""

    def __init__(self, host: str = "127.0.0.1", port: Union[int, str] = 5774, timeout: float = 30.0):
        self.host = host
        self.port = port
        self.timeout = timeout

    def api(self, token: str, npsn: str) -> DapodikClient:
        return DapodikClient(
            npsn=npsn,
            token=token,
            host=self.host,
            port=self.port,
            timeout=self.timeout,
        )
