from src.graph import Graph


def main() -> None:
    g = Graph(13)
    edges = [
        (0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
        (3, 7), (4, 7), (5, 8), (6, 8), (7, 9), (8, 10),
        (9, 11), (10, 11), (11, 12), (9, 12),
    ]
    for u, v in edges:
        g.add_edge(u, v)

    print("Исходный граф:")
    g.print()

    path = "sandbox\\graph.json"
    g.save_to_file(path)
    print(f"\nСохранили в {path}")

    restored = Graph.load_from_file(path)
    print("\nВосстановленный граф:")
    restored.print()

    print("\nBFS от вершины 0:", restored.bfs(0))
    print("DFS от вершины 0:", restored.dfs(0))


if __name__ == "__main__":
    main()
