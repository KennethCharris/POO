import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import sys

# -----------------------------------------------------------------------------
# Clase: Huesped
# -----------------------------------------------------------------------------
class Huesped:
    """
    Esta clase denominada Huésped define un huésped del hotel que
    ocupará una determinada habitación por ciertos días.
    """
    def __init__(self, nombres, apellidos, documento_identidad):
        self._nombres = nombres
        self._apellidos = apellidos
        self._documento_identidad = documento_identidad
        self._fecha_ingreso = None
        self._fecha_salida = None

    def set_fecha_salida(self, fecha):
        self._fecha_salida = fecha

    def set_fecha_ingreso(self, fecha):
        self._fecha_ingreso = fecha

    def get_fecha_ingreso(self):
        return self._fecha_ingreso

    def obtener_dias_alojamiento(self):
        """
        Método que calcula la cantidad de días de alojamiento del huésped
        """
        if self._fecha_salida and self._fecha_ingreso:
            delta = self._fecha_salida - self._fecha_ingreso
            return delta.days
        return 0

# -----------------------------------------------------------------------------
# Clase: Habitacion
# -----------------------------------------------------------------------------
class Habitacion:
    """
    Esta clase denominada Habitación define una habitación de un hotel
    a ser ocupada y desocupada por un huésped.
    """
    def __init__(self, numero_habitacion, disponible, precio_dia):
        self._numero_habitacion = numero_habitacion
        self._disponible = disponible
        self._precio_dia = precio_dia
        self._huesped = None

    def get_numero_habitacion(self):
        return self._numero_habitacion

    def get_disponible(self):
        return self._disponible

    def get_precio_dia(self):
        return self._precio_dia

    def get_huesped(self):
        return self._huesped

    def set_huesped(self, huesped):
        self._huesped = huesped

    def set_disponible(self, disponible):
        self._disponible = disponible

# -----------------------------------------------------------------------------
# Clase: Hotel
# -----------------------------------------------------------------------------
class Hotel:
    """
    Esta clase denominada Hotel define un hotel que contiene diez
    habitaciones a ser ocupadas y liberadas por diferentes huéspedes en
    fechas determinadas.
    """
    def __init__(self):
        # En Java es public static Vector<Habitación>, aqui usaremos una lista de instancia
        # dado que se pasa el objeto hotel a las ventanas.
        self.lista_habitaciones = []
        
        # Crea cada habitación con un número, disponibilidad y precio
        # Habitaciones 1-5: 120000
        for i in range(1, 6):
            self.lista_habitaciones.append(Habitacion(i, True, 120000))
        # Habitaciones 6-10: 160000
        for i in range(6, 11):
            self.lista_habitaciones.append(Habitacion(i, True, 160000))

    def buscar_fecha_ingreso_habitacion(self, numero):
        """
        Método que, dado un número de habitación, busca la fecha de ingreso
        """
        for habitacion in self.lista_habitaciones:
            if habitacion.get_numero_habitacion() == numero:
                huesped = habitacion.get_huesped()
                if huesped and huesped.get_fecha_ingreso():
                    return huesped.get_fecha_ingreso().strftime("%Y-%m-%d")
        return ""

    def buscar_habitacion_ocupada(self, numero):
        """
        Método que, dado un número de habitación, devuelve si está ocupada
        """
        for habitacion in self.lista_habitaciones:
            if habitacion.get_numero_habitacion() == numero and not habitacion.get_disponible():
                return True
        return False

