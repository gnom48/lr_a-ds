import pytest

from src.dynamic_array import DynamicArray


# ---------- Фикстуры ----------

@pytest.fixture
def empty() -> DynamicArray[int]:
    return DynamicArray()


@pytest.fixture
def filled() -> DynamicArray[int]:
    arr: DynamicArray[int] = DynamicArray()
    for x in [5, 3, 8, 1, 9]:
        arr.append(x)
    return arr


# ---------- Конструктор ----------

class TestInit:
    def test_default_capacity(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        assert len(arr) == 0
        assert arr.capacity == 10

    def test_custom_capacity(self) -> None:
        arr: DynamicArray[int] = DynamicArray(100)
        assert len(arr) == 0
        assert arr.capacity == 100

    @pytest.mark.parametrize("bad", [0, -1, -100])
    def test_invalid_capacity(self, bad: int) -> None:
        with pytest.raises(ValueError):
            DynamicArray(bad)

    def test_generic_instantiation(self) -> None:
        ints: DynamicArray[int] = DynamicArray()
        strs: DynamicArray[str] = DynamicArray()
        assert len(ints) == 0
        assert len(strs) == 0


# ---------- __len__ / __iter__ ----------

class TestLenIter:
    def test_len_empty(self, empty: DynamicArray[int]) -> None:
        assert len(empty) == 0

    def test_len_after_appends(self, empty: DynamicArray[int]) -> None:
        for i in range(7):
            empty.append(i)
        assert len(empty) == 7

    def test_iter_empty(self, empty: DynamicArray[int]) -> None:
        assert list(empty) == []

    def test_iter_order(self, filled: DynamicArray[int]) -> None:
        assert list(filled) == [5, 3, 8, 1, 9]

    def test_iter_reflects_changes(self, filled: DynamicArray[int]) -> None:
        filled.append(42)
        assert list(filled)[-1] == 42


# ---------- __getitem__ / __setitem__ ----------

class TestGetSetItem:
    def test_get_by_index(self, filled: DynamicArray[int]) -> None:
        assert filled[0] == 5
        assert filled[4] == 9

    def test_get_out_of_range(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            _ = filled[5]
        with pytest.raises(IndexError):
            _ = filled[-1]  # отрицательные не поддерживаются

    def test_get_from_empty(self, empty: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            _ = empty[0]

    def test_get_non_int_index(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(TypeError):
            _ = filled["0"]  # type: ignore[index]

    def test_set_by_index(self, filled: DynamicArray[int]) -> None:
        filled[2] = 100
        assert filled[2] == 100
        assert list(filled) == [5, 3, 100, 1, 9]

    def test_set_out_of_range(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            filled[10] = 1


# ---------- __delitem__ ----------

class TestDelItem:
    def test_delete_middle(self, filled: DynamicArray[int]) -> None:
        del filled[2]
        assert list(filled) == [5, 3, 1, 9]
        assert len(filled) == 4

    def test_delete_first(self, filled: DynamicArray[int]) -> None:
        del filled[0]
        assert list(filled) == [3, 8, 1, 9]

    def test_delete_last(self, filled: DynamicArray[int]) -> None:
        del filled[4]
        assert list(filled) == [5, 3, 8, 1]

    def test_delete_out_of_range(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            del filled[99]

    def test_delete_from_empty(self, empty: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            del empty[0]

    def test_delete_shrinks_capacity(self) -> None:
        arr: DynamicArray[int] = DynamicArray(16)
        for i in range(16):
            arr.append(i)
        # 16 элементов → capacity 16 (ровно)
        # удалим до 4 → должно сработать сжатие
        for _ in range(12):
            arr.pop()
        assert len(arr) == 4
        assert arr.capacity < 16


# ---------- __contains__ (линейный поиск) ----------

class TestContainsLinear:
    def test_present(self, filled: DynamicArray[int]) -> None:
        assert 5 in filled
        assert 9 in filled
        assert 1 in filled

    def test_absent(self, filled: DynamicArray[int]) -> None:
        assert 100 not in filled
        assert 0 not in filled

    def test_empty(self, empty: DynamicArray[int]) -> None:
        assert 1 not in empty

    def test_duplicates(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        arr.append(7)
        arr.append(7)
        assert 7 in arr


# ---------- contains_binary_search ----------

class TestBinarySearch:
    def test_found(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        for x in [1, 3, 5, 7, 9, 11, 13]:
            arr.append(x)
        for x in [1, 3, 5, 7, 9, 11, 13]:
            assert arr.contains_binary_search(x) is True

    def test_not_found(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        for x in [1, 3, 5, 7, 9]:
            arr.append(x)
        for x in [0, 2, 4, 6, 10]:
            assert arr.contains_binary_search(x) is False

    def test_empty(self, empty: DynamicArray[int]) -> None:
        assert empty.contains_binary_search(1) is False

    def test_single_element(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        arr.append(42)
        assert arr.contains_binary_search(42) is True
        assert arr.contains_binary_search(41) is False

    def test_requires_comparable(self) -> None:
        class Uncomparable:
            pass

        arr: DynamicArray[Uncomparable] = DynamicArray()
        arr.append(Uncomparable())
        with pytest.raises(TypeError):
            arr.contains_binary_search(Uncomparable())


# ---------- append / insert ----------

class TestAppendInsert:
    def test_append_grows(self, empty: DynamicArray[int]) -> None:
        for i in range(100):
            empty.append(i)
        assert len(empty) == 100
        assert empty.capacity >= 100
        assert list(empty) == list(range(100))

    def test_insert_at_start(self, filled: DynamicArray[int]) -> None:
        filled.insert(0, 100)
        assert list(filled) == [100, 5, 3, 8, 1, 9]

    def test_insert_at_end(self, filled: DynamicArray[int]) -> None:
        filled.insert(len(filled), 100)
        assert list(filled) == [5, 3, 8, 1, 9, 100]

    def test_insert_middle(self, filled: DynamicArray[int]) -> None:
        filled.insert(2, 100)
        assert list(filled) == [5, 3, 100, 8, 1, 9]

    def test_insert_negative_index(self, filled: DynamicArray[int]) -> None:
        filled.insert(-1, 100)
        # -1 → size + (-1) = 4
        assert list(filled) == [5, 3, 8, 1, 100, 9]

    def test_insert_beyond_end_clamps(self, filled: DynamicArray[int]) -> None:
        filled.insert(999, 100)
        assert list(filled)[-1] == 100
        assert len(filled) == 6

    def test_insert_into_empty(self, empty: DynamicArray[int]) -> None:
        empty.insert(0, 42)
        assert list(empty) == [42]


# ---------- pop ----------

class TestPop:
    def test_pop_last_default(self, filled: DynamicArray[int]) -> None:
        assert filled.pop() == 9
        assert list(filled) == [5, 3, 8, 1]

    def test_pop_index(self, filled: DynamicArray[int]) -> None:
        assert filled.pop(0) == 5
        assert list(filled) == [3, 8, 1, 9]

    def test_pop_negative(self, filled: DynamicArray[int]) -> None:
        assert filled.pop(-1) == 9
        assert list(filled) == [5, 3, 8, 1]

    def test_pop_empty(self, empty: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            empty.pop()

    def test_pop_out_of_range(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            filled.pop(99)


# ---------- reverse ----------

class TestReverse:
    def test_reverse_odd(self, filled: DynamicArray[int]) -> None:
        filled.reverse()
        assert list(filled) == [9, 1, 8, 3, 5]

    def test_reverse_even(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        for x in [1, 2, 3, 4]:
            arr.append(x)
        arr.reverse()
        assert list(arr) == [4, 3, 2, 1]

    def test_reverse_single(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        arr.append(1)
        arr.reverse()
        assert list(arr) == [1]

    def test_reverse_empty(self, empty: DynamicArray[int]) -> None:
        empty.reverse()
        assert list(empty) == []

    def test_reverse_twice_is_identity(self, filled: DynamicArray[int]) -> None:
        original = list(filled)
        filled.reverse()
        filled.reverse()
        assert list(filled) == original


# ---------- index / count ----------

class TestIndexCount:
    def test_index_found(self, filled: DynamicArray[int]) -> None:
        assert filled.index(5) == 0
        assert filled.index(8) == 2

    def test_index_not_found(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(ValueError):
            filled.index(100)

    def test_index_with_start(self, filled: DynamicArray[int]) -> None:
        assert filled.index(3, 1) == 1

    def test_index_with_start_stop(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(ValueError):
            filled.index(5, 1, 5)

    def test_count(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        for x in [1, 2, 1, 3, 1]:
            arr.append(x)
        assert arr.count(1) == 3
        assert arr.count(2) == 1
        assert arr.count(100) == 0


# ---------- sort ----------

class TestSort:
    def test_sort_ascending(self, filled: DynamicArray[int]) -> None:
        filled.sort()
        assert list(filled) == [1, 3, 5, 8, 9]

    def test_sort_descending(self, filled: DynamicArray[int]) -> None:
        filled.sort(reverse=True)
        assert list(filled) == [9, 8, 5, 3, 1]

    def test_sort_with_key(self) -> None:
        arr: DynamicArray[str] = DynamicArray()
        for s in ["bbb", "a", "cc"]:
            arr.append(s)
        arr.sort(key=len)
        assert list(arr) == ["a", "cc", "bbb"]

    def test_sort_empty(self, empty: DynamicArray[int]) -> None:
        empty.sort()
        assert list(empty) == []


# ---------- clear ----------

class TestClear:
    def test_clear(self, filled: DynamicArray[int]) -> None:
        filled.clear()
        assert len(filled) == 0
        assert list(filled) == []

    def test_clear_keeps_capacity(self, filled: DynamicArray[int]) -> None:
        cap_before = filled.capacity
        filled.clear()
        assert filled.capacity == cap_before

    def test_clear_empty(self, empty: DynamicArray[int]) -> None:
        empty.clear()
        assert len(empty) == 0


# ---------- repr / str / eq ----------

class TestDunder:
    def test_repr(self, filled: DynamicArray[int]) -> None:
        assert repr(filled) == "DynamicArray([5, 3, 8, 1, 9])"

    def test_str(self, filled: DynamicArray[int]) -> None:
        assert str(filled) == repr(filled)

    def test_repr_empty(self, empty: DynamicArray[int]) -> None:
        assert repr(empty) == "DynamicArray([])"

    def test_eq_same(self) -> None:
        a: DynamicArray[int] = DynamicArray()
        b: DynamicArray[int] = DynamicArray()
        for x in [1, 2, 3]:
            a.append(x)
            b.append(x)
        assert a == b

    def test_eq_different(self) -> None:
        a: DynamicArray[int] = DynamicArray()
        b: DynamicArray[int] = DynamicArray()
        a.append(1)
        b.append(2)
        assert a != b

    def test_eq_different_sizes(self) -> None:
        a: DynamicArray[int] = DynamicArray()
        b: DynamicArray[int] = DynamicArray()
        a.append(1)
        assert a != b

    def test_eq_with_non_array(self, filled: DynamicArray[int]) -> None:
        assert filled != [5, 3, 8, 1, 9]
        assert filled != 42


# ---------- MutableSequence-совместимость ----------

class TestMutableSequenceProtocol:
    def test_isinstance(self, filled: DynamicArray[int]) -> None:
        from collections.abc import MutableSequence
        assert isinstance(filled, MutableSequence)

    def test_extend_from_sequence(self, empty: DynamicArray[int]) -> None:
        empty.extend([1, 2, 3])
        assert list(empty) == [1, 2, 3]

    def test_index_method_from_mixin(self, filled: DynamicArray[int]) -> None:
        # у нас свой index, но проверим что работает
        assert filled.index(8) == 2

    def test_remove_from_mixin(self, filled: DynamicArray[int]) -> None:
        filled.remove(8)
        assert list(filled) == [5, 3, 1, 9]

    def test_iadd(self, empty: DynamicArray[int]) -> None:
        empty += [1, 2, 3]
        assert list(empty) == [1, 2, 3]


# ---------- Стресс / интеграция ----------

class TestStress:
    def test_many_appends_and_pops(self) -> None:
        arr: DynamicArray[int] = DynamicArray(2)
        for i in range(1000):
            arr.append(i)
        assert len(arr) == 1000
        for i in range(1000):
            assert arr.pop() == 999 - i
        assert len(arr) == 0

    def test_alternating_append_pop(self) -> None:
        arr: DynamicArray[int] = DynamicArray(4)
        for i in range(100):
            arr.append(i)
            arr.append(i + 1)
            arr.pop()
        # после 100 итераций: 100 элементов (по одному добавляется)
        assert len(arr) == 100

    def test_contains_after_resize(self) -> None:
        arr: DynamicArray[int] = DynamicArray(2)
        for i in range(50):
            arr.append(i)
        for i in range(50):
            assert i in arr
        for i in range(50, 100):
            assert i not in arr

    def test_mixed_operations(self) -> None:
        arr: DynamicArray[int] = DynamicArray(3)
        arr.extend([1, 2, 3, 4, 5])
        arr.insert(0, 0)
        arr.reverse()
        arr.pop()
        arr.sort()
        assert list(arr) == [1, 2, 3, 4, 5]
