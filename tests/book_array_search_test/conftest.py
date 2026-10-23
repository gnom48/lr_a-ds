import pytest

from src.models.book import Book
from src.book_array import BookArray


@pytest.fixture
def filled(books: list[Book]) -> BookArray:
    return BookArray(books)


@pytest.fixture
def books() -> list[Book]:
    return [
        Book("Толстой",    "Эксмо",  1200, 1500.0, 101),
        Book("Достоевский", "АСТ",     800, 1200.0, 305),
        Book("Пушкин",     "Питер",   400,  700.0, 202),
        Book("Чехов",      "Эксмо",   300,  500.0, 909),
        Book("Булгаков",   "Азбука",  500, 1100.0, 404),
        Book("Гоголь",     "АСТ",     350,  650.0, 707),
        Book("Лермонтов",  "Питер",   250,  450.0, 505),
        Book("Тургенев",   "Азбука",  600,  900.0, 808),
        Book("Гончаров",   "Эксмо",   700, 1000.0, 606),
        Book("Салтыков",   "АСТ",     450,  800.0, 303),
    ]


@pytest.fixture
def empty() -> BookArray:
    return BookArray()
