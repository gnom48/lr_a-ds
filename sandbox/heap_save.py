from src.heap import Heap
from src.models.student import make_student


def main() -> None:
    students = [
        make_student(name=f"Студент{i}", grade=3.0 + i * 0.1)
        for i in range(10)
    ]

    path = "sandbox\\students.json"
    heap = Heap()
    heap.build(students)
    heap.save(path)

    print("Сохранили")
    while not heap.is_empty():
        print(heap.pop())

    restored = Heap()
    restored.load(path)

    print("\nВосстановили")
    while not restored.is_empty():
        print(restored.pop())


if __name__ == "__main__":
    main()
