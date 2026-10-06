import pytest

from src.heap import Heap
from src.models.student import Student, make_student


# ---------- Фикстуры ----------

@pytest.fixture
def heap():
    return Heap()


@pytest.fixture
def filled():
    """10 студентов с баллами 3.0, 3.1, ..., 3.9."""
    h = Heap()
    for i in range(10):
        h.push(make_student(name=f"S{i}", grade=3.0 + i * 0.1))
    return h


def assert_heap_invariant(h: Heap) -> None:
    """Родитель >= детей. Ловит поломку __down/__up."""
    data = h._data
    n = len(data)
    assert n > 0
    for i in range(n):
        for child in (2 * i + 1, 2 * i + 2):
            if child < n:
                assert data[i].average_grade >= data[child].average_grade


# ---------- Базовые операции ----------

class TestBasic:
    def test_empty(self, heap):
        assert len(heap) == 0
        assert heap.is_empty()
        assert heap.peek() is None
        assert heap.pop() is None

    def test_push_and_len(self, heap):
        heap.push(make_student())
        assert len(heap) == 1
        assert not heap.is_empty()

    def test_peek_returns_max_without_removing(self, filled):
        top = filled.peek()
        assert top.average_grade == pytest.approx(3.9)
        assert len(filled) == 10

    def test_pop_returns_max_and_shrinks(self, filled):
        assert filled.pop().average_grade == pytest.approx(3.9)
        assert len(filled) == 9

    def test_pop_single(self, heap):
        s = make_student(grade=4.2)
        heap.push(s)
        assert heap.pop() == s
        assert heap.is_empty()

    def test_mixed_ops_len(self, heap):
        for i in range(20):
            heap.push(make_student(name=f"S{i}", grade=3.0 + i * 0.1))
        for _ in range(7):
            heap.pop()
        assert len(heap) == 13


# ---------- Инвариант кучи (главный тест на __up/__down) ----------

class TestInvariant:
    def test_after_push(self, heap):
        import random
        random.seed(42)
        for i in range(50):
            heap.push(make_student(name=f"S{i}", grade=random.uniform(2, 5)))
        assert_heap_invariant(heap)

    def test_after_pop(self, filled):
        for _ in range(5):
            filled.pop()
            assert_heap_invariant(filled)

    def test_duplicates(self, heap):
        for i in range(20):
            heap.push(make_student(name=f"S{i}", grade=4.5))
        assert len(heap) == 20
        assert [heap.pop().average_grade for _ in range(20)] == [4.5] * 20


# ---------- contains_full / contains_by_key ----------

class TestContains:
    def test_full_found_and_not_found(self, filled):
        assert filled.contains_full(make_student(name="S3", grade=3.3))
        assert not filled.contains_full(make_student(name="S3", grade=99.0))
        assert not filled.contains_full(make_student(name="Нет", grade=3.3))

    def test_full_on_empty(self, heap):
        assert not heap.contains_full(make_student())

    def test_by_key_found_and_not_found(self, filled):
        assert filled.contains_by_key(3.5)
        assert not filled.contains_by_key(2.5)

    def test_by_key_epsilon(self, heap):
        heap.push(make_student(grade=1 / 3))
        assert heap.contains_by_key(0.3333333, eps=1e-6)
        assert not heap.contains_by_key(0.34)

    def test_by_key_on_empty(self, heap):
        assert not heap.contains_by_key(4.0)


# ---------- build ----------

class TestBuild:
    def test_build_makes_valid_heap(self):
        h = Heap()
        h.build([make_student(name=f"S{i}", grade=3.0 + i * 0.1)
                 for i in range(10)])
        assert_heap_invariant(h)
        assert len(h) == 10

    def test_build_overwrites(self, filled):
        filled.build([make_student(name="A", grade=5.0)])
        assert len(filled) == 1
        assert filled.peek().average_grade == 5.0

    def test_build_empty(self, heap):
        heap.build([])
        assert heap.is_empty()
        assert heap.pop() is None


# ---------- Student: сравнения (ловит опечатку __bg__) ----------

class TestStudentComparison:
    def test_lt_gt(self):
        a = make_student(grade=3.0)
        b = make_student(grade=4.0)
        assert a < b
        assert b > a

    def test_eq(self):
        a = make_student(name="X", grade=4.0)
        b = make_student(name="X", grade=4.0)
        c = make_student(name="X", grade=4.1)
        assert a == b
        assert a != c
