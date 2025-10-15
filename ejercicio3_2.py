import tkinter as tk
from tkinter import messagebox
import math

class FiguraGeometrica:
    def __init__(self):
        self.volumen = 0.0
        self.superficie = 0.0

class Cilindro(FiguraGeometrica):
    def __init__(self, radio, altura):
        super().__init__()
        self.radio = radio
        self.altura = altura
        self.volumen = self.calcular_volumen()
        self.superficie = self.calcular_superficie()

    def calcular_volumen(self):
        return math.pi * self.altura * math.pow(self.radio, 2)

    def calcular_superficie(self):
        area_lateral = 2 * math.pi * self.radio * self.altura
        area_bases = 2 * math.pi * math.pow(self.radio, 2)
        return area_lateral + area_bases

class Esfera(FiguraGeometrica):
    def __init__(self, radio):
        super().__init__()
        self.radio = radio
        self.volumen = self.calcular_volumen()
        self.superficie = self.calcular_superficie()
        
    def calcular_volumen(self):
        return (4/3) * math.pi * math.pow(self.radio, 3)
        
    def calcular_superficie(self):
        return 4 * math.pi * math.pow(self.radio, 2)

class Piramide(FiguraGeometrica):
    def __init__(self, base, altura, apotema):
        super().__init__()
        self.base = base
        self.altura = altura
        self.apotema = apotema
        self.volumen = self.calcular_volumen()
        self.superficie = self.calcular_superficie()

    def calcular_volumen(self):
        return (math.pow(self.base, 2) * self.altura) / 3

    def calcular_superficie(self):
        area_base = math.pow(self.base, 2)
        area_lateral = 2 * self.base * self.apotema
        return area_base + area_lateral

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Figuras Geométricas")
        self.geometry("350x160")
        self.resizable(False, False)

        tk.Button(self, text="Cilindro", command=self.abrir_ventana_cilindro).place(x=20, y=50, width=80)
        tk.Button(self, text="Esfera", command=self.abrir_ventana_esfera).place(x=125, y=50, width=80)
        tk.Button(self, text="Pirámide", command=self.abrir_ventana_piramide).place(x=225, y=50, width=100)

    def abrir_ventana_cilindro(self):
        ventana = tk.Toplevel(self)
        ventana.title("Cilindro")
        ventana.geometry("280x240")
        ventana.resizable(False, False)

        tk.Label(ventana, text="Radio (cms):").place(x=20, y=20)
        campo_radio = tk.Entry(ventana)
        campo_radio.place(x=100, y=20, width=150)

        tk.Label(ventana, text="Altura (cms):").place(x=20, y=50)
        campo_altura = tk.Entry(ventana)
        campo_altura.place(x=100, y=50, width=150)

        label_volumen = tk.Label(ventana, text="Volumen (cm3):")
        label_volumen.place(x=20, y=120)
        label_superficie = tk.Label(ventana, text="Superficie (cm2):")
        label_superficie.place(x=20, y=150)

        def calcular():
            try:
                radio = float(campo_radio.get())
                altura = float(campo_altura.get())
                cilindro = Cilindro(radio, altura)
                label_volumen.config(text=f"Volumen (cm3): {cilindro.volumen:.2f}")
                label_superficie.config(text=f"Superficie (cm2): {cilindro.superficie:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.", parent=ventana)
        
        tk.Button(ventana, text="Calcular", command=calcular).place(x=100, y=80, width=80)

    def abrir_ventana_esfera(self):
        ventana = tk.Toplevel(self)
        ventana.title("Esfera")
        ventana.geometry("280x210")
        ventana.resizable(False, False)
        
        tk.Label(ventana, text="Radio (cms):").place(x=20, y=20)
        campo_radio = tk.Entry(ventana)
        campo_radio.place(x=100, y=20, width=150)

        label_volumen = tk.Label(ventana, text="Volumen (cm3):")
        label_volumen.place(x=20, y=90)
        label_superficie = tk.Label(ventana, text="Superficie (cm2):")
        label_superficie.place(x=20, y=120)
        
        def calcular():
            try:
                radio = float(campo_radio.get())
                esfera = Esfera(radio)
                label_volumen.config(text=f"Volumen (cm3): {esfera.volumen:.2f}")
                label_superficie.config(text=f"Superficie (cm2): {esfera.superficie:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un valor numérico válido.", parent=ventana)

        tk.Button(ventana, text="Calcular", command=calcular).place(x=100, y=50, width=80)

    def abrir_ventana_piramide(self):
        ventana = tk.Toplevel(self)
        ventana.title("Pirámide")
        ventana.geometry("280x270")
        ventana.resizable(False, False)

        tk.Label(ventana, text="Base (cms):").place(x=20, y=20)
        campo_base = tk.Entry(ventana)
        campo_base.place(x=120, y=20, width=135)

        tk.Label(ventana, text="Altura (cms):").place(x=20, y=50)
        campo_altura = tk.Entry(ventana)
        campo_altura.place(x=120, y=50, width=135)

        tk.Label(ventana, text="Apotema (cms):").place(x=20, y=80)
        campo_apotema = tk.Entry(ventana)
        campo_apotema.place(x=120, y=80, width=135)

        label_volumen = tk.Label(ventana, text="Volumen (cm3):")
        label_volumen.place(x=20, y=150)
        label_superficie = tk.Label(ventana, text="Superficie (cm2):")
        label_superficie.place(x=20, y=180)

        def calcular():
            try:
                base = float(campo_base.get())
                altura = float(campo_altura.get())
                apotema = float(campo_apotema.get())
                piramide = Piramide(base, altura, apotema)
                label_volumen.config(text=f"Volumen (cm3): {piramide.volumen:.2f}")
                label_superficie.config(text=f"Superficie (cm2): {piramide.superficie:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.", parent=ventana)

        tk.Button(ventana, text="Calcular", command=calcular).place(x=100, y=110, width=80)

def main():
    app = VentanaPrincipal()
    app.mainloop()

main()
