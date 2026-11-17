import random

import pytest

from src.graph import Graph


def make_chain(n: int) -> Graph:
    g = Graph(n)
    for i in range(n - 1):
        g.add_edge(i, i + 1)
    return g


class TestBenchmarkTraversal:
    @pytest.mark.parametrize("n", [100, 1_000, 5_000])
    def test_bench_bfs(self, benchmark, n: int) -> None:
        """BFS на цепочке из n вершин."""
        g = make_chain(n)
        benchmark(lambda: g.bfs(0))

    @pytest.mark.parametrize("n", [100, 1_000, 5_000])
    def test_bench_dfs(self, benchmark, n: int) -> None:
        """DFS на цепочке из n вершин."""
        g = make_chain(n)
        benchmark(lambda: g.dfs(0))


class TestBenchmarkBuild:
    @pytest.mark.parametrize("n", [100, 1_000])
    def test_bench_add_edges(self, benchmark, n: int) -> None:
        """Построение цепочки."""
        def run() -> None:
            g = Graph(n)
            for i in range(n - 1):
                g.add_edge(i, i + 1)
        benchmark(run)

    @pytest.mark.parametrize("n", [100, 1_000])
    def test_bench_add_random_edges(self, benchmark, n: int) -> None:
        """Случайные рёбра."""
        rnd = random.Random(1)
        pairs = [(rnd.randrange(n), rnd.randrange(n)) for _ in range(n)]

        def run() -> None:
            g = Graph(n)
            for u, v in pairs:
                if u != v:
                    g.add_edge(u, v)
        benchmark(run)


class TestBenchmarkIO:
    @pytest.mark.parametrize("n", [100, 500])
    def test_bench_save(self, benchmark, tmp_path, n: int) -> None:
        g = make_chain(n)
        path = tmp_path / f"g_{n}.json"
        benchmark(lambda: g.save_to_file(str(path)))

    @pytest.mark.parametrize("n", [100, 500])
    def test_bench_load(self, benchmark, tmp_path, n: int) -> None:
        g = make_chain(n)
        path = tmp_path / f"g_{n}.json"
        g.save_to_file(str(path))
        benchmark(lambda: Graph.load_from_file(str(path)))
