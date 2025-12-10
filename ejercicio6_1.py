import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from enum import Enum

# Enumerados para cargo y género
class TipoCargo(Enum):
    DIRECTIVO = "Directivo"
    ESTRATEGICO = "Estratégico"
    OPERATIVO = "Operativo"

class TipoGenero(Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"

# Clase Empleado
class Empleado:
    def __init__(self, nombre, apellidos, cargo, genero, salario_dia, dias_trabajados, otros_ingresos, pagos_salud, aporte_pensiones):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pensiones = aporte_pensiones

    def calcular_nomina(self):
        return (self.salario_dia * self.dias_trabajados) + self.otros_ingresos - self.pagos_salud - self.aporte_pensiones

# Clase ListaEmpleados
class ListaEmpleados:
    def __init__(self):
        self.lista = []
        self.total_nomina = 0

    def agregar_empleado(self, empleado):
        self.lista.append(empleado)

    def calcular_total_nomina(self):
        self.total_nomina = sum(e.calcular_nomina() for e in self.lista)
        return self.total_nomina

    def obtener_matriz(self):
        return [[e.nombre, e.apellidos, f"${e.calcular_nomina():.2f}"] for e in self.lista]

    def convertir_texto(self):
        texto = ""
        for e in self.lista:
            texto += (
                f"Nombre = {e.nombre}\n"
                f"Apellidos = {e.apellidos}\n"
                f"Cargo = {e.cargo.value}\n"
                f"Género = {e.genero.value}\n"
                f"Salario = ${e.salario_dia}\n"
                f"Días trabajados = {e.dias_trabajados}\n"
                f"Otros ingresos = ${e.otros_ingresos}\n"
                f"Pagos salud = ${e.pagos_salud}\n"
                f"Aportes pensiones = ${e.aporte_pensiones}\n---------\n"
            )
        texto += f"Total nómina = ${self.calcular_total_nomina():.2f}"
        return texto

# Ventana para agregar empleado
class VentanaAgregarEmpleado(tk.Toplevel):
    def __init__(self, master, lista_empleados):
        super().__init__(master)
        self.title("Agregar Empleado")
        self.geometry("320x420")
        self.resizable(False, False)
        self.lista = lista_empleados
        self.create_widgets()

    def create_widgets(self):
        # Nombre
        ttk.Label(self, text="Nombre:").place(x=20, y=20)
        self.campo_nombre = ttk.Entry(self)
        self.campo_nombre.place(x=160, y=20, width=120)
        # Apellidos
        ttk.Label(self, text="Apellidos:").place(x=20, y=50)
        self.campo_apellidos = ttk.Entry(self)
        self.campo_apellidos.place(x=160, y=50, width=120)
        # Cargo
        ttk.Label(self, text="Cargo:").place(x=20, y=80)
        self.campo_cargo = ttk.Combobox(self, values=[c.value for c in TipoCargo], state="readonly")
        self.campo_cargo.current(0)
        self.campo_cargo.place(x=160, y=80, width=120)
        # Género
        ttk.Label(self, text="Género:").place(x=20, y=110)
        self.genero_var = tk.StringVar(value=TipoGenero.MASCULINO.value)
        self.radio_m = ttk.Radiobutton(self, text="Masculino", variable=self.genero_var, value=TipoGenero.MASCULINO.value)
        self.radio_f = ttk.Radiobutton(self, text="Femenino", variable=self.genero_var, value=TipoGenero.FEMENINO.value)
        self.radio_m.place(x=160, y=110)
        self.radio_f.place(x=160, y=140)
        # Salario por día
        ttk.Label(self, text="Salario por día:").place(x=20, y=170)
        self.campo_salario_dia = ttk.Entry(self)
        self.campo_salario_dia.place(x=160, y=170, width=120)
        # Días trabajados
        ttk.Label(self, text="Días trabajados al mes:").place(x=20, y=200)
        self.campo_dias = ttk.Spinbox(self, from_=1, to=31)
        self.campo_dias.place(x=160, y=200, width=50)
        # Otros ingresos
        ttk.Label(self, text="Otros ingresos:").place(x=20, y=230)
        self.campo_otros = ttk.Entry(self)
        self.campo_otros.place(x=160, y=230, width=120)
        # Pagos salud
        ttk.Label(self, text="Pagos por salud:").place(x=20, y=260)
        self.campo_salud = ttk.Entry(self)
        self.campo_salud.place(x=160, y=260, width=120)
        # Aporte pensiones
        ttk.Label(self, text="Aportes pensiones:").place(x=20, y=290)
        self.campo_pensiones = ttk.Entry(self)
        self.campo_pensiones.place(x=160, y=290, width=120)
        # Botones
        self.btn_agregar = ttk.Button(self, text="Agregar", command=self.agregar_empleado)
        self.btn_agregar.place(x=40, y=340, width=100)
        self.btn_limpiar = ttk.Button(self, text="Borrar", command=self.limpiar_campos)
        self.btn_limpiar.place(x=180, y=340, width=100)

    def limpiar_campos(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_apellidos.delete(0, tk.END)
        self.campo_salario_dia.delete(0, tk.END)
        self.campo_dias.delete(0, tk.END)
        self.campo_otros.delete(0, tk.END)
        self.campo_salud.delete(0, tk.END)
        self.campo_pensiones.delete(0, tk.END)
        self.campo_dias.insert(0, "1")

    def agregar_empleado(self):
        try:
            nombre = self.campo_nombre.get().strip()
            apellidos = self.campo_apellidos.get().strip()
            cargo = TipoCargo(self.campo_cargo.get())
            genero = TipoGenero(self.genero_var.get())
            salario_dia = float(self.campo_salario_dia.get())
            dias_trabajados = int(self.campo_dias.get())
            otros_ingresos = float(self.campo_otros.get()) if self.campo_otros.get() else 0
            pagos_salud = float(self.campo_salud.get()) if self.campo_salud.get() else 0
            aporte_pensiones = float(self.campo_pensiones.get()) if self.campo_pensiones.get() else 0
            if not nombre or not apellidos:
                raise ValueError
            empleado = Empleado(nombre, apellidos, cargo, genero, salario_dia, dias_trabajados, otros_ingresos, pagos_salud, aporte_pensiones)
            self.lista.agregar_empleado(empleado)
            messagebox.showinfo("Mensaje", "El empleado ha sido agregado")
            self.limpiar_campos()
        except Exception:
            messagebox.showerror("Error", "Campo nulo o error en formato de número")

# Ventana para mostrar nómina
class VentanaNomina(tk.Toplevel):
    def __init__(self, master, lista_empleados):
        super().__init__(master)
        self.title("Nómina de Empleados")
        self.geometry("400x300")
        self.resizable(False, False)
        self.lista = lista_empleados
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Lista de empleados:").place(x=20, y=10)
        columns = ("Nombre", "Apellidos", "Sueldo")
        self.tabla = ttk.Treeview(self, columns=columns, show="headings", height=8)
        for col in columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120)
        self.tabla.place(x=20, y=40)
        for fila in self.lista.obtener_matriz():
            self.tabla.insert("", tk.END, values=fila)
        total = self.lista.calcular_total_nomina()
        ttk.Label(self, text=f"Total nómina mensual = ${total:.2f}").place(x=20, y=250)

# Ventana principal
class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nómina")
        self.geometry("300x380")
        self.resizable(False, False)
        self.empleados = ListaEmpleados()
        self.create_menu()

    def create_menu(self):
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(label="Agregar empleado", command=self.abrir_agregar_empleado)
        menu_opciones.add_command(label="Calcular nómina", command=self.abrir_nomina)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Guardar archivo", command=self.guardar_archivo)
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

    def abrir_agregar_empleado(self):
        VentanaAgregarEmpleado(self, self.empleados)

    def abrir_nomina(self):
        VentanaNomina(self, self.empleados)

    def guardar_archivo(self):
        carpeta = filedialog.askdirectory(title="Seleccione la carpeta para guardar Nómina.txt")
        if carpeta:
            ruta = f"{carpeta}/Nómina.txt"
            try:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(self.empleados.convertir_texto())
                messagebox.showinfo("Mensaje", f"El archivo de la nómina Nómina.txt se ha creado en {carpeta}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

if __name__ == "__main__":
    VentanaPrincipal().mainloop()
