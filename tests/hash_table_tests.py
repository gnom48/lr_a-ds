from src.hash_table import HashTable

import pytest


@pytest.fixture
def empty_ht():
    """Пустая хеш-таблица со стандартной ёмкостью."""
    return HashTable()


@pytest.fixture
def filled_ht():
    """Хеш-таблица с 20 парами key0..key19."""
    ht = HashTable()
    for i in range(20):
        ht[f"key{i}"] = i
    return ht


class TestBasicOperations:
    def test_empty_on_creation(self, empty_ht):
        assert len(empty_ht) == 0

    def test_set_and_get(self, empty_ht):
        empty_ht["a"] = 1
        empty_ht["b"] = 2
        empty_ht["c"] = 3

        assert empty_ht["a"] == 1
        assert empty_ht["b"] == 2
        assert empty_ht["c"] == 3
        assert len(empty_ht) == 3

    def test_get_missing_raises_keyerror(self, empty_ht):
        with pytest.raises(KeyError):
            _ = empty_ht["nope"]


class TestUpdate:
    def test_update_existing_key_overwrites(self, empty_ht):
        empty_ht["x"] = 10
        empty_ht["x"] = 20
        empty_ht["x"] = 30

        assert empty_ht["x"] == 30
        assert len(empty_ht) == 1

    @pytest.mark.parametrize("values", [
        [1, 2, 3],
        [100, -100, 0],
        ["a", "b", "c"],
    ])
    def test_update_with_various_types(self, empty_ht, values):
        for v in values:
            empty_ht["k"] = v
        assert empty_ht["k"] == values[-1]
        assert len(empty_ht) == 1


class TestDelete:
    def test_delete_existing(self, filled_ht):
        del filled_ht["key5"]
        assert len(filled_ht) == 19
        assert "key5" not in filled_ht
        assert filled_ht["key4"] == 4
        assert filled_ht["key6"] == 6

    def test_delete_missing_raises(self, empty_ht):
        with pytest.raises(KeyError):
            del empty_ht["nope"]

    def test_delete_twice_raises(self, empty_ht):
        empty_ht["a"] = 1
        del empty_ht["a"]
        with pytest.raises(KeyError):
            del empty_ht["a"]

    def test_get_after_delete_raises(self, empty_ht):
        empty_ht["a"] = 1
        del empty_ht["a"]
        with pytest.raises(KeyError):
            _ = empty_ht["a"]


class TestContains:
    def test_contains_both_variants_existing(self, filled_ht):
        for i in range(20):
            k = f"key{i}"
            assert k in filled_ht
            assert filled_ht.contains_direct(k)

    def test_contains_both_variants_missing(self, filled_ht):
        for i in range(20, 30):
            k = f"key{i}"
            assert k not in filled_ht
            assert not filled_ht.contains_direct(k)

    def test_contains_matches_getitem(self, filled_ht):
        """Инвариант: key in ht ⟺ ht[key] не бросает KeyError."""
        for i in range(30):
            k = f"key{i}"
            try:
                filled_ht[k]
                in_via_getitem = True
            except KeyError:
                in_via_getitem = False
            assert (k in filled_ht) == in_via_getitem
            assert filled_ht.contains_direct(k) == in_via_getitem


class TestRehashGrow:
    def test_grow_triggers_after_threshold(self):
        ht = HashTable(start_capacity=4)   # порог 4 * 0.75 = 3
        for i in range(4):
            ht[f"k{i}"] = i
        assert len(ht) == 4
        # capacity должна вырасти
        assert ht.capacity > 4, "rehash при расширении не сработал"

    def test_data_preserved_after_grow(self):
        ht = HashTable(start_capacity=4)
        for i in range(100):
            ht[f"k{i}"] = i
        for i in range(100):
            assert ht[f"k{i}"] == i

    def test_capacity_monotonic_growth(self):
        ht = HashTable(start_capacity=4)
        prev = ht.capacity
        for i in range(200):
            ht[f"k{i}"] = i
            assert ht.capacity >= prev, "capacity уменьшилась при вставке"
            prev = ht.capacity


class TestShrinkAndProtocols:
    def test_shrink_triggers_after_mass_delete(self):
        ht = HashTable(start_capacity=10)
        for i in range(100):
            ht[f"k{i}"] = i

        cap_before = ht.capacity
        for i in range(95):
            del ht[f"k{i}"]

        assert ht.capacity < cap_before, "сжатие не сработало"
        assert ht.capacity >= HashTable.START_CAPACITY
        assert len(ht) == 5

    def test_len_after_mixed_ops(self, empty_ht):
        for i in range(50):
            empty_ht[f"k{i}"] = i
        for i in range(0, 50, 2):
            del empty_ht[f"k{i}"]
        assert len(empty_ht) == 25


class TestEdgeCases:
    def test_start_capacity_zero_uses_default(self):
        ht = HashTable(start_capacity=0)
        assert ht.capacity == HashTable.START_CAPACITY

    def test_start_capacity_negative_uses_default(self):
        ht = HashTable(start_capacity=-5)
        assert ht.capacity == HashTable.START_CAPACITY

    def test_custom_start_capacity(self):
        ht = HashTable(start_capacity=32)
        assert ht.capacity == 32

    def test_collisions_handled(self):
        """Разные ключи с одинаковым хешем не должны теряться."""
        ht = HashTable(start_capacity=4)
        # Ключи 0, 4, 8, 12 при capacity=4 дают одинаковый индекс
        for i in (0, 4, 8, 12):
            ht[i] = i * 10
        for i in (0, 4, 8, 12):
            assert ht[i] == i * 10
        assert len(ht) == 4
