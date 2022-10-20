"""Utilities"""
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    """Enum class for consistent status codes."""

    OK = "OK"
    ERROR = "Error"


@dataclass
class StatusMessage:
    """Status class for consistent status message format."""

    status: Status
    message: str

    def info(self) -> dict[str, str]:
        return {"status": self.status.value, "message": self.message}
