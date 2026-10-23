import pytest

from src.models.book import Book
from src.book_array import BookArray


class TestJumpSearchAuthor:
    def test_raises_when_not_sorted(self, filled: BookArray) -> None:
        with pytest.raises(ValueError):
            filled.jump_search_by_author("Толстой")

    def test_find_existing(self, filled: BookArray) -> None:
        filled.sort_by_author()
        idx = filled.jump_search_by_author("Пушкин")
        assert idx != -1
        assert filled[idx].author == "Пушкин"

    def test_first_and_last(self, filled: BookArray) -> None:
        filled.sort_by_author()
        authors = [b.author for b in filled]
        first = filled.jump_search_by_author(authors[0])
        last = filled.jump_search_by_author(authors[-1])
        assert filled[first].author == authors[0]
        assert filled[last].author == authors[-1]

    def test_missing(self, filled: BookArray) -> None:
        filled.sort_by_author()
        assert filled.jump_search_by_author("Некрасов") == -1

    def test_empty(self, empty: BookArray) -> None:
        # пустой массив считается отсортированным, поиск вернёт -1
        assert empty.jump_search_by_author("Пушкин") == -1
