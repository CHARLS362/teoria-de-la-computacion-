import re
import tkinter as tk
from tkinter import font as tkfont

tokens = [
    ('IMPRIMIR', r'\bprint\b'),
    ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('NUM', r'\d+'),
    ('SUMA', r'\+'),
    ('RESTA', r'-'),
    ('MULTIPLICA', r'\*'),
    ('DIVIDE', r'/'),
    ('IGUAL', r'='),
    ('PUNTOYCOMA', r';'),
    ('OMITIR', r'[ \t\n]+'),
]

def lexer(codigo):
    regex_tokens = '|'.join('(?P<%s>%s)' % par for par in tokens)
    for match in re.finditer(regex_tokens, codigo):
        tipo_token = match.lastgroup
        valor_token = match.group(tipo_token)
        if tipo_token != 'OMITIR':
            yield tipo_token, valor_token

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.token_actual = self.tokens.pop(0) if self.tokens else None
        self.variables = {}

    def error(self):
        raise Exception('Error de sintaxis')

    def consumir(self, tipo_token):
        if self.token_actual and self.token_actual[0] == tipo_token:
            self.token_actual = self.tokens.pop(0) if self.tokens else None
        else:
            self.error()

    def factor(self):
        tipo_token, valor_token = self.token_actual
        if tipo_token == 'ID':
            self.consumir('ID')
            return self.variables.get(valor_token, 0)
        elif tipo_token == 'NUM':
            self.consumir('NUM')
            return int(valor_token)
        else:
            self.error()

    def termino(self):
        resultado = self.factor()
        while self.token_actual and self.token_actual[0] in ('MULTIPLICA', 'DIVIDE'):
            tipo_token, valor_token = self.token_actual
            if tipo_token == 'MULTIPLICA':
                self.consumir('MULTIPLICA')
                resultado *= self.factor()
            elif tipo_token == 'DIVIDE':
                self.consumir('DIVIDE')
                resultado /= self.factor()
        return resultado

    def expresion(self):
        resultado = self.termino()
        while self.token_actual and self.token_actual[0] in ('SUMA', 'RESTA'):
            tipo_token, valor_token = self.token_actual
            if tipo_token == 'SUMA':
                self.consumir('SUMA')
                resultado += self.termino()
            elif tipo_token == 'RESTA':
                self.consumir('RESTA')
                resultado -= self.termino()
        return resultado

    def declaracion(self):
        nombre_var = self.token_actual[1]
        self.consumir('ID')
        self.consumir('IGUAL')
        resultado = self.expresion()
        self.variables[nombre_var] = resultado
        self.consumir('PUNTOYCOMA')
        return resultado

    def sentencia(self):
        if self.token_actual and self.token_actual[0] == 'IMPRIMIR':
            self.consumir('IMPRIMIR')
            resultado = self.expresion()
            self.consumir('PUNTOYCOMA')
            return resultado
        else:
            return self.declaracion()

    def analizar(self):
        resultados = []
        while self.token_actual:
            resultado = self.sentencia()
            if resultado is not None:
                resultados.append(resultado)
        return resultados

class Aplicacion(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Analizador Sintáctico")
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

        self.run_button = tk.Button(self, text="Ejecutar", command=self.ejecutar_analizador, font=self.font, bg="orange", fg="white", pady=10, padx=20)
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
            parser = AnalizadorSintactico(lexer(codigo))
            resultados = parser.analizar()

            self.output_text.delete('1.0', tk.END)
            for resultado in resultados:
                self.output_text.insert(tk.END, str(resultado) + "\n")
        except Exception as e:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, str(e))

root = tk.Tk()
app = Aplicacion(master=root)
app.mainloop()