# -----------------------------------------------------------------------------
# Clase: VentanaPrincipal
# -----------------------------------------------------------------------------
class VentanaPrincipal(tk.Tk):
    """
    Esta clase define una interfaz gráfica que permitirá gestionar
    el ingreso y salida de huéspedes.
    """
    def __init__(self, hotel):
        super().__init__()
        self.hotel = hotel
        self.titulo = "Hotel"
        self.geometry("280x380")
        self.resizable(False, False)
        self.title(self.titulo)
        
        # Centrar ventana (aproximado en Tkinter)
        self.eval('tk::PlaceWindow . center')

        self.inicio()

    def inicio(self):
        # No usamos layout manager en el frame principal segun instrucciones (null layout)
        # pero para el menu bar no aplica layout del container de contenido.
        
        # Barra de menú
        self.barra_menu = tk.Menu(self)
        self.menu_opciones = tk.Menu(self.barra_menu, tearoff=0)
        
        self.menu_opciones.add_command(label="Consultar habitaciones", command=self.abrir_habitaciones)
        self.menu_opciones.add_command(label="Salida de huéspedes", command=self.salida_huespedes)
        
        self.barra_menu.add_cascade(label="Menú", menu=self.menu_opciones)
        self.config(menu=self.barra_menu)

    def abrir_habitaciones(self):
        ventana = VentanaHabitaciones(self, self.hotel)
        # No usamos setVisible(false) para la principal, ya que es la root.
        # En Java: "se crea la ventana habitaciones... se visualiza".
        # Podemos ocultar la principal si queremos ser exactos con comportamientos de 'navegacion'
        # o dejarla abierta. El texto no dice explicitamente que se oculte la Principal,
        # solo dice que se genera una nueva.
        pass

    def salida_huespedes(self):
        habitacion_str = simpledialog.askstring("Salida de huéspedes", "Ingrese número de habitación", parent=self)
        
        if habitacion_str is not None:
            try:
                numero = int(habitacion_str)
                if numero < 1 or numero > 10:
                    messagebox.showinfo("Mensaje", "El número de habitación debe estar entre 1 y 10")
                elif self.hotel.buscar_habitacion_ocupada(numero):
                    ventana = VentanaSalida(self, self.hotel, numero)
                else:
                    messagebox.showinfo("Mensaje", "La habitación ingresada no ha sido ocupada")
            except ValueError:
                messagebox.showerror("Error", "Campo nulo o error en formato de numero")

# -----------------------------------------------------------------------------
# Clase: VentanaHabitaciones
# -----------------------------------------------------------------------------
class VentanaHabitaciones(tk.Toplevel):
    def __init__(self, parent, hotel):
        super().__init__(parent)
        self.hotel = hotel
        self.title("Habitaciones")
        self.geometry("760x260")
        self.resizable(False, False)
        # Centrar
        # self.eval('tk::PlaceWindow . center') # solo funciona en raiz a veces
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.inicio()

    def inicio(self):
        # Mimetizando el layout null con place
        habitaciones = self.hotel.lista_habitaciones
        
        # Fila 1 (Habitaciones 1-5)
        x_positions = [20, 160, 300, 440, 580]
        for i in range(5):
            hab = habitaciones[i]
            lbl_hab = tk.Label(self.container, text=f"Habitación {hab.get_numero_habitacion()}")
            lbl_hab.place(x=x_positions[i], y=30, width=130, height=23)
            
            estado = "No disponible" if not hab.get_disponible() else "Disponible"
            lbl_est = tk.Label(self.container, text=estado)
            lbl_est.place(x=x_positions[i], y=50, width=100, height=23)

        # Fila 2 (Habitaciones 6-10)
        for i in range(5):
            hab = habitaciones[i+5]
            lbl_hab = tk.Label(self.container, text=f"Habitación {hab.get_numero_habitacion()}")
            lbl_hab.place(x=x_positions[i], y=120, width=130, height=23)
            
            estado = "No disponible" if not hab.get_disponible() else "Disponible"
            lbl_est = tk.Label(self.container, text=estado)
            lbl_est.place(x=x_positions[i], y=140, width=100, height=23)

        # Selección
        lbl_sel = tk.Label(self.container, text="Habitación a reservar:")
        lbl_sel.place(x=250, y=180, width=135, height=23)
        
        self.spinner = tk.Spinbox(self.container, from_=1, to=10)
        self.spinner.place(x=380, y=180, width=50, height=23) # ancho un poco mas para que quepa
        
        btn_aceptar = tk.Button(self.container, text="Aceptar", command=self.accion_aceptar)
        btn_aceptar.place(x=500, y=180, width=100, height=23)

    def accion_aceptar(self):
        try:
            seleccion = int(self.spinner.get())
            if not self.hotel.buscar_habitacion_ocupada(seleccion):
                vent_ingreso = VentanaIngreso(self.master, self.hotel, seleccion)
                self.destroy() # "La ventana con el listado de habitaciones se cierra"
            else:
                messagebox.showinfo("Mensaje", "La habitación está ocupada")
        except ValueError:
            pass

