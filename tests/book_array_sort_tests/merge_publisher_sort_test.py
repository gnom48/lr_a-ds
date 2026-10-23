import pytest

from src.models.book import Book
from src.book_array import BookArray


class TestMergeSortPublisher:
    def test_ascending(self, filled: BookArray) -> None:
        filled.sort_by_publisher()
        pubs = [b.publisher for b in filled]
        assert pubs == sorted(pubs)

    def test_stable_within_same_publisher(self, filled: BookArray) -> None:
        filled.sort_by_publisher()
        ek = [b.author for b in filled if b.publisher == "Эксмо"]
        assert ek == ["Толстой", "Чехов", "Гончаров"]

    @pytest.mark.parametrize("n", [0, 1, 2])
    def test_trivial_sizes(self, n: int) -> None:
        arr = BookArray([Book(f"A{i}", "P", 1, 1.0, i) for i in range(n)])
        arr.sort_by_publisher()
        assert len(arr) == n
