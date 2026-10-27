from typing import Optional, Callable, Any, Generic, TypeVar

T = TypeVar("T")


class MaxHeap(Generic[T]):
    def __init__(self, key: Callable[[T], Any] = lambda x: x) -> None:
        self._data: list[T] = []
        self._key = key

    def push(self, value: T) -> None:
        self._data.append(value)
        self.__up(len(self._data) - 1)

    def pop(self) -> Optional[T]:
        if not self._data:
            return None
        if len(self._data) == 1:
            return self._data.pop()
        top = self._data[0]
        self._data[0] = self._data.pop()
        self.__down(0)
        return top

    def __up(self, i: int) -> None:
        parent = (i - 1) // 2
        while i > 0 and self._key(self._data[parent]) < self._key(self._data[i]):
            self._data[parent], self._data[i] = self._data[i], self._data[parent]
            i = parent
            parent = (i - 1) // 2

    def __down(self, i: int) -> None:
        n = len(self._data)
        while True:
            l, r = 2 * i + 1, 2 * i + 2
            gr = i
            if l < n and self._key(self._data[l]) > self._key(self._data[gr]):
                gr = l
            if r < n and self._key(self._data[r]) > self._key(self._data[gr]):
                gr = r
            if gr == i:
                break
            self._data[i], self._data[gr] = self._data[gr], self._data[i]
            i = gr

    def build(self, items: list[T]) -> None:
        self._data = list(items)
        for i in range(len(self._data) // 2 - 1, -1, -1):
            self.__down(i)

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def peek(self) -> Optional[T]:
        return self._data[0] if self._data else None
