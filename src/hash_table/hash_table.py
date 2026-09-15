class HashTable[A, B]:
    CAPACITY_MULTIPLICATION_FACTOR = 2
    START_CAPACITY = 5

    def __init__(self, start_capacity: int | None = None):
        self._capacity: int = self.START_CAPACITY if start_capacity is None or start_capacity <= 0 else start_capacity
        self._size: int = 0
        self._data: list[list[tuple[A, B]]] = [[]
                                               for _ in range(self._capacity)]

    def __index(self, key: A) -> int:
        """Рассчитывает индекс бакета"""
        return key.__hash__() % self._capacity

    def __getitem__(self, key: A) -> B:
        for k, v in self._data[self.__index(key=key)]:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key: A, value: B) -> None:
        i = self.__index(key=key)
        bucket = self._data[i]
        for bucket_tuple_index in range(0, len(bucket)):
            if bucket[bucket_tuple_index][0] == key:
                bucket[bucket_tuple_index] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / self._capacity > 0.75:
            self._capacity *= self.CAPACITY_MULTIPLICATION_FACTOR
            self.__rebuild()

    def __delitem__(self, key: A) -> None:
        i = self.__index(key=key)
        bucket = self._data[i]
        for bucket_tuple_index in range(0, len(bucket)):
            if bucket[bucket_tuple_index][0] == key:
                del bucket[bucket_tuple_index]
                self._size -= 1
                if self._capacity > self.START_CAPACITY and self._size / self._capacity < 0.2:
                    self._capacity = max(
                        self._capacity // 2, self.START_CAPACITY)
                    self.__rebuild()
                return
        raise KeyError(key)

    def __rebuild(self) -> None:
        """Пересборка по новым бакетам"""
        swap_data = self._data
        self._data = [[] for _ in range(self._capacity)]
        self._size = 0
        for swap_bucket in swap_data:
            for swap_k, swap_v in swap_bucket:
                self.__setitem__(swap_k, swap_v)

    def __len__(self) -> int:
        """Всего пар"""
        return self._size

    def __contains__(self, key: A) -> bool:
        """Проверка вхождения через свой же __getitem__"""
        try:
            self.__getitem__(key=key)
            return True
        except KeyError:
            return False

    def contains_direct(self, key: A) -> bool:
        """Прямая проверка"""
        bucket = self._data[self.__index(key)]
        for k, _ in bucket:
            if k == key:
                return True
        return False

    def __iter__(self):
        for bucket in self._data:
            for k, v in bucket:
                yield k, v

    @property
    def capacity(self) -> int:
        """Текущее число бакетов (для тестов)."""
        return self._capacity
