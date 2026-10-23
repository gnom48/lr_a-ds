import pytest

from src.models.book import Book
from src.book_array import BookArray


class TestBinarySearchPublisher:
    def test_raises_when_not_sorted(self, filled: BookArray) -> None:
        with pytest.raises(ValueError):
            filled.binary_search_by_publisher("Эксмо")

    def test_find_existing(self, filled: BookArray) -> None:
        filled.sort_by_publisher()
        idx = filled.binary_search_by_publisher("Азбука")
        assert idx != -1
        assert filled[idx].publisher == "Азбука"

    def test_returns_first_occurrence(self, filled: BookArray) -> None:
        filled.sort_by_publisher()
        idx = filled.binary_search_by_publisher("Эксмо")
        # Эксмо встречается несколько раз — должен вернуться первый
        assert filled[idx].publisher == "Эксмо"
        assert idx == 0 or filled[idx - 1].publisher != "Эксмо"

    def test_missing(self, filled: BookArray) -> None:
        filled.sort_by_publisher()
        assert filled.binary_search_by_publisher("МИФ") == -1

    def test_empty(self, empty: BookArray) -> None:
        assert empty.binary_search_by_publisher("Эксмо") == -1
