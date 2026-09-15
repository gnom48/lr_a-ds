import pytest

from src.set import Set


# ---------- Фикстуры ----------

@pytest.fixture
def empty() -> Set[int]:
    return Set()


@pytest.fixture
def filled() -> Set[int]:
    s: Set[int] = Set()
    for x in [1, 2, 3, 4, 5]:
        s.add(x)
    return s


@pytest.fixture
def other() -> Set[int]:
    s: Set[int] = Set()
    for x in [4, 5, 6, 7]:
        s.add(x)
    return s


# ---------- Конструктор и len ----------

class TestInitLen:
    def test_empty(self, empty: Set[int]) -> None:
        assert len(empty) == 0

    def test_custom_capacity(self) -> None:
        s: Set[int] = Set(100)
        assert len(s) == 0

    def test_invalid_capacity(self) -> None:
        with pytest.raises(ValueError):
            Set(0)

    def test_len_after_add(self, empty: Set[int]) -> None:
        for i in range(5):
            empty.add(i)
        assert len(empty) == 5


# ---------- add / уникальность ----------

class TestAdd:
    def test_add_new(self, empty: Set[int]) -> None:
        empty.add(42)
        assert 42 in empty
        assert len(empty) == 1

    def test_add_duplicate_ignored(self, empty: Set[int]) -> None:
        empty.add(42)
        empty.add(42)
        empty.add(42)
        assert len(empty) == 1

    def test_add_many(self, empty: Set[int]) -> None:
        for i in range(100):
            empty.add(i)
        assert len(empty) == 100

    def test_add_strings(self) -> None:
        s: Set[str] = Set()
        for w in ["a", "b", "a", "c"]:
            s.add(w)
        assert len(s) == 3
        assert "b" in s


# ---------- __contains__ (линейный поиск) ----------

class TestContainsLinear:
    def test_present(self, filled: Set[int]) -> None:
        for x in [1, 2, 3, 4, 5]:
            assert x in filled

    def test_absent(self, filled: Set[int]) -> None:
        for x in [0, 6, 100, -1]:
            assert x not in filled

    def test_empty(self, empty: Set[int]) -> None:
        assert 1 not in empty


# ---------- contains_binary_search ----------

class TestBinarySearch:
    def test_found_when_sorted(self) -> None:
        s: Set[int] = Set()
        for x in [5, 1, 3, 2, 4]:
            s.add(x)
        s._data.sort()  # сортируем вручную, т.к. add сбрасывает _sorted
        s._sorted = True
        for x in [1, 2, 3, 4, 5]:
            assert s.contains_binary_search(x) is True

    def test_not_found(self) -> None:
        s: Set[int] = Set()
        for x in [1, 3, 5, 7, 9]:
            s.add(x)
        s._data.sort()
        for x in [0, 2, 4, 6, 10]:
            assert s.contains_binary_search(x) is False

    def test_empty(self, empty: Set[int]) -> None:
        assert empty.contains_binary_search(1) is False

    def test_single(self) -> None:
        s: Set[int] = Set()
        s.add(42)
        assert s.contains_binary_search(42) is True
        assert s.contains_binary_search(41) is False


# ---------- remove / pop / clear ----------

class TestRemove:
    def test_remove_existing(self, filled: Set[int]) -> None:
        filled.remove(3)
        assert 3 not in filled
        assert len(filled) == 4

    def test_remove_missing_raises(self, filled: Set[int]) -> None:
        with pytest.raises(KeyError):
            filled.remove(100)

    def test_remove_from_empty(self, empty: Set[int]) -> None:
        with pytest.raises(KeyError):
            empty.remove(1)


class TestPop:
    def test_pop_removes_one(self, filled: Set[int]) -> None:
        value = filled.pop()
        assert value not in filled
        assert len(filled) == 4

    def test_pop_empty_raises(self, empty: Set[int]) -> None:
        with pytest.raises(KeyError):
            empty.pop()


class TestClear:
    def test_clear(self, filled: Set[int]) -> None:
        filled.clear()
        assert len(filled) == 0
        assert list(filled) == []

    def test_clear_empty(self, empty: Set[int]) -> None:
        empty.clear()
        assert len(empty) == 0


# ---------- union ----------

class TestUnion:
    def test_union_basic(self, filled: Set[int], other: Set[int]) -> None:
        result = filled.union(other)
        assert set(result.to_list() if hasattr(result, "to_list")
                   else list(result)) == {1, 2, 3, 4, 5, 6, 7}

    def test_union_no_duplicates(self, filled: Set[int], other: Set[int]) -> None:
        result = filled.union(other)
        # 4 и 5 встречаются в обоих — в результате один раз
        assert len(result) == 7

    def test_union_with_empty(self, filled: Set[int], empty: Set[int]) -> None:
        assert filled.union(empty) == filled
        assert empty.union(filled) == filled

    def test_union_operator(self, filled: Set[int], other: Set[int]) -> None:
        assert (filled | other) == filled.union(other)

    def test_union_does_not_mutate(self, filled: Set[int], other: Set[int]) -> None:
        before_a = set(filled)
        before_b = set(other)
        filled.union(other)
        assert set(filled) == before_a
        assert set(other) == before_b


# ---------- intersect ----------

class TestIntersect:
    def test_intersect_basic(self, filled: Set[int], other: Set[int]) -> None:
        result = filled.intersect(other)
        assert set(result) == {4, 5}

    def test_intersect_disjoint(self, filled: Set[int], empty: Set[int]) -> None:
        assert len(filled.intersect(empty)) == 0

    def test_intersect_self(self, filled: Set[int]) -> None:
        assert filled.intersect(filled) == filled

    def test_intersect_operator(self, filled: Set[int], other: Set[int]) -> None:
        assert (filled & other) == filled.intersect(other)

    def test_intersect_does_not_mutate(self, filled: Set[int], other: Set[int]) -> None:
        before_a = set(filled)
        before_b = set(other)
        filled.intersect(other)
        assert set(filled) == before_a
        assert set(other) == before_b


# ---------- difference / symmetric_difference ----------

class TestDifference:
    def test_difference(self, filled: Set[int], other: Set[int]) -> None:
        result = filled.difference(other)
        assert set(result) == {1, 2, 3}

    def test_difference_operator(self, filled: Set[int], other: Set[int]) -> None:
        assert (filled - other) == filled.difference(other)

    def test_symmetric_difference(self, filled: Set[int], other: Set[int]) -> None:
        result = filled.symmetric_difference(other)
        assert set(result) == {1, 2, 3, 6, 7}

    def test_symmetric_difference_operator(self, filled: Set[int], other: Set[int]) -> None:
        assert (filled ^ other) == filled.symmetric_difference(other)


# ---------- __eq__ ----------

class TestEq:
    def test_eq_same(self) -> None:
        a: Set[int] = Set()
        b: Set[int] = Set()
        for x in [1, 2, 3]:
            a.add(x)
            b.add(x)
        assert a == b

    def test_eq_different(self, filled: Set[int], other: Set[int]) -> None:
        assert filled != other

    def test_eq_ignores_order(self) -> None:
        a: Set[int] = Set()
        b: Set[int] = Set()
        for x in [1, 2, 3]:
            a.add(x)
        for x in [3, 1, 2]:
            b.add(x)
        assert a == b

    def test_eq_with_non_set(self, filled: Set[int]) -> None:
        assert filled != {1, 2, 3, 4, 5}
        assert filled != 42