# -----------------------------------------------------------------------------
# Clase: VentanaIngreso
# -----------------------------------------------------------------------------
class VentanaIngreso(tk.Toplevel):
    def __init__(self, parent, hotel, numero_habitacion):
        super().__init__(parent)
        self.hotel = hotel
        self.numero_habitacion_reservada = numero_habitacion
        self.title("Ingreso")
        self.geometry("290x250")
        self.resizable(False, False)
        
        self.inicio()

    def inicio(self):
        # GridBagLayout -> grid
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Habitación Label
        lbl_hab = tk.Label(self.container, text=f"Habitación: {self.numero_habitacion_reservada}")
        lbl_hab.grid(row=0, column=0, sticky="w", padx=3, pady=3)
        
        # Fecha
        lbl_fecha = tk.Label(self.container, text="Fecha (aaaa-mm-dd):")
        lbl_fecha.grid(row=1, column=0, sticky="w", padx=3, pady=3)
        self.txt_fecha = tk.Entry(self.container)
        self.txt_fecha.grid(row=1, column=1, sticky="ew", padx=3, pady=3)
        
        # Huesped Label
        lbl_huesped = tk.Label(self.container, text="Huésped")
        lbl_huesped.grid(row=2, column=0, sticky="w", padx=3, pady=3)
        
        # Nombre
        lbl_nom = tk.Label(self.container, text="Nombre: ")
        lbl_nom.grid(row=3, column=0, sticky="w", padx=3, pady=3)
        self.txt_nom = tk.Entry(self.container)
        self.txt_nom.grid(row=3, column=1, sticky="ew", padx=3, pady=3)
        
        # Apellidos
        lbl_ape = tk.Label(self.container, text="Apellidos: ")
        lbl_ape.grid(row=4, column=0, sticky="w", padx=3, pady=3)
        self.txt_ape = tk.Entry(self.container)
        self.txt_ape.grid(row=4, column=1, sticky="ew", padx=3, pady=3)
        
        # Documento
        lbl_doc = tk.Label(self.container, text="Doc. Identidad: ")
        lbl_doc.grid(row=5, column=0, sticky="w", padx=3, pady=3)
        self.txt_doc = tk.Entry(self.container)
        self.txt_doc.grid(row=5, column=1, sticky="ew", padx=3, pady=3)
        
        # Botones
        btn_aceptar = tk.Button(self.container, text="Aceptar", command=self.accion_aceptar)
        btn_aceptar.grid(row=6, column=0, padx=3, pady=3)
        
        btn_cancelar = tk.Button(self.container, text="Cancelar", command=self.destroy)
        btn_cancelar.grid(row=6, column=1, padx=3, pady=3)

    def accion_aceptar(self):
        try:
            fecha_str = self.txt_fecha.get()
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            
            nom = self.txt_nom.get()
            ape = self.txt_ape.get()
            doc_str = self.txt_doc.get()
            if not nom or not ape or not doc_str:
                raise ValueError("Campos vacíos")
            doc = int(doc_str)

            # Buscar habitación y actualizar
            for hab in self.hotel.lista_habitaciones:
                if hab.get_numero_habitacion() == self.numero_habitacion_reservada:
                    huesped = Huesped(nom, ape, doc)
                    huesped.set_fecha_ingreso(fecha)
                    hab.set_huesped(huesped)
                    hab.set_disponible(False)
                    break
            
            messagebox.showinfo("Mensaje", "El huésped ha sido registrado")
            self.destroy()

        except ValueError as e:
            if "format" in str(e) or "Rest" in str(e): # strptime error
                 messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado")
            else:
                 messagebox.showerror("Error", "Campo nulo o error en formato de numero")

