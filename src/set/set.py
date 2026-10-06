from typing import Iterator, Any
from collections.abc import MutableSet

from src.dynamic_array.dynamic_array import DynamicArray


# TODO: переделать: главное что set не должен давать доступ по индексу
class Set[T](MutableSet[T]):
    """
    Множество на основе DynamicArray
    """

    def __init__(self, initial_capacity: int = 10) -> None:
        self._data: DynamicArray[T] = DynamicArray(initial_capacity)
        # self._data: list[T] = [None * initial_capacity]
        self._sorted: bool = True

    def _check_index(self, index: int) -> None:
        if not isinstance(index, int):
            raise TypeError(
                f"Индекс должен быть целым числом, получен {type(index)}")
        if index < 0 or index >= len(self._data):
            raise IndexError(
                f"Индекс {index} выходит за границы множества (размер: {len(self._data)})"
            )

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __contains__(self, item: object) -> bool:
        """
        Проверка вхождения через линейный поиск
        """
        return item in self._data

    def contains_binary_search(self, item: T) -> bool:
        """
        Проверка вхождения через бинарный поиск.
        Требует, чтобы множество было отсортировано.
        """
        if not self._sorted:
            self._data.sort()
            self._sorted = True
        return self._data.contains_binary_search(item)

    def __getitem__(self, index: int) -> T:
        self._check_index(index)
        return self._data[index]

    def __delitem__(self, index: int) -> None:
        self._check_index(index)
        del self._data[index]

    def add(self, value: T) -> None:
        """Добавляет элемент, если его ещё нет"""
        if value not in self._data:
            self._data.append(value)
            self._sorted = False

    def remove(self, value: T) -> None:
        """
        Удаляет элемент
        Args:
            value: 
        Raises:
            KeyError: если элемента нет
        """
        for i in range(len(self._data)):
            if self._data[i] == value:
                del self._data[i]
                return
        raise KeyError(value)

    def discard(self, value: T) -> None:
        """ Удаляет элемент, если он есть. Не бросает KeyError."""
        for i in range(len(self._data)):
            if self._data[i] == value:
                del self._data[i]
                return

    def pop(self) -> T:
        """Удаляет и возвращает произвольный элемент"""
        if len(self._data) == 0:
            raise KeyError("pop from an empty set")
        return self._data.pop()

    def clear(self) -> None:
        self._data.clear()
        self._sorted = True

    # region логические операторы для множеств

    def union(self, other: "Set[T]") -> "Set[T]":
        """ Объединение: возвращает новое множество со всеми элементами из self и other (без дубликатов)"""
        result: Set[T] = Set()
        for item in self:
            result.add(item)
        for item in other:
            result.add(item)
        return result

    def intersect(self, other: "Set[T]") -> "Set[T]":
        """ Пересечение: возвращает новое множество с элементами, которые есть и в self, и в other"""
        result: Set[T] = Set()
        smaller, larger = (self, other) if len(
            self) <= len(other) else (other, self)
        for item in smaller:
            if item in larger:
                result.add(item)
        return result

    def difference(self, other: "Set[T]") -> "Set[T]":
        """ Разность: элементы self, которых нет в other."""
        result: Set[T] = Set()
        for item in self:
            if item not in other:
                result.add(item)
        return result

    def symmetric_difference(self, other: "Set[T]") -> "Set[T]":
        """ Симметрическая разность: элементы, входящие ровно в одно из множеств."""
        result: Set[T] = Set()
        for item in self:
            if item not in other:
                result.add(item)
        for item in other:
            if item not in self:
                result.add(item)
        return result

    def __or__(self, other: "Set[T]") -> "Set[T]":
        return self.union(other)

    def __and__(self, other: "Set[T]") -> "Set[T]":
        return self.intersect(other)

    def __sub__(self, other: "Set[T]") -> "Set[T]":
        return self.difference(other)

    def __xor__(self, other: "Set[T]") -> "Set[T]":
        return self.symmetric_difference(other)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        if len(self) != len(other):
            return False
        for item in self:
            if item not in other:
                return False
        return True

    # endregion

    def __repr__(self) -> str:
        elements = ", ".join(str(x) for x in self._data)
        return f"Set({{{elements}}})"

    def __str__(self) -> str:
        return self.__repr__()
