import tkinter as tk
from tkinter import messagebox
import math

class Notas:
    def __init__(self):

        self.lista_notas = []

    def calcular_promedio(self):
        return sum(self.lista_notas) / len(self.lista_notas)

    def calcular_desviacion(self):
        prom = self.calcular_promedio()
        suma_cuadrados = 0
        for nota in self.lista_notas:
            suma_cuadrados += math.pow(nota - prom, 2)
        return math.sqrt(suma_cuadrados / len(self.lista_notas))

    def calcular_mayor(self):

        return max(self.lista_notas)

    def calcular_menor(self):

        return min(self.lista_notas)

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.notas_logica = Notas()

        self.title("Notas")
        self.geometry("280x380")
        self.resizable(False, False) 

        self.crear_widgets()

    def crear_widgets(self):
        self.campos_notas = []
        labels_text = ["Nota 1:", "Nota 2:", "Nota 3:", "Nota 4:", "Nota 5:"]

        for i, texto in enumerate(labels_text):
            label = tk.Label(self, text=texto)
            label.place(x=20, y=20 + i * 30)
            campo = tk.Entry(self)
            campo.place(x=105, y=20 + i * 30, width=135, height=23)
            self.campos_notas.append(campo)
            
        btn_calcular = tk.Button(self, text="Calcular", command=self.calcular_notas)
        btn_calcular.place(x=20, y=170, width=100, height=23)

        btn_limpiar = tk.Button(self, text="Limpiar", command=self.limpiar_campos)
        btn_limpiar.place(x=125, y=170, width=80, height=23)
        self.label_promedio = tk.Label(self, text="Promedio = ")
        self.label_promedio.place(x=20, y=210)
        
        self.label_desviacion = tk.Label(self, text="Desviación estándar = ")
        self.label_desviacion.place(x=20, y=240)

        self.label_mayor = tk.Label(self, text="Valor mayor = ")
        self.label_mayor.place(x=20, y=270)
        
        self.label_menor = tk.Label(self, text="Valor menor = ")
        self.label_menor.place(x=20, y=300)

    def calcular_notas(self):
        try:
            self.notas_logica.lista_notas.clear()
            for campo in self.campos_notas:
                self.notas_logica.lista_notas.append(float(campo.get()))
            self.label_promedio.config(text=f"Promedio = {self.notas_logica.calcular_promedio():.2f}")
            self.label_desviacion.config(text=f"Desviación estándar = {self.notas_logica.calcular_desviacion():.2f}")
            self.label_mayor.config(text=f"Valor mayor = {self.notas_logica.calcular_mayor()}")
            self.label_menor.config(text=f"Valor menor = {self.notas_logica.calcular_menor()}")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese solo valores numéricos en todos los campos.")

    def limpiar_campos(self):
        """
        Esta función se ejecuta cuando se presiona el botón "Limpiar".
        """
        for campo in self.campos_notas:
            campo.delete(0, tk.END)
        
        self.label_promedio.config(text="Promedio = ")
        self.label_desviacion.config(text="Desviación estándar = ")
        self.label_mayor.config(text="Valor mayor = ")
        self.label_menor.config(text="Valor menor = ")

def main():
    app = VentanaPrincipal()
    app.mainloop()

main()
