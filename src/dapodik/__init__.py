"""
Dapodik SDK for Python
~~~~~~~~~~~~~~~~~~~~~~

Modern, lightweight, type-safe Python SDK untuk WebService Dapodik Kemendikdasmen.

:copyright: (c) 2026 Ryan Ardian & SMA Negeri 1 Gedeg.
:license: MIT, see LICENSE for more details.
"""

from dapodik.client import Dapodik, DapodikClient
from dapodik.errors import (
    DapodikAuthError,
    DapodikConnectionError,
    DapodikError,
    DapodikHttpError,
)
from dapodik.models import DapodikResponse

__version__ = "1.0.0"
__author__ = "Ryan Ardian <inisaya@ardianryan.com>"
__all__ = [
    "Dapodik",
    "DapodikClient",
    "DapodikResponse",
    "DapodikError",
    "DapodikAuthError",
    "DapodikConnectionError",
    "DapodikHttpError",
]
