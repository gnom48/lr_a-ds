import json


class Graph:
    """Неориентированный граф на основе матрицы смежности."""

    def __init__(self, size: int = 0):
        self.size = size
        self.matrix = [[0] * size for _ in range(size)]

    def add_edge(self, u: int, v: int):
        """Добавить ребро между вершинами u и v."""
        if not (0 <= u < self.size and 0 <= v < self.size):
            raise IndexError(f"Вершина вне диапазона: {u}, {v}")
        self.matrix[u][v] = 1
        self.matrix[v][u] = 1

    def remove_edge(self, u: int, v: int):
        if not (0 <= u < self.size and 0 <= v < self.size):
            raise IndexError(f"Вершина вне диапазона: {u}, {v}")
        self.matrix[u][v] = 0
        self.matrix[v][u] = 0

    def print(self):
        """Вывод текущего представления графа в терминал."""
        print(f"Graph ({self.size} vertices)")
        header = "    " + " ".join(f"{i:2d}" for i in range(self.size))
        print(header)
        for i, row in enumerate(self.matrix):
            print(f"{i:2d}  " + " ".join(f"{x:2d}" for x in row))

    def bfs(self, start: int) -> list[int]:
        """Поиск в ширину. Возвращает порядок обхода."""
        if not (0 <= start < self.size):
            raise IndexError(f"Вершина вне диапазона: {start}")
        visited = [False] * self.size
        order = []
        queue = [start]
        visited[start] = True
        while queue:
            v = queue.pop(0)
            order.append(v)
            for u in range(self.size):
                if self.matrix[v][u] and not visited[u]:
                    visited[u] = True
                    queue.append(u)
        return order

    def dfs(self, start: int) -> list[int]:
        """Поиск в глубину. Возвращает порядок обхода."""
        if not (0 <= start < self.size):
            raise IndexError(f"Вершина вне диапазона: {start}")
        visited = [False] * self.size
        order = []
        # итеративный вариант, чтобы не упасть на больших графах
        stack = [start]
        while stack:
            v = stack.pop()
            if visited[v]:
                continue
            visited[v] = True
            order.append(v)
            for u in range(self.size - 1, -1, -1):
                if self.matrix[v][u] and not visited[u]:
                    stack.append(u)
        return order

    def save_to_file(self, path: str):
        """Сохранить текущее представление графа в JSON-файл."""
        data = {"size": self.size, "matrix": self.matrix}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    @classmethod
    def load_from_file(cls, path: str) -> "Graph":
        """Загрузить граф из JSON-файла."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        graph = cls(data["size"])
        graph.matrix = data["matrix"]
        return graph
