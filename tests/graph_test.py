import pytest

from src.graph import Graph


# region Фикстуры

@pytest.fixture
def empty_graph() -> Graph:
    return Graph(5)


@pytest.fixture
def sample_graph() -> Graph:
    """Связный граф из 13 вершин."""
    g = Graph(13)
    edges = [
        (0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
        (3, 7), (4, 7), (5, 8), (6, 8), (7, 9), (8, 10),
        (9, 11), (10, 11), (11, 12), (9, 12),
    ]
    for u, v in edges:
        g.add_edge(u, v)
    return g


# region Рёбра

class TestEdges:
    def test_add_edge_symmetric(self, empty_graph):
        empty_graph.add_edge(0, 2)
        assert empty_graph.matrix[0][2] == 1
        assert empty_graph.matrix[2][0] == 1
        assert empty_graph.matrix[0][1] == 0

    def test_remove_edge(self, empty_graph):
        empty_graph.add_edge(1, 3)
        empty_graph.remove_edge(1, 3)
        assert empty_graph.matrix[1][3] == 0
        assert empty_graph.matrix[3][1] == 0

    def test_add_edge_out_of_range(self, empty_graph):
        with pytest.raises(IndexError):
            empty_graph.add_edge(0, 5)


# region Обходы

class TestTraversal:
    def test_bfs_order(self):
        g = Graph(4)
        for u, v in [(0, 1), (0, 2), (1, 3)]:
            g.add_edge(u, v)
        assert g.bfs(0) == [0, 1, 2, 3]

    def test_dfs_order(self):
        g = Graph(4)
        for u, v in [(0, 1), (0, 2), (1, 3)]:
            g.add_edge(u, v)
        assert g.dfs(0) == [0, 1, 3, 2]

    def test_both_visit_all_vertices(self, sample_graph):
        assert set(sample_graph.bfs(0)) == set(range(13))
        assert set(sample_graph.dfs(0)) == set(range(13))

    def test_disconnected(self):
        g = Graph(5)
        g.add_edge(0, 1)
        g.add_edge(3, 4)
        assert set(g.bfs(0)) == {0, 1}
        assert set(g.dfs(3)) == {3, 4}

    def test_out_of_range(self, empty_graph):
        with pytest.raises(IndexError):
            empty_graph.bfs(10)


# region Сохранение

class TestPersistence:
    def test_save_and_load(self, sample_graph, tmp_path):
        path = tmp_path / "graph.json"
        sample_graph.save_to_file(str(path))
        loaded = Graph.load_from_file(str(path))
        assert loaded.size == sample_graph.size
        assert loaded.matrix == sample_graph.matrix
        assert loaded.bfs(0) == sample_graph.bfs(0)
