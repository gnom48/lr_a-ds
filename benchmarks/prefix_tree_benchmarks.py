import pytest

from src.prefix_tree import PrefixTree


class TestBenchmarkAdd:
    @pytest.mark.parametrize("n", [1_000, 10_000, 100_000])
    def test_benchmark_add_scaling(self, benchmark, n):
        words = [f"word{i:07d}" for i in range(n)]

        def run():
            t = PrefixTree()
            for w in words:
                t.add(w)
            return t

        t = benchmark(run)
        per_op_us = benchmark.stats["mean"] / n * 1e6
        print(f"\n  N = {n:>7}: {benchmark.stats['mean']:.4f} с  "
              f"({per_op_us:.3f} мкс/операция, contains last = "
              f"{t.contains(words[-1])})")


class TestBenchmarkAutocomplete:
    def test_benchmark_starts_with(self, benchmark):
        t = PrefixTree()
        for i in range(10_000):
            t.add(f"prefix{i:05d}")

        def run():
            return t.starts_with("prefix")

        result = benchmark.pedantic(run, rounds=20, iterations=100)
        print(f"\n  найдено вариантов: {len(result)}")
