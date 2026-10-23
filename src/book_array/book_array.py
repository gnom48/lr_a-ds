from typing import Iterable
from typing import Any, Callable, Iterable

from src.models.book import Book


class BookArray:
    def __init__(self, items: Iterable[Book] | None = None) -> None:
        self._items: list[Book] = list(items) if items is not None else []

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> Book:
        return self._items[index]

    def __setitem__(self, index: int, value: Book) -> None:
        self._items[index] = value

    def __iter__(self):
        return iter(self._items)

    def append(self, book: Book) -> None:
        self._items.append(book)

    def to_list(self) -> list[Book]:
        return list(self._items)

    # region merge_sort: publisher, по возрастанию
    @staticmethod
    def merge_sort(items: list[Book], key: Callable[[Book], Any]) -> list[Book]:
        if len(items) <= 1:
            return list(items)
        mid = len(items) // 2
        left = BookArray.merge_sort(items[:mid], key)
        right = BookArray.merge_sort(items[mid:], key)
        return BookArray._merge(left, right, key)

    @staticmethod
    def _merge(left: list[Book], right: list[Book],
               key: Callable[[Book], Any]) -> list[Book]:
        result: list[Book] = []
        i = j = 0
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort_by_publisher(self) -> None:
        """Сортировка слиянием по возрастанию поля publisher."""
        self._items = self.merge_sort(self._items, key=lambda b: b.publisher)
    # endregion

    # region counting_sort: isbn, по убыванию
    @staticmethod
    def counting_sort_desc(items: list[Book],
                           key: Callable[[Book], int]) -> list[Book]:
        if not items:
            return []
        keys = [key(b) for b in items]
        min_k, max_k = min(keys), max(keys)
        size = max_k - min_k + 1
        counts = [0] * size
        for k in keys:
            counts[k - min_k] += 1
        for i in range(1, size):
            counts[i] += counts[i - 1]
        output: list[Book | None] = [None] * len(items)
        for i in range(len(items) - 1, -1, -1):
            k = keys[i] - min_k
            output[counts[k] - 1] = items[i]
            counts[k] -= 1
        return list(reversed(output))

    def sort_by_isbn_desc(self) -> None:
        """Сортировка подсчётом по убыванию поля isbn."""
        self._items = self.counting_sort_desc(
            self._items, key=lambda b: b.isbn)
    # endregion

    # region insertion_sort: price, по возрастанию
    @staticmethod
    def insertion_sort(items: list[Book],
                       key: Callable[[Book], Any]) -> list[Book]:
        arr = list(items)
        for i in range(1, len(arr)):
            cur = arr[i]
            cur_key = key(cur)
            j = i - 1
            while j >= 0 and key(arr[j]) > cur_key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = cur
        return arr

    def sort_by_price(self) -> None:
        """Сортировка вставками по возрастанию поля price."""
        self._items = self.insertion_sort(self._items, key=lambda b: b.price)
    # endregion

    # region heap_sort: pages, по убыванию
    @staticmethod
    def _sift_down(items: list[Book], start: int, end: int,
                   key: Callable[[Book], Any]) -> None:
        root = start
        while 2 * root + 1 <= end:
            child = 2 * root + 1
            swap = root
            if key(items[swap]) < key(items[child]):
                swap = child
            if child + 1 <= end and key(items[swap]) < key(items[child + 1]):
                swap = child + 1
            if swap == root:
                return
            items[root], items[swap] = items[swap], items[root]
            root = swap

    @staticmethod
    def heap_sort(items: list[Book],
                  key: Callable[[Book], Any]) -> list[Book]:
        arr = list(items)
        n = len(arr)
        for start in range((n - 2) // 2, -1, -1):
            BookArray._sift_down(arr, start, n - 1, key)
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            BookArray._sift_down(arr, 0, end - 1, key)
        return arr

    def sort_by_pages_desc(self) -> None:
        """Сортировка кучей по убыванию поля pages."""
        self._items = list(reversed(
            self.heap_sort(self._items, key=lambda b: b.pages)
        ))
    # endregion
