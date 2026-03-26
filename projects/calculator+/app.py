import tkinter as tk
from tkinter import ttk, messagebox

from calculator import (
    calculate_expression,
    solve_equation,
    solve_quadratic,
)


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator+")
        self.geometry("700x520")
        self.minsize(620, 480)

        self._build_ui()

    def _build_ui(self):
        header = ttk.Label(
            self,
            text="Calculator+",
            font=("Helvetica", 20, "bold"),
        )
        header.pack(pady=(16, 8))

        subtitle = ttk.Label(
            self,
            text=(
                "Выражения: +, -, *, /, ^, (), pi, e, i. "
                "Уравнения: латинские буквы как переменные."
            ),
        )
        subtitle.pack(pady=(0, 12))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=16, pady=8)

        expr_tab = ttk.Frame(notebook)
        eq_tab = ttk.Frame(notebook)
        quad_tab = ttk.Frame(notebook)

        notebook.add(expr_tab, text="Выражение")
        notebook.add(eq_tab, text="Уравнение")
        notebook.add(quad_tab, text="Квадратное")

        self._build_expression_tab(expr_tab)
        self._build_equation_tab(eq_tab)
        self._build_quadratic_tab(quad_tab)

    def _build_expression_tab(self, parent):
        ttk.Label(parent, text="Введите выражение:").pack(anchor="w", padx=12, pady=(12, 4))
        self.expr_entry = ttk.Entry(parent, font=("Helvetica", 12))
        self.expr_entry.pack(fill="x", padx=12, pady=(0, 8))

        btn_row = ttk.Frame(parent)
        btn_row.pack(fill="x", padx=12, pady=(0, 8))
        ttk.Button(btn_row, text="Вычислить", command=self._on_calc_expression).pack(side="left")
        ttk.Button(btn_row, text="Очистить", command=lambda: self._clear_entry(self.expr_entry)).pack(
            side="left", padx=(8, 0)
        )

        self._build_keypad(parent)

        ttk.Label(parent, text="Результат:").pack(anchor="w", padx=12, pady=(8, 4))
        self.expr_result = tk.Text(parent, height=6, wrap="word", font=("Helvetica", 12))
        self.expr_result.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self._set_readonly(self.expr_result, True)

    def _build_equation_tab(self, parent):
        ttk.Label(parent, text="Введите уравнение (например, x + 1 = 2):").pack(
            anchor="w", padx=12, pady=(12, 4)
        )
        self.eq_entry = ttk.Entry(parent, font=("Helvetica", 12))
        self.eq_entry.pack(fill="x", padx=12, pady=(0, 8))

        btn_row = ttk.Frame(parent)
        btn_row.pack(fill="x", padx=12, pady=(0, 8))
        ttk.Button(btn_row, text="Решить", command=self._on_solve_equation).pack(side="left")
        ttk.Button(btn_row, text="Очистить", command=lambda: self._clear_entry(self.eq_entry)).pack(
            side="left", padx=(8, 0)
        )

        ttk.Label(parent, text="Решения:").pack(anchor="w", padx=12, pady=(8, 4))
        self.eq_result = tk.Text(parent, height=6, wrap="word", font=("Helvetica", 12))
        self.eq_result.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self._set_readonly(self.eq_result, True)

    def _build_quadratic_tab(self, parent):
        ttk.Label(parent, text="Уравнение: a*x^2 + b*x + c = 0").pack(
            anchor="w", padx=12, pady=(12, 4)
        )

        grid = ttk.Frame(parent)
        grid.pack(fill="x", padx=12, pady=(0, 8))

        ttk.Label(grid, text="a").grid(row=0, column=0, sticky="w")
        self.a_entry = ttk.Entry(grid, width=12, font=("Helvetica", 12))
        self.a_entry.grid(row=0, column=1, padx=(4, 16), sticky="w")

        ttk.Label(grid, text="b").grid(row=0, column=2, sticky="w")
        self.b_entry = ttk.Entry(grid, width=12, font=("Helvetica", 12))
        self.b_entry.grid(row=0, column=3, padx=(4, 16), sticky="w")

        ttk.Label(grid, text="c").grid(row=0, column=4, sticky="w")
        self.c_entry = ttk.Entry(grid, width=12, font=("Helvetica", 12))
        self.c_entry.grid(row=0, column=5, padx=(4, 0), sticky="w")

        btn_row = ttk.Frame(parent)
        btn_row.pack(fill="x", padx=12, pady=(0, 8))
        ttk.Button(btn_row, text="Решить", command=self._on_solve_quadratic).pack(side="left")
        ttk.Button(btn_row, text="Очистить", command=self._clear_quadratic).pack(
            side="left", padx=(8, 0)
        )

        ttk.Label(parent, text="Результат:").pack(anchor="w", padx=12, pady=(8, 4))
        self.quad_result = tk.Text(parent, height=6, wrap="word", font=("Helvetica", 12))
        self.quad_result.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self._set_readonly(self.quad_result, True)

    def _build_keypad(self, parent):
        keypad = ttk.LabelFrame(parent, text="Кнопочная панель")
        keypad.pack(fill="x", padx=12, pady=(0, 8))

        buttons = [
            ["7", "8", "9", "/", "(", ")"],
            ["4", "5", "6", "*", "^", "pi"],
            ["1", "2", "3", "-", "e", "i"],
            ["0", ".", "+", "←", "C"],
        ]

        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                btn = ttk.Button(
                    keypad,
                    text=label,
                    command=lambda v=label: self._on_keypad_press(v),
                    width=5,
                )
                btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        for c in range(6):
            keypad.grid_columnconfigure(c, weight=1)

    def _clear_entry(self, entry):
        entry.delete(0, tk.END)

    def _clear_quadratic(self):
        for entry in (self.a_entry, self.b_entry, self.c_entry):
            entry.delete(0, tk.END)

    def _set_readonly(self, text_widget, readonly):
        text_widget.configure(state=("disabled" if readonly else "normal"))

    def _write_result(self, text_widget, content):
        self._set_readonly(text_widget, False)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, content)
        self._set_readonly(text_widget, True)

    def _on_calc_expression(self):
        expression = self.expr_entry.get()
        try:
            result = calculate_expression(expression)
            self._write_result(self.expr_result, str(result))
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))

    def _on_keypad_press(self, value):
        if value == "C":
            self._clear_entry(self.expr_entry)
            return
        if value == "←":
            current = self.expr_entry.get()
            if current:
                self.expr_entry.delete(len(current) - 1, tk.END)
            return
        if value in ("pi", "e", "i"):
            insert_value = value
        else:
            insert_value = value
        self.expr_entry.insert(tk.END, insert_value)
        self.expr_entry.focus_set()

    def _on_solve_equation(self):
        eq = self.eq_entry.get()
        try:
            solutions = solve_equation(eq)
            if solutions:
                self._write_result(self.eq_result, str(solutions))
            else:
                self._write_result(self.eq_result, "Нет решений")
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))

    def _on_solve_quadratic(self):
        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            c = float(self.c_entry.get())
            x1, x2 = solve_quadratic(a, b, c)
            self._write_result(self.quad_result, f"x1 = {x1}\nx2 = {x2}")
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
