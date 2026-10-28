from typing import Iterable
from typing import Any, Callable, Iterable

from src.models.book import Book
from .max_heap import MaxHeap


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
        """Сортировка слиянием по возрастанию поля publisher"""
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
        buckets: list[list[Book]] = [[] for _ in range(max_k - min_k + 1)]
        for b in items:
            buckets[key(b) - min_k].append(b)
        output: list[Book] = []
        for i in range(len(buckets) - 1, -1, -1):
            output.extend(buckets[i])
        return output

    def sort_by_isbn_desc(self) -> None:
        """Сортировка подсчётом по убыванию поля isbn"""
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
            j = i - 1
            while j >= 0 and key(arr[j]) > key(cur):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = cur
        return arr

    def sort_by_price(self) -> None:
        """Сортировка вставками по возрастанию поля price"""
        self._items = self.insertion_sort(self._items, key=lambda b: b.price)
    # endregion

    # region heap_sort: pages, по убыванию

    def sort_by_pages_desc(self) -> None:
        """Сортировка кучей по убыванию поля pages через max-heap"""
        heap = MaxHeap(key=lambda b: b.pages)
        heap.build(self._items)
        self._items = [heap.pop() for _ in range(len(heap))]
    # endregion

    # region jump_search по author

    def sort_by_author(self) -> None:
        """Сортировка слиянием по возрастанию поля author (готовит данные под jump_search)"""
        self._items = self.merge_sort(self._items, key=lambda b: b.author)

    def _is_sorted_asc(self, key: Callable[[Book], Any]) -> bool:
        return all(key(self._items[i]) <= key(self._items[i + 1])
                   for i in range(len(self._items) - 1))

    def jump_search_by_author(self, author: str) -> int:
        """
        Скачкообразный поиск по полю author.
        Возвращает индекс первого совпадения. Если элемента нет — -1.
        Бросает ValueError, если массив не отсортирован по author.
        """
        if not self._is_sorted_asc(lambda b: b.author):
            raise ValueError("Массив не отсортирован по полю 'author'")

        n = len(self._items)
        if n == 0:
            return -1

        step = int(n ** 0.5)
        prev = 0
        while prev < n and self._items[min(step, n) - 1].author < author:
            prev = step
            step += int(n ** 0.5)
            if prev >= n:
                return -1

        while prev < min(step, n) and self._items[prev].author < author:
            prev += 1

        if prev < n and self._items[prev].author == author:
            return prev
        return -1
    # endregion

    # region binary_search по publisher
    def sort_by_publisher_asc(self) -> None:
        """Сортировка слиянием по возрастанию поля publisher (готовит данные под binary_search)"""
        self._items = self.merge_sort(self._items, key=lambda b: b.publisher)

    def binary_search_by_publisher(self, publisher: str) -> int:
        """
        Бинарный поиск по полю publisher.
        Возвращает индекс первого совпадения. Если элемента нет — -1.
        Бросает ValueError, если массив не отсортирован по publisher.
        """
        if not self._is_sorted_asc(lambda b: b.publisher):
            raise ValueError("Массив не отсортирован по полю 'publisher'")

        lo, hi = 0, len(self._items) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            val = self._items[mid].publisher
            if val < publisher:
                lo = mid + 1
            elif val > publisher:
                hi = mid - 1
            else:
                # идём к первому вхождению
                while mid > 0 and self._items[mid - 1].publisher == publisher:
                    mid -= 1
                return mid
        return -1
    # endregion
