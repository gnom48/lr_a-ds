from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Book:
    author: str
    publisher: str
    pages: int
    price: float
    isbn: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
