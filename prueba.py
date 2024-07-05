import re
import tkinter as tk
from tkinter import font as tkfont

class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(ASTNode):
    def __init__(self, value):
        self.value = value

class Var(ASTNode):
    def __init__(self, name):
        self.name = name

class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Print(ASTNode):
    def __init__(self, expr):
        self.expr = expr




class Parser:
    def __init__(self, input):
        self.input = input
        self.pos = 0
        self.current_char = self.input[self.pos] if self.input else None
        self.variables = {}

    def error(self):
        raise Exception('Error de sintaxis')

    def advance(self):
        self.pos += 1
        self.current_char = self.input[self.pos] if self.pos < len(self.input) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Num(float(result))

    def factor(self):
        self.skip_whitespace()
        if self.current_char.isdigit():
            return self.number()
        elif self.current_char.isalpha():
            return self.variable()
        elif self.current_char == '(':
            self.advance()
            node = self.expr()
            if self.current_char == ')':
                self.advance()
                return node
            else:
                self.error()
        else:
            self.error()

    def term(self):
        node = self.factor()
        while self.current_char is not None and self.current_char in ('*', '/'):
            op = self.current_char
            self.advance()
            node = BinOp(left=node, op=op, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_char is not None and self.current_char in ('+', '-'):
            op = self.current_char
            self.advance()
            node = BinOp(left=node, op=op, right=self.term())
        return node

    def variable(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return Var(result)

    def assignment(self):
        var = self.variable()
        self.skip_whitespace()
        if self.current_char == '=':
            self.advance()
            value = self.expr()
            return Assign(var.name, value)
        else:
            self.error()

    def statement(self):
        self.skip_whitespace()
        if self.current_char.isalpha():
            var = self.variable()
            self.skip_whitespace()
            if self.current_char == '=':
                self.advance()
                value = self.expr()
                self.skip_whitespace()
                if self.current_char == ';':
                    self.advance()
                    return Assign(var.name, value)
                else:
                    self.error()
            elif var.name == "print":
                expr = self.expr()
                self.skip_whitespace()
                if self.current_char == ';':
                    self.advance()
                    return Print(expr)
                else:
                    self.error()
        self.error()

    def parse(self):
        nodes = []
        while self.current_char is not None:
            node = self.statement()
            if node is not None:
                nodes.append(node)
            self.skip_whitespace()
        return nodes

class Evaluator:
    def __init__(self):
        self.variables = {}

    def visit(self, node):
        if isinstance(node, Num):
            return node.value
        elif isinstance(node, Var):
            return self.variables.get(node.name, 0)
        elif isinstance(node, BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right
        elif isinstance(node, Assign):
            value = self.visit(node.value)
            self.variables[node.name] = value
            return value
        elif isinstance(node, Print):
            value = self.visit(node.expr)
            print(value)
            return value

    def evaluate(self, nodes):
        results = []
        for node in nodes:
            result = self.visit(node)
            results.append(result)
        return results


class Aplicacion(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Evaluador de Expresiones")
        self.master.geometry("700x700")
        self.pack()
        self.crear_widgets()

    def crear_widgets(self):
        self.font = tkfont.Font(family="Helvetica", size=12)

        self.label_var1 = tk.Label(self, text="Nombre de la primera variable:", font=self.font)
        self.label_var1.config(bg="lightblue", fg="navy", pady=10, padx=10)
        self.label_var1.pack()

        self.entry_var1 = tk.Entry(self, highlightthickness=1, highlightbackground="green", highlightcolor="green", font=self.font)
        self.entry_var1.pack(pady=5)

        self.label_val1 = tk.Label(self, text="Valor de la primera variable:", font=self.font)
        self.label_val1.config(bg="lightblue", fg="navy", pady=10, padx=10)
        self.label_val1.pack()

        self.entry_val1 = tk.Entry(self, highlightthickness=1, highlightbackground="green", highlightcolor="green", font=self.font)
        self.entry_val1.pack(pady=5)

        self.label_var2 = tk.Label(self, text="Nombre de la segunda variable:", font=self.font)
        self.label_var2.config(bg="lightgreen", fg="darkgreen", pady=10, padx=10)
        self.label_var2.pack()

        self.entry_var2 = tk.Entry(self, highlightthickness=1, highlightbackground="green", highlightcolor="green", font=self.font)
        self.entry_var2.pack(pady=5)

        self.label_val2 = tk.Label(self, text="Valor de la segunda variable:", font=self.font)
        self.label_val2.config(bg="lightgreen", fg="darkgreen", pady=10, padx=10)
        self.label_val2.pack()

        self.entry_val2 = tk.Entry(self, highlightthickness=1, highlightbackground="green", highlightcolor="green", font=self.font)
        self.entry_val2.pack(pady=5)

        self.run_button = tk.Button(self, text="Evaluar", command=self.ejecutar_analizador, font=self.font, bg="orange", fg="white", pady=10, padx=20)
        self.run_button.pack(pady=20)

        self.output_text = tk.Text(self, height=10, width=60, font=self.font)
        self.output_text.pack(pady=10)

    def ejecutar_analizador(self):
        var1 = self.entry_var1.get()
        var2 = self.entry_var2.get()
        val1 = self.entry_val1.get()
        val2 = self.entry_val2.get()

        codigo = (
            f"{var1} = {val1}; "
            f"{var2} = {val2}; "
            f"print {var1} + {var2}; "
            f"print {var1} - {var2}; "
            f"print {var1} * {var2}; "
            f"print {var1} / {var2};"
        )

        try:
            parser = Parser(codigo)
            nodes = parser.parse()
            evaluator = Evaluator()
            resultados = evaluator.evaluate(nodes)

            self.output_text.delete('1.0', tk.END)
            for resultado in resultados:
                self.output_text.insert(tk.END, str(resultado) + "\n")
        except Exception as e:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, str(e))

root = tk.Tk()
app = Aplicacion(master=root)
app.mainloop()
