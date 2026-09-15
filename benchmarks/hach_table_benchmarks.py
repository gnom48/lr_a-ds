from src.hash_table import HashTable

import pytest


class TestBenchmarkContains:
    def test_benchmark_contains_miss(self, benchmark):
        ht = HashTable()
        for i in range(10_000):
            ht[f"key{i}"] = i

        def run():
            return "missing" in ht

        benchmark.pedantic(run, rounds=50, iterations=1_000)

    def test_benchmark_contains_direct_miss(self, benchmark):
        ht = HashTable()
        for i in range(10_000):
            ht[f"key{i}"] = i

        def run():
            return ht.contains_direct("missing")

        benchmark.pedantic(run, rounds=50, iterations=1_000)


class TestBenchmarkInsert:
    @pytest.mark.parametrize("n", [1_000, 10_000, 100_000])
    def test_benchmark_insert_scaling(self, benchmark, n):
        def run():
            ht = HashTable()
            for i in range(n):
                ht[f"key{i}"] = i
            return ht

        ht = benchmark(run)
        per_op_us = benchmark.stats["mean"] / n * 1e6
        print(f"\n  N = {n:>7}: {benchmark.stats['mean']:.4f} с  "
              f"({per_op_us:.3f} мкс/операция, capacity = {ht.capacity})")
