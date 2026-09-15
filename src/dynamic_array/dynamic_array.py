from typing import Iterator, Optional, Any
from collections.abc import MutableSequence


INITIAL_CAPACITY = 10


class DynamicArray[T](MutableSequence[T]):
    """
    Динамический массив
    """

    def __init__(self, initial_capacity: int = INITIAL_CAPACITY):
        """
        Инициализация динамического массива.

        Args:
            initial_capacity: Начальная емкость массива
        """
        if initial_capacity <= 0:
            raise ValueError("Начальная емкость должна быть положительной")

        self._capacity: int = initial_capacity
        self._size: int = 0
        self._data: list[Optional[T]] = [None] * initial_capacity

    def _resize(self, new_capacity: int) -> None:
        """
        Изменение размера внутреннего массива.

        Args:
            new_capacity: Новая емкость
        """
        new_data: list[Optional[T]] = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]

        self._data = new_data
        self._capacity = new_capacity

    def _check_index(self, index: int) -> None:
        """
        Проверка корректности индекса.

        Args:
            index: Индекс для проверки
        """
        if not isinstance(index, int):
            raise TypeError(
                f"Индекс должен быть целым числом, не {type(index)}")

        if index < 0 or index >= self._size:
            raise IndexError(
                f"Индекс {index} выходит за границы массива (размер: {self._size})")

    def __getitem__(self, index: int) -> T:
        """
        Получение элемента по индексу.

        Args:
            index: Индекс элемента

        Returns:
            Элемент массива
        """
        self._check_index(index)
        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        """
        Установка значения элемента по индексу.

        Args:
            index: Индекс элемента
            value: Новое значение
        """
        self._check_index(index)
        # FIXME: оказывается T это всего лишь строка-маркер типа, а не тип
        # if not isinstance(value, T):
        #     raise TypeError(f"Ожидался тип {T}, но передан {type(value)}")
        self._data[index] = value

    def __delitem__(self, index: int) -> None:
        """
        Удаление элемента по индексу.

        Args:
            index: Индекс элемента для удаления
        """
        self._check_index(index)

        # Сдвиг
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._size -= 1
        self._data[self._size] = None

        # Уменьшаем емкость, если фактический размер, например, в 4 раза меньше
        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(max(self._capacity // 2, INITIAL_CAPACITY))

    def __len__(self) -> int:
        """
        Возвращает количество элементов в массиве.

        Returns:
            Размер массива
        """
        return self._size

    def __iter__(self) -> Iterator[T]:
        """
        Итератор по элементам массива.

        Yields:
            Элементы массива
        """
        for i in range(self._size):
            yield self._data[i]

    def __contains__(self, item: T) -> bool:
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
                "Элементы массива должны поддерживать операции сравнения для бинарного поиска")

        return False

    def __repr__(self) -> str:
        """
        Строковое представление массива.

        Returns:
            Строка с элементами массива
        """
        elements = [str(self._data[i]) for i in range(self._size)]
        return f"DynamicArray([{', '.join(elements)}])"

    def __str__(self) -> str:
        """
        Пользовательское строковое представление.

        Returns:
            Строка с элементами массива
        """
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        """
        Сравнение массивов на равенство.

        Args:
            other: Другой объект для сравнения

        Returns:
            True, если массивы равны
        """
        if not isinstance(other, DynamicArray):
            return False

        if self._size != other._size:
            return False

        for i in range(self._size):
            if self._data[i] != other._data[i]:
                return False

        return True

    def insert(self, index: int, value: T) -> None:
        """
        Вставка элемента по индексу.

        Args:
            index: Позиция для вставки
            value: Значение для вставки
        """
        if index < 0:
            index = max(0, self._size + index)
        elif index > self._size:
            index = self._size

        if self._size >= self._capacity:
            self._resize(self._capacity * 2)

        # Сдвиг
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1

    def append(self, value: T) -> None:
        """
        Добавление элемента в конец массива.

        Args:
            value: Значение для добавления
        """
        if self._size >= self._capacity:
            self._resize(self._capacity * 2)

        self._data[self._size] = value
        self._size += 1

    def pop(self, index: int = -1) -> T:
        """
        Удаление и возврат элемента по индексу.

        Args:
            index: Индекс элемента (по умолчанию последний)

        Returns:
            Удаленный элемент
        """
        if self._size == 0:
            raise IndexError("Нельзя удалить элемент из пустого массива")

        if index < 0:
            index = self._size + index

        self._check_index(index)

        value = self._data[index]
        del self[index]
        return value  # type: ignore

    def reverse(self) -> None:
        """
        Изменение порядка элементов на противоположный.
        """
        left, right = 0, self._size - 1

        while left < right:
            self._data[left], self._data[right] = self._data[right], self._data[left]
            left += 1
            right -= 1

    def index(self, value: T, start: int = 0, stop: Optional[int] = None) -> int:
        """
        Поиск индекса первого вхождения элемента.

        Args:
            value: Искомое значение
            start: Начальный индекс поиска
            stop: Конечный индекс поиска

        Returns:
            Индекс первого вхождения

        Raises:
            ValueError: Если элемент не найден
        """
        if stop is None:
            stop = self._size

        for i in range(start, min(stop, self._size)):
            if self._data[i] == value:
                return i

        raise ValueError(f"Элемент {value} не найден в массиве")

    def count(self, value: T) -> int:
        """
        Подсчет количества вхождений элемента.

        Args:
            value: Искомое значение

        Returns:
            Количество вхождений
        """
        count = 0
        for i in range(self._size):
            if self._data[i] == value:
                count += 1
        return count

    def clear(self) -> None:
        """
        Очистка массива.
        """
        self._data = [None] * self._capacity
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
        """
        Текущая емкость массива.

        Returns:
            Емкость массива
        """
        return self._capacity
