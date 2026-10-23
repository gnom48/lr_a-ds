import pytest

from src.models.book import Book
from src.book_array import BookArray


class TestHeapSortPages:
    def test_descending(self, filled: BookArray) -> None:
        filled.sort_by_pages_desc()
        pages = [b.pages for b in filled]
        assert pages == sorted(pages, reverse=True)
        assert pages[0] == 1200
        assert pages[-1] == 250

    def test_empty(self, empty: BookArray) -> None:
        empty.sort_by_pages_desc()
        assert len(empty) == 0

    def test_single(self) -> None:
        arr = BookArray([Book("A", "P", 42, 1.0, 1)])
        arr.sort_by_pages_desc()
        assert arr[0].pages == 42
