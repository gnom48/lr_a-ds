import os
import json
import tempfile

import pytest

from src.heap import Heap
from src.models.student import Student


def make_student(name: str = "Иванов И.И.",
                 group: str = "PZ-21",
                 course: int = 2,
                 age: int = 18,
                 grade: float = 4.0) -> Student:
    return Student(name, group, course, age, grade)


@pytest.fixture
def empty_heap():
    return Heap()


@pytest.fixture
def filled_heap():
    h = Heap()
    for i in range(10):
        h.push(make_student(name=f"Student{i}", grade=3.0 + i * 0.1))
    return h


@pytest.fixture
def sample_students():
    return [make_student(name=f"Student{i}", grade=3.0 + i * 0.1) for i in range(10)]


class TestBasicOperations:
    def test_empty_on_creation(self, empty_heap):
        assert len(empty_heap) == 0
        assert empty_heap.is_empty()
        assert empty_heap.peek() is None

    def test_push_increases_len(self, empty_heap):
        empty_heap.push(make_student())
        assert len(empty_heap) == 1
        assert not empty_heap.is_empty()

        empty_heap.push(make_student(name="Петров П.П.", grade=5.0))
        assert len(empty_heap) == 2

    def test_peek_does_not_remove(self, filled_heap):
        top = filled_heap.peek()
        assert top is not None
        assert len(filled_heap) == 10
        assert filled_heap.peek() is top

    def test_peek_returns_max(self, filled_heap):
        # максимальный балл в фикстуре — 3.9
        assert filled_heap.peek().average_grade == pytest.approx(3.9)

    def test_len_after_mixed_ops(self, empty_heap):
        for i in range(20):
            empty_heap.push(make_student(name=f"S{i}", grade=3.0 + i * 0.1))
        for _ in range(7):
            empty_heap.pop()
        assert len(empty_heap) == 13


class TestPop:
    def test_pop_empty_returns_none(self, empty_heap):
        assert empty_heap.pop() is None

    def test_pop_single(self, empty_heap):
        s = make_student(grade=4.2)
        empty_heap.push(s)
        assert empty_heap.pop() == s
        assert empty_heap.is_empty()

    def test_pop_returns_max(self, filled_heap):
        top = filled_heap.pop()
        assert top.average_grade == pytest.approx(3.9)
        assert len(filled_heap) == 9

    def test_pop_returns_descending_order(self, filled_heap):
        grades = []
        while not filled_heap.is_empty():
            grades.append(filled_heap.pop().average_grade)
        assert grades == sorted(grades, reverse=True)

    def test_pop_removes_element_completely(self, empty_heap):
        s = make_student(name="Уникум", grade=5.0)
        empty_heap.push(s)
        empty_heap.push(make_student(name="Второй", grade=3.0))
        empty_heap.pop()
        assert not empty_heap.contains_full(s)


class TestHeapInvariant:
    def test_invariant_after_push(self, empty_heap):
        """После каждой вставки родитель >= детей."""
        import random
        random.seed(42)
        for i in range(50):
            empty_heap.push(make_student(
                name=f"S{i}", grade=random.uniform(2.0, 5.0)))
        _assert_heap_invariant(empty_heap)

    def test_invariant_after_pop(self, filled_heap):
        for _ in range(5):
            filled_heap.pop()
            _assert_heap_invariant(filled_heap)

    def test_duplicates_do_not_loop(self, empty_heap):
        """Все баллы одинаковы — не должно быть зависания."""
        for i in range(20):
            empty_heap.push(make_student(name=f"S{i}", grade=4.5))
        assert len(empty_heap) == 20
        assert empty_heap.pop().average_grade == pytest.approx(4.5)

    def test_duplicates_order_arbitrary_but_grades_sorted(self, empty_heap):
        for i in range(10):
            empty_heap.push(make_student(name=f"S{i}", grade=4.0))
        grades = [empty_heap.pop().average_grade for _ in range(10)]
        assert grades == [4.0] * 10


def _assert_heap_invariant(h: Heap):
    """Проверка, что массив внутри h — корректная max-heap."""
    data = h._data
    n = len(data)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n:
            assert data[i].average_grade >= data[left].average_grade
        if right < n:
            assert data[i].average_grade >= data[right].average_grade


class TestContainsFull:
    def test_found_when_fully_equal(self, filled_heap, sample_students):
        for s in sample_students:
            assert filled_heap.contains_full(s)

    def test_not_found_when_grade_differs(self, filled_heap):
        # тот же студент, но балл другой
        wrong = make_student(name="Student3", grade=99.0)
        assert not filled_heap.contains_full(wrong)

    def test_not_found_when_name_differs(self, filled_heap):
        wrong = make_student(name="Несуществующий", grade=3.3)
        assert not filled_heap.contains_full(wrong)

    def test_not_found_on_empty(self, empty_heap):
        assert not empty_heap.contains_full(make_student())

    def test_found_after_push(self, empty_heap):
        s = make_student(name="Новичок", grade=4.7)
        empty_heap.push(s)
        assert empty_heap.contains_full(s)