# -----------------------------------------------------------------------------
# Clase: VentanaSalida
# -----------------------------------------------------------------------------
class VentanaSalida(tk.Toplevel):
    def __init__(self, parent, hotel, numero_habitacion):
        super().__init__(parent)
        self.hotel = hotel
        self.numero_habitacion = numero_habitacion
        self.habitacion_ocupada = None
        
        # Obtener referencia a la habitacion ocupada
        for hab in self.hotel.lista_habitaciones:
            if hab.get_numero_habitacion() == self.numero_habitacion:
                self.habitacion_ocupada = hab
                break
                
        self.title("Salida huéspedes")
        self.geometry("260x260")
        self.resizable(False, False)
        
        self.inicio()

    def inicio(self):
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Habitacion
        tk.Label(self.container, text=f"Habitación: {self.numero_habitacion}").grid(row=0, column=0, sticky="w", padx=3, pady=3)
        
        # Fecha Ingreso
        fecha_ingreso_str = self.hotel.buscar_fecha_ingreso_habitacion(self.numero_habitacion)
        tk.Label(self.container, text=f"Fecha de ingreso: {fecha_ingreso_str}").grid(row=1, column=0, sticky="w", padx=3, pady=3)
        
        # Fecha Salida
        tk.Label(self.container, text="Fecha de salida (aaaa-mm-dd): ").grid(row=2, column=0, sticky="w", padx=3, pady=3)
        self.txt_salida = tk.Entry(self.container)
        self.txt_salida.grid(row=3, column=0, sticky="ew", padx=3, pady=3)
        
        # Boton Calcular
        self.btn_calcular = tk.Button(self.container, text="Calcular", command=self.accion_calcular)
        self.btn_calcular.grid(row=4, column=0, padx=3, pady=3)
        
        # Cantidad dias
        self.lbl_dias = tk.Label(self.container, text="Cantidad de días: ")
        self.lbl_dias.grid(row=5, column=0, sticky="w", padx=3, pady=3)
        
        # Total pago
        self.lbl_total = tk.Label(self.container, text="Total: $")
        self.lbl_total.grid(row=6, column=0, sticky="w", padx=3, pady=3)
        
        # Registrar Salida
        self.btn_registrar = tk.Button(self.container, text="RegistrarSalida", command=self.accion_registrar, state="disabled")
        self.btn_registrar.grid(row=7, column=0, padx=3, pady=3)

    def accion_calcular(self):
        try:
            fecha_salida_str = self.txt_salida.get()
            fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d")
            
            # Establecer fecha salida en huesped
            huesped = self.habitacion_ocupada.get_huesped()
            huesped.set_fecha_salida(fecha_salida)
            
            if huesped.get_fecha_ingreso() < fecha_salida:
                dias = huesped.obtener_dias_alojamiento()
                print(dias)
                valor = dias * self.habitacion_ocupada.get_precio_dia()
                
                self.lbl_dias.config(text=f"Cantidad de días: {dias}")
                self.lbl_total.config(text=f"Total: ${valor}")
                self.btn_registrar.config(state="normal")
            else:
                 messagebox.showerror("Mensaje", "La fecha de salida es menor que la de ingreso")

        except ValueError:
             messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado")

    def accion_registrar(self):
        # Liberar habitacion
        self.habitacion_ocupada.set_huesped(None)
        self.habitacion_ocupada.set_disponible(True)
        
        messagebox.showinfo("Mensaje", "Se ha registrado la salida del huésped")
        self.destroy()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    hotel = Hotel()
    app = VentanaPrincipal(hotel)
    app.mainloop()
