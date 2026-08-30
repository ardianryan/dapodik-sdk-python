"""
Hierarki Exception untuk Dapodik Python SDK
"""

from typing import Optional


class DapodikError(Exception):
    """Base exception class untuk semua error Dapodik SDK."""
    pass


class DapodikAuthError(DapodikError):
    """Exception ketika autentikasi gagal (HTTP 401 atau 403)."""

    def __init__(self, message: str = "Akses ditolak (401/403). Pastikan token dan IP client sudah didaftarkan di Pengaturan WebService Dapodik."):
        super().__init__(message)


class DapodikConnectionError(DapodikError):
    """Exception ketika gagal terhubung ke server Dapodik atau request timeout."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error


class DapodikHttpError(DapodikError):
    """Exception ketika WebService Dapodik mengembalikan status HTTP 4xx / 5xx."""

    def __init__(self, status_code: int, status_text: str, endpoint: str, raw_body: str = ""):
        self.status_code = status_code
        self.status_text = status_text
        self.endpoint = endpoint
        self.raw_body = raw_body
        super().__init__(
            f"Dapodik WebService HTTP {status_code} ({status_text}) saat memanggil endpoint '{endpoint}'"
        )
