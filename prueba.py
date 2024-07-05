import re


class NodoAST:
    pass

class OperacionBinaria(NodoAST):
    def __init__(self, izquierda, operacion, derecha):
        self.izquierda = izquierda
        self.operacion = operacion
        self.derecha = derecha

class Numero(NodoAST):
    def __init__(self, valor):
        self.valor = valor

class Variable(NodoAST):
    def __init__(self, nombre):
        self.nombre = nombre

class Asignacion(NodoAST):
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

class Imprimir(NodoAST):
    def __init__(self, expresion):
        self.expresion = expresion




class Analizador:
    def __init__(self, entrada):
        self.entrada = entrada
        self.posicion = 0
        self.caracter_actual = self.entrada[self.posicion] if self.entrada else None
        self.variables = {}

    def error(self):
        raise Exception('Error de sintaxis')

    def avanzar(self):
        self.posicion += 1
        self.caracter_actual = self.entrada[self.posicion] if self.posicion < len(self.entrada) else None

    def omitir_espacios(self):
        while self.caracter_actual is not None and self.caracter_actual.isspace():
            self.avanzar()

    def numero(self):
        resultado = ''
        while self.caracter_actual is not None and self.caracter_actual.isdigit():
            resultado += self.caracter_actual
            self.avanzar()
        return Numero(float(resultado))

    def factor(self):
        self.omitir_espacios()
        if self.caracter_actual.isdigit():
            return self.numero()
        elif self.caracter_actual.isalpha():
            return self.variable()
        elif self.caracter_actual == '(':
            self.avanzar()
            nodo = self.expresion()
            if self.caracter_actual == ')':
                self.avanzar()
                return nodo
            else:
                self.error()
        else:
            self.error()

    def termino(self):
        nodo = self.factor()
        while self.caracter_actual is not None and self.caracter_actual in ('*', '/'):
            operacion = self.caracter_actual
            self.avanzar()
            nodo = OperacionBinaria(izquierda=nodo, operacion=operacion, derecha=self.factor())
        return nodo

    def expresion(self):
        nodo = self.termino()
        while self.caracter_actual is not None and self.caracter_actual in ('+', '-'):
            operacion = self.caracter_actual
            self.avanzar()
            nodo = OperacionBinaria(izquierda=nodo, operacion=operacion, derecha=self.termino())
        return nodo

    def variable(self):
        resultado = ''
        while self.caracter_actual is not None and self.caracter_actual.isalnum():
            resultado += self.caracter_actual
            self.avanzar()
        return Variable(resultado)

    def asignacion(self):
        var = self.variable()
        self.omitir_espacios()
        if self.caracter_actual == '=':
            self.avanzar()
            valor = self.expresion()
            return Asignacion(var.nombre, valor)
        else:
            self.error()

    def sentencia(self):
        self.omitir_espacios()
        if self.caracter_actual.isalpha():
            var = self.variable()
            self.omitir_espacios()
            if self.caracter_actual == '=':
                self.avanzar()
                valor = self.expresion()
                self.omitir_espacios()
                if self.caracter_actual == ';':
                    self.avanzar()
                    return Asignacion(var.nombre, valor)
                else:
                    self.error()
            elif var.nombre == "print":
                expr = self.expresion()
                self.omitir_espacios()
                if self.caracter_actual == ';':
                    self.avanzar()
                    return Imprimir(expr)
                else:
                    self.error()
        self.error()

    def parsear(self):
        nodos = []
        while self.caracter_actual is not None:
            nodo = self.sentencia()
            if nodo is not None:
                nodos.append(nodo)
            self.omitir_espacios()
        return nodos

class Evaluador:
    def __init__(self):
        self.variables = {}

    def visitar(self, nodo):
        if isinstance(nodo, Numero):
            return nodo.valor
        elif isinstance(nodo, Variable):
            return self.variables.get(nodo.nombre, 0)
        elif isinstance(nodo, OperacionBinaria):
            izquierda = self.visitar(nodo.izquierda)
            derecha = self.visitar(nodo.derecha)
            if nodo.operacion == '+':
                return izquierda + derecha
            elif nodo.operacion == '-':
                return izquierda - derecha
            elif nodo.operacion == '*':
                return izquierda * derecha
            elif nodo.operacion == '/':
                return izquierda / derecha
        elif isinstance(nodo, Asignacion):
            valor = self.visitar(nodo.valor)
            self.variables[nodo.nombre] = valor
            return valor
        elif isinstance(nodo, Imprimir):
            valor = self.visitar(nodo.expresion)
            return valor

    def evaluar(self, nodos):
        resultados = []
        for nodo in nodos:
            resultado = self.visitar(nodo)
            if isinstance(nodo, Imprimir):
                resultados.append(resultado)
        return resultados


import tkinter as tk
from tkinter import font as tkfont

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
            parser = Analizador(codigo)
            nodos = parser.parsear()
            evaluador = Evaluador()
            resultados = evaluador.evaluar(nodos)

            self.output_text.delete('1.0', tk.END)
            for resultado in resultados:
                self.output_text.insert(tk.END, str(resultado) + "\n")
        except Exception as e:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, str(e))

root = tk.Tk()
app = Aplicacion(master=root)
app.mainloop()
