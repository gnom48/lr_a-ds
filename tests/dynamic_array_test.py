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


@pytest.fixture
def sorted_arr() -> DynamicArray[int]:
    arr: DynamicArray[int] = DynamicArray()
    for x in [1, 3, 5, 7, 9, 11, 13]:
        arr.append(x)
    return arr


# ---------- Конструктор ----------

class TestInit:
    def test_default(self) -> None:
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


# ---------- len / iter ----------

class TestLenIter:
    def test_len(self, filled: DynamicArray[int]) -> None:
        assert len(filled) == 5

    def test_iter_order(self, filled: DynamicArray[int]) -> None:
        assert list(filled) == [5, 3, 8, 1, 9]

    def test_iter_empty(self, empty: DynamicArray[int]) -> None:
        assert list(empty) == []


# ---------- getitem / setitem / delitem ----------

class TestIndexing:
    def test_get(self, filled: DynamicArray[int]) -> None:
        assert filled[0] == 5
        assert filled[4] == 9

    def test_set(self, filled: DynamicArray[int]) -> None:
        filled[2] = 100
        assert filled[2] == 100
        assert list(filled) == [5, 3, 100, 1, 9]

    def test_get_out_of_range(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            _ = filled[5]

    def test_get_non_int(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(TypeError):
            _ = filled["0"]

    def test_del(self, filled: DynamicArray[int]) -> None:
        del filled[2]
        assert list(filled) == [5, 3, 1, 9]
        assert len(filled) == 4

    def test_del_out_of_range(self, filled: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            del filled[99]

    def test_del_from_empty(self, empty: DynamicArray[int]) -> None:
        with pytest.raises(IndexError):
            del empty[0]


# ---------- Проверки вхождения ----------

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


class TestContainsBinarySearch:
    def test_found(self, sorted_arr: DynamicArray[int]) -> None:
        for x in [1, 3, 5, 7, 9, 11, 13]:
            assert sorted_arr.contains_binary_search(x) is True

    def test_not_found(self, sorted_arr: DynamicArray[int]) -> None:
        for x in [0, 2, 4, 6, 8, 10, 100]:
            assert sorted_arr.contains_binary_search(x) is False

    def test_empty(self, empty: DynamicArray[int]) -> None:
        assert empty.contains_binary_search(1) is False

    def test_single(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        arr.append(42)
        assert arr.contains_binary_search(42) is True
        assert arr.contains_binary_search(41) is False

    def test_uncomparable(self) -> None:
        class Uncomparable:
            pass

        arr: DynamicArray[Uncomparable] = DynamicArray()
        arr.append(Uncomparable())
        with pytest.raises(TypeError):
            arr.contains_binary_search(Uncomparable())


# ---------- sum / average ----------

class TestSumAverage:
    def test_sum(self, filled: DynamicArray[int]) -> None:
        assert filled.sum() == 26  # 5+3+8+1+9

    def test_sum_with_start(self, filled: DynamicArray[int]) -> None:
        assert filled.sum(100) == 126

    def test_sum_empty(self, empty: DynamicArray[int]) -> None:
        assert empty.sum() == 0

    def test_average(self, filled: DynamicArray[int]) -> None:
        assert filled.average() == 26 / 5

    def test_average_single(self) -> None:
        arr: DynamicArray[int] = DynamicArray()
        arr.append(42)
        assert arr.average() == 42.0

    def test_average_empty(self, empty: DynamicArray[int]) -> None:
        with pytest.raises(ValueError):
            empty.average()

    def test_sum_strings(self) -> None:
        arr: DynamicArray[str] = DynamicArray()
        for s in ["a", "b", "c"]:
            arr.append(s)
        with pytest.raises(TypeError):
            assert arr.sum("") == "abc"


# ---------- append ----------

class TestAppendResize:
    def test_append_grows(self, empty: DynamicArray[int]) -> None:
        for i in range(100):
            empty.append(i)
        assert len(empty) == 100
        assert empty.capacity >= 100
        assert list(empty) == list(range(100))

    def test_contains_after_resize(self) -> None:
        arr: DynamicArray[int] = DynamicArray(2)
        for i in range(50):
            arr.append(i)
        for i in range(50):
            assert i in arr
        assert 50 not in arr
