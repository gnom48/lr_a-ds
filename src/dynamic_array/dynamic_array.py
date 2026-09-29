from typing import Iterator, Any


INITIAL_CAPACITY = 10


class DynamicArray[T]:
    """
    Динамический массив.
    """

    def __init__(self, initial_capacity: int = INITIAL_CAPACITY) -> None:
        if initial_capacity <= 0:
            raise ValueError("Начальная емкость должна быть положительной")

        self._capacity: int = initial_capacity
        self._size: int = 0
        self._data: list[T | None] = [None] * initial_capacity

    def _resize(self, new_capacity: int) -> None:
        new_data: list[T | None] = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def _check_index(self, index: int) -> None:
        if not isinstance(index, int):
            raise TypeError(
                f"Индекс должен быть целым числом, не {type(index)}")
        if index < 0 or index >= self._size:
            raise IndexError(
                f"Индекс {index} выходит за границы массива (размер: {self._size})"
            )

    def __getitem__(self, index: int) -> T:
        self._check_index(index)
        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        self._check_index(index)
        self._data[index] = value

    def __delitem__(self, index: int) -> None:
        self._check_index(index)

        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._size -= 1
        self._data[self._size] = None

        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(max(self._capacity // 2, INITIAL_CAPACITY))

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._data[i]

    def __repr__(self) -> str:
        elements = ", ".join(str(self._data[i]) for i in range(self._size))
        return f"DynamicArray([{elements}])"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DynamicArray):
            return NotImplemented
        if self._size != other._size:
            return False
        for i in range(self._size):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __contains__(self, item: object) -> bool:
        """
        Линейный поиск. Сложность O(n).
        """
        for i in range(self._size):
            if self._data[i] == item:
                return True
        return False

    def contains_binary_search(self, item: T) -> bool:
        """
        Бинарный поиск. Сложность O(log n).
        Требует, чтобы массив был отсортирован.

        Raises:
            TypeError: если элементы не поддерживают сравнение
        """
        if self._size == 0:
            return False

        left, right = 0, self._size - 1
        try:
            while left <= right:
                mid = (left + right) // 2
                mid_value = self._data[mid]

                if mid_value == item:
                    return True
                elif mid_value < item:
                    left = mid + 1
                else:
                    right = mid - 1
        except TypeError:
            raise TypeError(
                "Элементы массива должны поддерживать операции сравнения"
            )
        return False

    def sum(self, start: T = 0) -> T:
        """
        Сумма всех элементов.

        Args:
            start: Начальное значение (по умолчанию 0)

        Returns:
            Сумма всех элементов
        """
        return sum(self, start)

    def average(self) -> float:
        """
        Среднее арифметическое всех элементов.

        Returns:
            Среднее арифметическое

        Raises:
            ValueError: если массив пуст
        """
        if self._size == 0:
            raise ValueError("Нельзя вычислить среднее для пустого массива")
        return self.sum() / self._size

    def append(self, value: T) -> None:
        if self._size >= self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index: int, value: T) -> None:
        if index < 0:
            index = max(0, self._size + index)
        elif index > self._size:
            index = self._size

        if self._size >= self._capacity:
            self._resize(self._capacity * 2)

        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1

    def pop(self, index: int = -1) -> T:
        if self._size == 0:
            raise IndexError("Нельзя удалить элемент из пустого массива")
        if index < 0:
            index = self._size + index
        self._check_index(index)

        value = self._data[index]
        del self[index]
        return value

    def clear(self) -> None:
        self._data = [None] * self._capacity
        self._size = 0

    def sort(self, key=None, reverse: bool = False) -> None:
        """Сортировка через list.sort (Timsort, O(n log n))."""
        items = [self._data[i] for i in range(self._size)]
        items.sort(key=key, reverse=reverse)
        for i in range(self._size):
            self._data[i] = items[i]

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def size(self) -> int:
        return self._size
