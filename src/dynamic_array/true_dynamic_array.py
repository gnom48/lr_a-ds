from typing import Iterator, Optional, Any
from ctypes import Array, py_object
from collections.abc import MutableSequence


class DynamicArray[T](MutableSequence[T]):
    """
    Динамический массив на основе ctypes.Array (непрерывный блок памяти).
    """

    def __init__(self, initial_capacity: int = 10):
        if initial_capacity <= 0:
            raise ValueError("Начальная емкость должна быть положительной")

        self._capacity: int = initial_capacity
        self._size: int = 0
        # Массив C-уровня, хранящий ссылки на Python-объекты.
        # Аннотация Array[T | None] — вроде как только условная: ctypes.Array вроде не поддерживат generic,
        # поэтому реальный тип здесь Array[py_object].
        self._data: Array[T | None] = self._make_storage(initial_capacity)

    @staticmethod
    def _make_storage(capacity: int) -> Array[Any]:
        """Создаёт ctypes-массив из py_object, заполненный None."""
        storage = (capacity * py_object)()
        for i in range(capacity):
            storage[i] = None
        return storage

    def _resize(self, new_capacity: int) -> None:
        """Изменение размера внутреннего массива."""
        new_data = self._make_storage(new_capacity)
        for i in range(self._size):
            new_data[i] = self._data[i]

        self._data = new_data
        self._capacity = new_capacity

    def _check_index(self, index: int) -> None:
        if not isinstance(index, int):
            raise TypeError(
                f"Индекс должен быть целым числом, но передан {type(index)}")

        if index < 0 or index >= self._size:
            raise IndexError(
                f"Индекс {index} выходит за границы массива (размер: {self._size})")

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
            self._resize(max(self._capacity // 2, 10))

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._data[i]

    def __contains__(self, item: object) -> bool:
        """
        Проверка вхождения элемента.
        Использует линейный поиск.

        Args:
            item: Элемент для поиска

        Returns:
            True, если элемент найден, иначе False
        """
        for i in range(self._size):
            if self._data[i] == item:
                return True
        return False

    def contains_binary_search(self, item: T) -> bool:
        """
        Проверка вхождения элемента.
        Использует бинарный поиск (требует отсортированный массив).

        Args:
            item: Элемент для поиска

        Returns:
            True, если элемент найден, иначе False

        Raises:
            TypeError: Если элементы не поддерживают сравнение
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
                "Элементы массива должны поддерживать операции сравнения "
                "для бинарного поиска")

        return False

    def __repr__(self) -> str:
        elements = [str(self._data[i]) for i in range(self._size)]
        return f"DynamicArray([{', '.join(elements)}])"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DynamicArray):
            return NotImplemented

        if self._size != other._size:
            return False

        for i in range(self._size):
            if self._data[i] != other._data[i]:
                return False

        return True

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

    def append(self, value: T) -> None:
        if self._size >= self._capacity:
            self._resize(self._capacity * 2)

        self._data[self._size] = value
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

    def reverse(self) -> None:
        left, right = 0, self._size - 1

        while left < right:
            self._data[left], self._data[right] = (
                self._data[right],
                self._data[left],
            )
            left += 1
            right -= 1

    def index(self, value: T, start: int = 0,
              stop: Optional[int] = None) -> int:
        if stop is None:
            stop = self._size

        for i in range(start, min(stop, self._size)):
            if self._data[i] == value:
                return i

        raise ValueError(f"Элемент {value} не найден в массиве")

    def count(self, value: T) -> int:
        count = 0
        for i in range(self._size):
            if self._data[i] == value:
                count += 1
        return count

    def clear(self) -> None:
        self._data = self._make_storage(self._capacity)
        self._size = 0

    def sort(self, key=None, reverse: bool = False) -> None:
        """
        Сортировка через оптимальный list.sort

        Args:
            key: Функция для извлечения ключа сортировки
            reverse: Сортировка по убыванию
        """
        items = [self._data[i] for i in range(self._size)]
        items.sort(key=key, reverse=reverse)

        for i in range(self._size):
            self._data[i] = items[i]

    @property
    def capacity(self) -> int:
        return self._capacity
