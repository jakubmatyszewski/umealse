"""Utilities"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

class Status(Enum):
    """Enum class for consistent status codes."""

    OK = "OK"
    ERROR = "Error"


@dataclass
class StatusMessage:
    """Status class for consistent status message format."""

    status: Status
    message: str
    data: Optional[Any] = None

    def info(self) -> Dict[str, str]:
        return {"status": self.status.value, "message": self.message}
