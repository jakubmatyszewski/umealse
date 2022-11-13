"""Utilities"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class Status(Enum):
    """Enum class for consistent status codes."""

    OK = "OK"
    ERROR = "Error"


@dataclass
class StatusMessage:
    """Status class for consistent status message format."""

    status: Status
    message: str

    def info(self) -> Dict[str, str]:
        return {"status": self.status.value, "message": self.message}