class TestContainsByKey:
    def test_found_existing_grades(self, filled_heap):
        for i in range(10):
            assert filled_heap.contains_by_key(3.0 + i * 0.1)

    def test_not_found_missing_grade(self, filled_heap):
        assert not filled_heap.contains_by_key(2.5)
        assert not filled_heap.contains_by_key(5.0)

    def test_multiple_students_same_grade(self, empty_heap):
        empty_heap.push(make_student(name="A", grade=4.5))
        empty_heap.push(make_student(name="B", grade=4.5))
        empty_heap.push(make_student(name="C", grade=4.5))
        assert empty_heap.contains_by_key(4.5)

    def test_epsilon_for_float(self, empty_heap):
        empty_heap.push(make_student(grade=1 / 3))  # 0.3333...
        assert empty_heap.contains_by_key(0.3333333)  # в пределах eps
        assert not empty_heap.contains_by_key(0.34)   # вне eps

    def test_empty_heap(self, empty_heap):
        assert not empty_heap.contains_by_key(4.0)


class TestBuild:
    def test_build_makes_valid_heap(self, sample_students):
        h = Heap()
        h.build(sample_students)
        _assert_heap_invariant(h)
        assert len(h) == 10

    def test_build_sorts_via_pop(self, sample_students):
        h = Heap()
        h.build(sample_students)
        grades = [h.pop().average_grade for _ in range(10)]
        assert grades == sorted(grades, reverse=True)

    def test_build_from_reverse_sorted(self):
        """Худший случай для наивного build, лучший — для heapify."""
        h = Heap()
        students = [make_student(
            name=f"S{i}", grade=3.0 + i * 0.1) for i in range(20)]
        h.build(students)
        _assert_heap_invariant(h)

    def test_build_overwrites_existing(self, filled_heap, sample_students):
        filled_heap.build(sample_students[:3])
        assert len(filled_heap) == 3

    def test_build_on_empty_list(self, empty_heap):
        empty_heap.build([])
        assert empty_heap.is_empty()
        assert empty_heap.pop() is None


class TestSaveLoad:
    def test_save_creates_file(self, filled_heap, tmp_path):
        path = tmp_path / "heap.json"
        filled_heap.save(str(path))
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["size"] == 10
        assert len(data["items"]) == 10

    def test_load_restores_size_and_data(self, filled_heap, sample_students, tmp_path):
        path = tmp_path / "heap.json"
        filled_heap.save(str(path))

        restored = Heap()
        restored.load(str(path))

        assert len(restored) == 10
        for s in sample_students:
            assert restored.contains_full(s)

    def test_load_restores_heap_property(self, filled_heap, tmp_path):
        path = tmp_path / "heap.json"
        filled_heap.save(str(path))

        restored = Heap()
        restored.load(str(path))
        _assert_heap_invariant(restored)

    def test_load_overwrites_current_state(self, filled_heap, tmp_path):
        path = tmp_path / "heap.json"
        filled_heap.save(str(path))

        other = Heap()
        other.push(make_student(name="Чужой", grade=5.0))
        other.load(str(path))
        assert not other.contains_full(make_student(name="Чужой", grade=5.0))
        assert len(other) == 10

    def test_roundtrip_preserves_order(self, filled_heap, tmp_path):
        path = tmp_path / "heap.json"
        filled_heap.save(str(path))

        restored = Heap()
        restored.load(str(path))

        original_grades = [filled_heap.pop().average_grade for _ in range(10)]
        restored_grades = [restored.pop().average_grade for _ in range(10)]
        assert original_grades == restored_grades


class TestEdgeCases:
    def test_many_pushes_and_pops(self, empty_heap):
        import random
        random.seed(1)
        for i in range(1000):
            empty_heap.push(make_student(
                name=f"S{i}", grade=random.uniform(2, 5)))
        while len(empty_heap) > 1:
            a = empty_heap.pop()
            b = empty_heap.peek()
            assert a.average_grade >= b.average_grade

    def test_pop_until_empty(self, filled_heap):
        for _ in range(10):
            filled_heap.pop()
        assert filled_heap.is_empty()
        assert filled_heap.pop() is None

    def test_negative_and_zero_grades(self, empty_heap):
        empty_heap.push(make_student(grade=0.0))
        empty_heap.push(make_student(grade=-1.0))
        empty_heap.push(make_student(grade=5.0))
        assert empty_heap.pop().average_grade == 5.0
        assert empty_heap.pop().average_grade == 0.0
        assert empty_heap.pop().average_grade == -1.0
