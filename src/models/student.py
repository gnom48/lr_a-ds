from dataclasses import dataclass, asdict


@dataclass
class Student:
    full_name: str
    group_number: str
    course: int
    age: int
    average_grade: float

    def __str__(self):
        return (f"{self.full_name} | гр. {self.group_number} | "
                f"{self.course} курс | {self.age} лет | ср.балл {self.average_grade:.2f}")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Student":
        return cls(**d)

    def __lt__(self, other: "Student") -> bool:
        return self.average_grade < other.average_grade

    def __gr__(self, other: "Student") -> bool:
        return self.average_grade > other.average_grade

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return (self.full_name == other.full_name
                and self.group_number == other.group_number
                and self.course == other.course
                and self.age == other.age
                and abs(self.average_grade - other.average_grade) < 1e-9)


def make_student(name: str = "Иванов И.И.",
                 group: str = "4517",
                 course: int = 2,
                 age: int = 21,
                 grade: float = 4.0) -> Student:
    return Student(name, group, course, age, grade)
