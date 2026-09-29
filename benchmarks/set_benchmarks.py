import pytest

from src.set import Set


def make_set(n: int, start: int = 0) -> Set[int]:
    s: Set[int] = Set()
    for i in range(start, start + n):
        s.add(i)
    return s


class TestBenchmarkAdd:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_add_unique(self, benchmark, n: int) -> None:
        """add уникальных значений — O(n^2) суммарно из-за линейного поиска."""
        def run() -> None:
            s: Set[int] = Set()
            for i in range(n):
                s.add(i)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_add_duplicate(self, benchmark, n: int) -> None:
        """add дубликатов — каждый раз линейный поиск до конца, O(n) на операцию."""
        s = make_set(n)

        def run() -> None:
            for i in range(n):
                s.add(0)  # 0 уже есть в начале
        benchmark(run)


class TestBenchmarkContains:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_contains_linear(self, benchmark, n: int) -> None:
        """Линейный поиск (in) — O(n) на запрос."""
        s = make_set(n)

        def run() -> None:
            for i in range(n):
                _ = i in s
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_contains_binary(self, benchmark, n: int) -> None:
        """Бинарный поиск — O(log n) на запрос, но требует отсортированности."""
        s = make_set(n)
        s._data.sort()
        s._sorted = True

        def run() -> None:
            for i in range(n):
                _ = s.contains_binary_search(i)
        benchmark(run)


class TestBenchmarkRemove:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_remove_first(self, benchmark, n: int) -> None:
        """remove первого элемента — линейный поиск + сдвиг."""
        def run() -> None:
            local = make_set(n)
            local.remove(0)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_remove_last(self, benchmark, n: int) -> None:
        """remove последнего элемента — линейный поиск до конца без сдвига."""
        def run() -> None:
            local = make_set(n)
            local.remove(n - 1)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_pop(self, benchmark, n: int) -> None:
        """pop — O(1), удаляет с конца."""
        def run() -> None:
            local = make_set(n)
            local.pop()
        benchmark(run)


class TestBenchmarkUnion:
    @pytest.mark.parametrize("n", [100, 500, 1_000])
    def test_bench_union(self, benchmark, n: int) -> None:
        """union двух множеств размера n — O((2n)^2) из-за add."""
        a = make_set(n, start=0)
        b = make_set(n, start=n // 2)  # половина пересекается

        def run() -> None:
            _ = a.union(b)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 500, 1_000])
    def test_bench_union_disjoint(self, benchmark, n: int) -> None:
        """union непересекающихся — те же O((2n)^2), но add всегда добавляет."""
        a = make_set(n, start=0)
        b = make_set(n, start=n)

        def run() -> None:
            _ = a.union(b)
        benchmark(run)


class TestBenchmarkIntersect:
    @pytest.mark.parametrize("n", [100, 500, 1_000])
    def test_bench_intersect_half(self, benchmark, n: int) -> None:
        """intersect при пересечении в половину — O(n^2)."""
        a = make_set(n, start=0)
        b = make_set(n, start=n // 2)

        def run() -> None:
            _ = a.intersect(b)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 500, 1_000])
    def test_bench_intersect_empty(self, benchmark, n: int) -> None:
        """intersect непересекающихся — итерируемся по меньшему, ищем в большем."""
        a = make_set(n, start=0)
        b = make_set(n, start=n)

        def run() -> None:
            _ = a.intersect(b)
        benchmark(run)
