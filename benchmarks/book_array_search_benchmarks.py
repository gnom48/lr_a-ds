import pytest

from src.models.book import Book
from src.book_array import BookArray


def make_books(n: int) -> list[Book]:
    return [
        Book(
            author=f"Author{i:05d}",
            publisher=f"Pub{i % 50:02d}",
            pages=100 + (i * 37) % 1000,
            price=float((i * 53) % 2000),
            isbn=1000 + i,
        )
        for i in range(n)
    ]


class TestBenchmarkJumpSearch:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_jump_search(self, benchmark, n: int) -> None:
        books = make_books(n)
        arr = BookArray(books)
        arr.sort_by_author()
        target = arr[n // 2].author

        def run() -> None:
            arr.jump_search_by_author(target)

        benchmark(run)


class TestBenchmarkBinarySearch:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_binary_search(self, benchmark, n: int) -> None:
        books = make_books(n)
        arr = BookArray(books)
        arr.sort_by_publisher()
        target = arr[n // 2].publisher

        def run() -> None:
            arr.binary_search_by_publisher(target)

        benchmark(run)
