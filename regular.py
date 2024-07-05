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

        self.run_button = tk.Button(self, text="Evaluar", command=self.ejecutar_evaluador, font=self.font, bg="orange", fg="white", pady=10, padx=20)
        self.run_button.pack(pady=20)

        self.output_text = tk.Text(self, height=10, width=60, font=self.font)
        self.output_text.pack(pady=10)

    def ejecutar_evaluador(self):
        var1 = self.entry_var1.get()
        var2 = self.entry_var2.get()
        val1 = self.entry_val1.get()
        val2 = self.entry_val2.get()

        try:
            contexto = {var1: float(val1), var2: float(val2)}
            
            suma = eval(f"{var1} + {var2}", {}, contexto)
            resta = eval(f"{var1} - {var2}", {}, contexto)
            multiplicacion = eval(f"{var1} * {var2}", {}, contexto)
            division = eval(f"{var1} / {var2}", {}, contexto)

            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, f"{var1} + {var2} = {suma}\n")
            self.output_text.insert(tk.END, f"{var1} - {var2} = {resta}\n")
            self.output_text.insert(tk.END, f"{var1} * {var2} = {multiplicacion}\n")
            self.output_text.insert(tk.END, f"{var1} / {var2} = {division}\n")
        except Exception as e:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, str(e))

root = tk.Tk()
app = Aplicacion(master=root)
app.mainloop()
