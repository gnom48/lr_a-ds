import pytest

from src.models.book import Book
from src.book_array import BookArray


def make_books(n: int) -> list[Book]:
    publishers = ["Эксмо", "АСТ", "Питер", "Азбука"]
    return [
        Book(
            author=f"Author{i}",
            publisher=publishers[(i * 3) % 4],
            pages=100 + (i * 37) % 1000,
            price=float((i * 53) % 2000),
            isbn=1000 + i * 7,
        )
        for i in range(n)
    ]


class TestBenchmarkMergeSort:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_merge_sort(self, benchmark, n: int) -> None:
        books = make_books(n)

        def run() -> None:
            BookArray(books).sort_by_publisher()

        benchmark(run)


class TestBenchmarkCountingSort:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_counting_sort(self, benchmark, n: int) -> None:
        books = make_books(n)

        def run() -> None:
            BookArray(books).sort_by_isbn_desc()

        benchmark(run)


class TestBenchmarkInsertionSort:
    @pytest.mark.parametrize("n", [100, 1_000, 5_000])
    def test_bench_insertion_sort(self, benchmark, n: int) -> None:
        books = make_books(n)

        def run() -> None:
            BookArray(books).sort_by_price()

        benchmark(run)


class TestBenchmarkHeapSort:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_heap_sort(self, benchmark, n: int) -> None:
        books = make_books(n)

        def run() -> None:
            BookArray(books).sort_by_pages_desc()

        benchmark(run)
