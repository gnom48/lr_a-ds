import pytest

from src.heap import Heap
from src.models.student import Student


def make_student(name: str = "Иванов И.И.",
                 group: str = "PZ-21",
                 course: int = 2,
                 age: int = 18,
                 grade: float = 4.0) -> Student:
    return Student(name, group, course, age, grade)


class TestBenchmarkPush:
    @pytest.mark.parametrize("n", [1_000, 10_000, 100_000])
    def test_benchmark_push_scaling(self, benchmark, n):
        students = [make_student(name=f"S{i}", grade=(i % 100) / 100 + 3.0)
                    for i in range(n)]

        def run():
            h = Heap()
            for s in students:
                h.push(s)
            return h

        h = benchmark(run)
        per_op_us = benchmark.stats["mean"] / n * 1e6
        print(f"\n  N = {n:>7}: {benchmark.stats['mean']:.4f} с  "
              f"({per_op_us:.3f} мкс/операция, size = {len(h)})")


class TestBenchmarkContainsKey:
    def test_benchmark_contains_by_key_miss(self, benchmark):
        h = Heap()
        for i in range(10_000):
            h.push(make_student(name=f"S{i}", grade=3.0 + (i % 200) / 100))

        def run():
            return h.contains_by_key(99.99)

        benchmark.pedantic(run, rounds=50, iterations=1_000)
