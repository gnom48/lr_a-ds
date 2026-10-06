import sys
import msvcrt
import os


from src.prefix_tree import PrefixTree


def main2():
    """крутое с реальным автодополнением"""
    os.system('')

    storage = PrefixTree()
    for w in ["python", "prefix", "python prefix", "pypl", "arm", "axe"]:
        storage.add(w)

    GRAY = "\033[90m"
    RESET = "\033[0m"

    print("Начните вводить текст.")
    print("Используйте стрелки ВВЕРХ/ВНИЗ для выбора вариантов, а ENTER чтобы подтвердить.")
    print("Чтобы выйти - Esc.\n")

    user_input = ""
    suggestion_index = 0

    while True:
        suggestions: list[str] = storage.starts_with(
            user_input) if user_input != "" else []

        if suggestion_index >= len(suggestions):
            suggestion_index = 0

        current_suggestion = suggestions[suggestion_index] if suggestions else ""
        tail = current_suggestion[len(
            user_input):] if current_suggestion else ""

        # махинации с консолью
        # \r — возвращает курсор в начало строки
        # \033[K — очищает строку от курсора до конца (чтобы не оставалось старых букв)
        sys.stdout.write(f"\r> {user_input}{GRAY}{tail}{RESET}\033[K")

        # Сдвигает мигающий курсор назад на длину серого хвоста
        if tail:
            sys.stdout.write(f"\033[{len(tail)}D")
        sys.stdout.flush()

        ch = msvcrt.getch()

        # Обработка спецклавиш (Стрелки на Windows возвращают два байта: 0xE0 или 0x00, а затем код кнопки)
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            if suggestions:
                if ch2 == b'H':
                    suggestion_index = (
                        suggestion_index - 1) % len(suggestions)
                elif ch2 == b'P':
                    suggestion_index = (
                        suggestion_index + 1) % len(suggestions)
            continue

        # Нажатие Enter
        if ch == b'\r':
            if current_suggestion:
                user_input = current_suggestion  # Подставляем выбранный вариант целиком
            # Печатаем финальный результат на новой строке
            sys.stdout.write(f"\r> {user_input}\n")
            print(f"Выбрано: '{user_input}'\n")
            # Сбрасываем для нового ввода
            user_input = ""
            suggestion_index = 0
            continue

        # Нажатие Backspace (удаление символа)
        if ch == b'\x08':
            user_input = user_input[:-1]
            suggestion_index = 0  # Сбрасываем выбор при изменении корня
            continue

        # Нажатие Esc (выход)
        if ch == b'\x1b':
            print("\nВыход")
            break

        # Обычные символы (буквы, цифры, пробел)
        try:
            letter = ch.decode('utf-8')
            if letter.isprintable():
                user_input += letter
                suggestion_index = 0  # Сбрасываем выбор при вводе новой буквы
        except UnicodeDecodeError:
            pass


def main():
    """Тупое просто с вводом-выводом"""

    storage = PrefixTree()
    for w in ["python", "prefix", "python prefix", "pypl", "arm", "axe"]:
        storage.add(w)

    while True:
        prefix = input("\nВведите начало слова (или 'exit'): ").strip()
        if prefix.lower() == "exit":
            break
        if not prefix:
            continue

        suggestions = storage.starts_with(prefix)
        if suggestions:
            print("Варианты автодополнения:")
            for i, s in enumerate(suggestions, 1):
                print(f"  {i}. {s}")
            print("  0. None (ввести слово полностью)")

            choice = input("Выберите номер (Enter — None): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
                word = suggestions[int(choice) - 1]
                print(f"Выбрано: {word}")
                continue

        # None или нет вариантов — вводим полностью
        word = input("Введите слово полностью: ").strip()
        if word:
            storage.add(word)
            print(f"Слово '{word}' добавлено в дерево.")


if __name__ == "__main__":
    main()
