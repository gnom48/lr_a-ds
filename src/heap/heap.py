import json
from typing import Optional

from src.models.student import Student


class Heap[S: Student]:
    def __init__(self):
        self._data: list[S] = list()

    def push(self, value: S) -> None:
        """Добавить в кучу новый элемент"""
        self._data.append(value)
        self.__up(len(self._data) - 1)

    def pop(self) -> Optional[S]:
        """Извлечь корень"""
        if not self._data:
            return None
        if len(self._data) == 1:
            return self._data.pop()
        gr = self._data[0]
        self._data[0] = self._data.pop()
        self.__down(0)
        return gr

    def __up(self, i: int) -> None:
        """Поднимать выше пока больше родителя"""
        parent = (i - 1) // 2
        while i > 0 and self._data[parent] < self._data[i]:
            self._data[parent], self._data[i] = self._data[i], self._data[parent]
            i = parent
            parent = (i - 1) // 2

    def __down(self, i: int) -> None:
        n = len(self._data)
        while True:
            l_child, r_child = 2 * i + 1, 2 * i + 2
            gr = i
            if l_child < n and self._data[l_child] > self._data[gr]:
                gr = l_child
            if r_child < n and self._data[r_child] > self._data[gr]:
                gr = r_child
            if gr == i:
                break
            self._data[i], self._data[gr] = self._data[gr], self._data[i]
            i = gr

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def peek(self) -> Optional[Student]:
        """Вернуть корень, не удаляя"""
        return self._data[0] if self._data else None

    # ---------- Вхождение ----------
    def contains_full(self, student: Student) -> bool:
        """
        Проверка вхождения по полям
        """
        return any(s == student for s in self._data)

    def contains_by_key(self, average_grade: float, eps: float = 1e-9) -> bool:
        """
        Проверка вхождения по ключу
        """
        return any(abs(s.average_grade - average_grade) < eps for s in self._data)

    # ---------- Сериализация ----------
    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"items": [s.to_dict() for s in self._data]},
                      f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        students = [Student.from_dict(d) for d in data["items"]]
        self.build(students)

    def build(self, students: list[S]) -> None:
        """Построить кучу из готового списка"""
        self._data = list(students)
        for i in range(len(self._data) // 2 - 1, -1, -1):
            self.__down(i)
