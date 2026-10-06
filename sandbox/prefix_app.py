import sys
import msvcrt
import os


from src.prefix_tree import PrefixTree

storage = PrefixTree()
storage.add("python")
storage.add("prefix")
storage.add("python prefix")
storage.add("pypl")
storage.add("arm")
storage.add("axe")

GRAY = "\033[90m"
RESET = "\033[0m"


def main():
    os.system('')

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


if __name__ == "__main__":
    main()
