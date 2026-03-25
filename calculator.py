# Консольный калькулятор на Python
# Программа запрашивает два числа и оператор, вычисляет результат и обрабатывает ошибки

# Функция для сложения
def add(a, b):
    return a + b

# Функция для вычитания
def subtract(a, b):
    return a - b

# Функция для умножения
def multiply(a, b):
    return a * b

# Функция для деления
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

            # Запрашиваем оператор
            operator = input("Введите оператор (+, -, *, /): ")

            # Запрашиваем второе число
            num2 = float(input("Введите второе число: "))

            # Выполняем операцию в зависимости от оператора
            if operator == '+':
                result = add(num1, num2)
            elif operator == '-':
                result = subtract(num1, num2)
            elif operator == '*':
                result = multiply(num1, num2)
            elif operator == '/':
                result = divide(num1, num2)
            else:
                raise ValueError("Неверный оператор. Используйте +, -, *, /")

            # Выводим результат
            print(f"Результат: {result}")

        except ValueError as e:
            # Обрабатываем ошибки ввода чисел или неверного оператора
            print(f"Ошибка: {e}")
        except ZeroDivisionError as e:
            # Обрабатываем деление на ноль
            print(f"Ошибка: {e}")

        # Спрашиваем, хочет ли пользователь продолжить
        continue_calc = input("Хотите продолжить? (да/нет): ").lower()
        if continue_calc != 'да':
            print("Спасибо за использование калькулятора!")
            break

# Запуск программы
if __name__ == "__main__":
    main()