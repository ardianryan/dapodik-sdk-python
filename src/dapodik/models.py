"""
Data models and collection wrapper for Dapodik Python SDK
"""

from typing import Any, Dict, Iterator, List, Optional, Sequence


class DapodikResponse(Sequence[Dict[str, Any]]):
    """
    Wrapper respons Dapodik yang mengemas data baris (rows) dengan kemampuan
    filtering, mapping, dan konversi instan ke Pandas DataFrame.
    """

    def __init__(self, rows: List[Dict[str, Any]], raw_response: Optional[Dict[str, Any]] = None):
        self._rows = rows
        self._raw = raw_response or {}

    def __len__(self) -> int:
        return len(self._rows)

    def __getitem__(self, index: Any) -> Any:
        return self._rows[index]

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        return iter(self._rows)

    def __repr__(self) -> str:
        return f"<DapodikResponse count={len(self._rows)}>"

    @property
    def rows(self) -> List[Dict[str, Any]]:
        """Mengembalikan list of dictionaries dari data baris."""
        return self._rows

    @property
    def first(self) -> Optional[Dict[str, Any]]:
        """Mengembalikan baris pertama atau None jika kosong."""
        return self._rows[0] if self._rows else None

    @property
    def count(self) -> int:
        """Jumlah item."""
        return len(self._rows)

    def filter(self, **conditions: Any) -> "DapodikResponse":
        """
        Memfilter data berdasarkan key-value criteria.
        Contoh: response.filter(jenis_kelamin="L", tingkatan_pendidikan_id="10")
        """
        filtered = [
            row for row in self._rows
            if all(row.get(k) == v for k, v in conditions.items())
        ]
        return DapodikResponse(filtered, self._raw)

    def pluck(self, key: str) -> List[Any]:
        """Mengambil satu field tertentu dari seluruh baris."""
        return [row.get(key) for row in self._rows if key in row]

    def to_list(self) -> List[Dict[str, Any]]:
        """Mengonversi ke Python list of dicts."""
        return list(self._rows)

    def to_dataframe(self) -> Any:
        """
        Mengonversi data respons menjadi Pandas DataFrame.
        Memerlukan pustaka `pandas` (`pip install dapodik-sdk[dataframe]`).
        """
        try:
            import pandas as pd
            return pd.DataFrame(self._rows)
        except ImportError as exc:
            raise ImportError(
                "Pustaka 'pandas' belum terpasang. Pasang dengan: pip install 'dapodik-sdk[dataframe]' atau pip install pandas"
            ) from exc
