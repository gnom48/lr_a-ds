import pytest

from src.dynamic_array import DynamicArray
# from dynamic_array.true_dynamic_array import DynamicArray

"""
Как показывают бенчмарки: list реализация в разы быстрее ctype.Array реализации - факт!
"""


def make_array(n: int, capacity: int = 10) -> DynamicArray[int]:
    arr: DynamicArray[int] = DynamicArray(capacity)
    for i in range(n):
        arr.append(i)
    return arr


class TestBenchmarkAppend:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_append(self, benchmark, n: int) -> None:
        """Амортизированное добавление в конец."""
        benchmark(lambda: [DynamicArray().append(i) for i in range(n)])

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_append_preallocated(self, benchmark, n: int) -> None:
        """Append в массив с заранее большой ёмкостью — без ресайзов."""
        def run() -> None:
            arr: DynamicArray[int] = DynamicArray(n)
            for i in range(n):
                arr.append(i)
        benchmark(run)


class TestBenchmarkInsert:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_insert_at_start(self, benchmark, n: int) -> None:
        """Вставка в начало — O(n) на каждый insert → O(n²) суммарно."""
        def run() -> None:
            arr: DynamicArray[int] = DynamicArray(n + 1)
            for i in range(n):
                arr.insert(0, i)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_insert_at_end(self, benchmark, n: int) -> None:
        """Вставка в конец через insert — фактически append."""
        def run() -> None:
            arr: DynamicArray[int] = DynamicArray(n)
            for i in range(n):
                arr.insert(len(arr), i)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_insert_middle(self, benchmark, n: int) -> None:
        """Вставка в середину."""
        def run() -> None:
            arr: DynamicArray[int] = DynamicArray(n + 1)
            for i in range(n):
                arr.insert(len(arr) // 2, i)
        benchmark(run)


class TestBenchmarkPop:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_pop_from_end(self, benchmark, n: int) -> None:
        """Удаление с конца — O(1)."""
        def run() -> None:
            arr = make_array(n)
            for _ in range(n):
                arr.pop()
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_pop_from_start(self, benchmark, n: int) -> None:
        """Удаление из начала — O(n) каждый раз."""
        def run() -> None:
            arr = make_array(n)
            for _ in range(n):
                arr.pop(0)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_delitem_middle(self, benchmark, n: int) -> None:
        """Удаление из середины через del."""
        def run() -> None:
            arr = make_array(n)
            for _ in range(n):
                del arr[len(arr) // 2]
        benchmark(run)


class TestBenchmarkResize:
    def test_bench_growth_amortized(benchmark) -> None:
        """Рост с 10 до 100_000: сколько ресайзов и время."""
        def run() -> None:
            arr: DynamicArray[int] = DynamicArray(10)
            for i in range(100_000):
                arr.append(i)
        benchmark(run)

    def test_bench_shrink_amortized(benchmark) -> None:
        """Сжатие: удаление 90_000 элементов pop'ом с конца."""
        arr = make_array(100_000, capacity=100_000)

        def run() -> None:
            # копируем, чтобы не мутировать между запусками
            local = make_array(100_000, capacity=100_000)
            for _ in range(90_000):
                local.pop()
        benchmark(run)
