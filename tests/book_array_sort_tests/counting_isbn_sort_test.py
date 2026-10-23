import pytest

from src.models.book import Book
from src.book_array import BookArray


class TestCountingSortIsbn:
    def test_descending(self, filled: BookArray) -> None:
        filled.sort_by_isbn_desc()
        isbns = [b.isbn for b in filled]
        assert isbns == sorted(isbns, reverse=True)
        assert isbns[0] == 909
        assert isbns[-1] == 101

    def test_empty(self, empty: BookArray) -> None:
        empty.sort_by_isbn_desc()
        assert len(empty) == 0

    def test_single(self) -> None:
        arr = BookArray([Book("A", "P", 1, 1.0, 42)])
        arr.sort_by_isbn_desc()
        assert arr[0].isbn == 42
