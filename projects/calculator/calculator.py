# Консольный калькулятор на Python
# Программа запрашивает математическое выражение и вычисляет результат

import math  # Импорт модуля math для констант pi и e
import sympy as sp  # Импорт sympy для решения уравнений
import cmath  # Импорт cmath для комплексных чисел

# Функция для проверки допустимости выражения
# Разрешены только цифры, операторы + - * / ^ ( ) пробелы и константы pi, e, i
def is_valid_expression(expression):
    allowed_chars = set('0123456789+-*/^() .piei')  # Добавляем точку для float, p,i,e,i для pi, e, i
    for char in expression:
        if char not in allowed_chars:
            return False
    return True

# Функция для подготовки выражения к eval
# Заменяем ^ на **
def prepare_expression(expression):
    # Заменяем ^ на **
    expression = expression.replace('^', '**')
    return expression

# Функция для вычисления выражения
def calculate_expression(expression):
    try:
        # Проверяем на пустой ввод
        if not expression.strip():
            raise ValueError("Вы ввели пустое выражение")

        # Проверяем на допустимые символы
        if not is_valid_expression(expression):
            raise ValueError("Выражение содержит недопустимые символы. Разрешены только цифры, +, -, *, /, ^, (, ), пробелы и константы pi, e, i")

        # Подготавливаем выражение
        prepared_expr = prepare_expression(expression)

        # Вычисляем с помощью eval, предоставляя константы pi, e, i
        result = eval(prepared_expr, {"__builtins__": {}, "pi": math.pi, "e": math.e, "i": 1j})

        return result
    except ZeroDivisionError:
        raise ValueError("Деление на ноль")
    except SyntaxError:
        raise ValueError("Некорректный синтаксис выражения")
    except NameError:
        raise ValueError("Неизвестная переменная или константа")
    except Exception as e:
        raise ValueError(f"Ошибка в вычислении: {str(e)}")

# Функция для решения квадратного уравнения
def solve_quadratic(a, b, c):
    if a == 0:
        raise ValueError("Это не квадратное уравнение (a не может быть 0)")
    
    d = b**2 - 4*a*c
    x1 = (-b + cmath.sqrt(d)) / (2*a)
    x2 = (-b - cmath.sqrt(d)) / (2*a)
    return x1, x2
def solve_equation(eq):
    # Найти все латинские строчные буквы как переменные
    variables = set()
    for char in eq:
        if char.isalpha() and char.islower() and char.isascii():
            variables.add(char)
    
    if not variables:
        raise ValueError("В уравнении нет переменных")
    
    # Создать символы
    sym_vars = sp.symbols(list(variables))
    var_dict = dict(zip(variables, sym_vars))
    var_dict.update({'pi': sp.pi, 'e': sp.E, 'i': sp.I})  # Добавить константы
    
    # Заменить ^ на **
    eq = eq.replace('^', '**')
    
    # Разделить по =
    if '=' not in eq:
        raise ValueError("Уравнение должно содержать '='")
    left, right = eq.split('=', 1)
    
    try:
        # Создать уравнение
        equation = sp.Eq(sp.sympify(left, locals=var_dict), sp.sympify(right, locals=var_dict))
        # Решить относительно всех переменных
        solutions = sp.solve(equation, sym_vars)
        return solutions
    except Exception as e:
        raise ValueError(f"Ошибка в решении уравнения: {e}")

# Основная функция программы
def main():
    print("Добро пожаловать в консольный калькулятор!")
    print("Выберите режим:")
    print("1 - Вычислить математическое выражение")
    print("2 - Решить уравнение")
    print("3 - Решить квадратное уравнение")
    print("Поддерживаемые операции: +, -, *, /, ^ (возведение в степень).")
    print("Для выражений: константы pi, e, i.")
    print("Для уравнений: латинские буквы как переменные.")

    while True:
        choice = input("Выберите режим (1, 2 или 3): ")
        
        if choice == '1':
            # Вычисление выражения
            expression = input("Введите выражение: ")
            try:
                result = calculate_expression(expression)
                print(f"Результат: {result}")
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == '2':
            # Решение уравнения
            eq = input("Введите уравнение (например, x + 1 = 2): ")
            try:
                solutions = solve_equation(eq)
                if solutions:
                    print(f"Решения: {solutions}")
                else:
                    print("Нет решений")
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == '3':
            # Решение квадратного уравнения
            print("Введите коэффициенты для уравнения a*x^2 + b*x + c = 0")
            try:
                a = float(input("Введите коэффициент a: "))
                b = float(input("Введите коэффициент b: "))
                c = float(input("Введите коэффициент c: "))
                x1, x2 = solve_quadratic(a, b, c)
                print(f"Решения: x1 = {x1}, x2 = {x2}")
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        else:
            print("Неверный выбор. Введите 1, 2 или 3.")
            continue
        
        # Спрашиваем, хочет ли пользователь продолжить
        continue_calc = input("Продолжить? (1 - да, 2 - нет): ")
        if continue_calc != '1':
            print("Спасибо за использование калькулятора!")
            break

# Запуск программы
if __name__ == "__main__":
    main()