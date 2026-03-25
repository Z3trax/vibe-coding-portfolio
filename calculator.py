# Функция для сложения двух чисел
def add(a, b):
    return a + b

# Функция для вычитания двух чисел
def subtract(a, b):
    return a - b

# Функция для умножения двух чисел
def multiply(a, b):
    return a * b

# Функция для деления двух чисел с проверкой на деление на ноль
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Деление на ноль невозможно")
    return a / b

# Основная функция программы
def main():
    print("Добро пожаловать в консольный калькулятор!")
    while True:
        try:
            # Запрашиваем первое число
            num1 = float(input("Введите первое число: "))
        except ValueError:
            print("Ошибка: Введите корректное число.")
            continue

        # Запрашиваем оператор
        operator = input("Введите оператор (+, -, *, /): ").strip()
        if operator not in ['+', '-', '*', '/']:
            print("Ошибка: Неверный оператор. Используйте +, -, *, /.")
            continue

        try:
            # Запрашиваем второе число
            num2 = float(input("Введите второе число: "))
        except ValueError:
            print("Ошибка: Введите корректное число.")
            continue

        try:
            # Выполняем операцию
            if operator == '+':
                result = add(num1, num2)
            elif operator == '-':
                result = subtract(num1, num2)
            elif operator == '*':
                result = multiply(num1, num2)
            elif operator == '/':
                result = divide(num1, num2)

            # Выводим результат
            print(f"Результат: {result}")
        except ZeroDivisionError as e:
            print(f"Ошибка: {e}")
            continue

        # Спрашиваем, хочет ли пользователь продолжить
        continue_calc = input("Хотите продолжить? (да/нет): ").strip().lower()
        if continue_calc != 'да':
            print("Спасибо за использование калькулятора!")
            break

# Запуск программы
if __name__ == "__main__":
    main()
