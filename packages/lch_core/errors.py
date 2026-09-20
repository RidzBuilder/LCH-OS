from dataclasses import dataclass


@dataclass
class LchError(Exception):
    code: str
    message: str
    retryable: bool = False

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"
