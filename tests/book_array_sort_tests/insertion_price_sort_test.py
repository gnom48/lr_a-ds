import pytest

from src.models.book import Book
from src.book_array import BookArray


class TestInsertionSortPrice:
    def test_ascending(self, filled: BookArray) -> None:
        filled.sort_by_price()
        prices = [b.price for b in filled]
        assert prices == sorted(prices)

    def test_stable_within_same_price(self) -> None:
        arr = BookArray([
            Book("A", "P", 10, 100.0, 1),
            Book("B", "P", 20,  50.0, 2),
            Book("C", "P", 30, 100.0, 3),
            Book("D", "P", 40,  50.0, 4),
        ])
        arr.sort_by_price()
        assert [b.author for b in arr] == ["B", "D", "A", "C"]

    @pytest.mark.parametrize("n", [0, 1, 2])
    def test_trivial_sizes(self, n: int) -> None:
        arr = BookArray([Book(f"A{i}", "P", 1, float(i), i) for i in range(n)])
        arr.sort_by_price()
        assert len(arr) == n
