import pytest

from src.dynamic_array import DynamicArray


def make_array(n: int, capacity: int = 10) -> DynamicArray[int]:
    arr: DynamicArray[int] = DynamicArray(capacity)
    for i in range(n):
        arr.append(i)
    return arr


def make_sorted_array(n: int) -> DynamicArray[int]:
    arr: DynamicArray[int] = DynamicArray(n)
    for i in range(n):
        arr.append(i)
    return arr  # уже отсортирован, т.к. добавляли по возрастанию


# ---------- append ----------

class TestBenchmarkAppend:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_append(self, benchmark, n: int) -> None:
        """Амортизированное добавление в конец с ресайзами."""
        def run() -> None:
            arr: DynamicArray[int] = DynamicArray()
            for i in range(n):
                arr.append(i)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_append_preallocated(self, benchmark, n: int) -> None:
        """Append в массив с заранее большой ёмкостью — без ресайзов."""
        def run() -> None:
            arr: DynamicArray[int] = DynamicArray(n)
            for i in range(n):
                arr.append(i)
        benchmark(run)


class TestBenchmarkResize:
    def test_bench_growth_amortized(self, benchmark) -> None:
        """Рост с 10 до 100_000: амортизированная стоимость append с ресайзами."""
        def run() -> None:
            arr: DynamicArray[int] = DynamicArray(10)
            for i in range(100_000):
                arr.append(i)
        benchmark(run)


# ---------- Проверки вхождения ----------

class TestBenchmarkContainsLinear:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_contains_linear(self, benchmark, n: int) -> None:
        """Линейный поиск через `in` — O(n) на запрос."""
        arr = make_array(n)

        def run() -> None:
            for i in range(n):
                _ = i in arr
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_contains_linear_missing(self, benchmark, n: int) -> None:
        """Линейный поиск отсутствующего элемента — всегда O(n), без раннего выхода."""
        arr = make_array(n)

        def run() -> None:
            for i in range(n):
                _ = (n + i) in arr
        benchmark(run)


class TestBenchmarkContainsBinary:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_contains_binary(self, benchmark, n: int) -> None:
        """Бинарный поиск — O(log n) на запрос (массив отсортирован)."""
        arr = make_sorted_array(n)

        def run() -> None:
            for i in range(n):
                _ = arr.contains_binary_search(i)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_contains_binary_missing(self, benchmark, n: int) -> None:
        """Бинарный поиск отсутствующего элемента — O(log n)."""
        arr = make_sorted_array(n)

        def run() -> None:
            for i in range(n):
                _ = arr.contains_binary_search(n + i)
        benchmark(run)


# ---------- sum / average ----------

class TestBenchmarkSumAverage:
    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_sum(self, benchmark, n: int) -> None:
        """Сумма всех элементов — O(n)."""
        arr = make_array(n)

        def run() -> None:
            _ = arr.sum()
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000, 10_000])
    def test_bench_average(self, benchmark, n: int) -> None:
        """Среднее арифметическое — O(n)."""
        arr = make_array(n)

        def run() -> None:
            _ = arr.average()
        benchmark(run)
