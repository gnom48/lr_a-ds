import pytest

from src.prefix_tree import PrefixTree


# ---------- Фикстуры ----------

@pytest.fixture
def tree():
    return PrefixTree()


@pytest.fixture
def filled():
    """Небольшой набор для проверки автодополнения."""
    t = PrefixTree()
    for w in ["apple", "application", "apply", "banana", "band", "bandana"]:
        t.add(w)
    return t


# ---------- Базовые операции ----------

class TestBasic:
    def test_empty(self, tree):
        assert tree.contains("") is False
        assert tree.contains("anything") is False
        assert tree.starts_with("a") == []

    def test_add_and_contains(self, tree):
        tree.add("hello")
        assert tree.contains("hello") is True
        assert tree.contains("hell") is False   # префикс — не слово
        assert tree.contains("helloo") is False

    def test_add_duplicate_is_idempotent(self, tree):
        tree.add("cat")
        tree.add("cat")
        assert tree.contains("cat") is True
        assert tree.starts_with("cat") == ["cat"]


# ---------- Автодополнение ----------

class TestAutocomplete:
    def test_prefix_found(self, filled):
        assert sorted(filled.starts_with("app")) == [
            "apple", "application", "apply"
        ]

    def test_prefix_exact_word(self, filled):
        # слово целиком — тоже валидный результат
        assert "banana" in filled.starts_with("banana")

    def test_prefix_missing(self, filled):
        assert filled.starts_with("xyz") == []

    def test_prefix_is_part_of_many(self, filled):
        assert sorted(filled.starts_with("band")) == ["band", "bandana"]

    def test_empty_prefix_returns_all(self, filled):
        assert sorted(filled.starts_with("")) == sorted([
            "apple", "application", "apply", "banana", "band", "bandana"
        ])


# ---------- Совместные сценарии ----------

class TestScenarios:
    def test_add_after_query(self, tree):
        tree.add("apple")
        tree.add("apply")
        assert sorted(tree.starts_with("app")) == ["apple", "apply"]

        # добавляем новое слово — оно появляется в автодополнении
        tree.add("apricot")
        assert "apricot" in tree.starts_with("ap")

    def test_shared_prefix_words(self, tree):
        for w in ["car", "cart", "care", "careful"]:
            tree.add(w)
        assert sorted(tree.starts_with("car")) == [
            "car", "care", "careful", "cart"
        ]
        assert tree.contains("care") is True
        assert tree.contains("car") is True
