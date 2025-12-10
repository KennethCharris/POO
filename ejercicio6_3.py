import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# -----------------------------------------------------------------------------
# Clase: Contacto
# -----------------------------------------------------------------------------
class Contacto:
    """
    Esta clase denominada Contacto define un contacto para una agenda
    de contactos.
    """
    def __init__(self, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo):
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

# -----------------------------------------------------------------------------
# Clase: ListaContactos
# -----------------------------------------------------------------------------
class ListaContactos:
    """
    Esta clase denominada ListaContactos define una lista de objetos de
    tipo Contacto.
    """
    def __init__(self):
        self.lista = [] # Vector en Java, lista en Python

    def agregar_contacto(self, contacto):
        self.lista.append(contacto)

# -----------------------------------------------------------------------------
# Clase: VentanaContacto
# -----------------------------------------------------------------------------
class VentanaContacto(tk.Tk):
    """
    Esta clase denominada VentanaContacto crea una ventana que
    permite agregar un contacto.
    """
    def __init__(self):
        super().__init__()
        self.title("Detalles del contacto")
        # En JavaFX: Scene(grid, 600, 300)
        self.geometry("600x300")
        
        self.inicio()

    def inicio(self):
        # Establece un grid para los componentes gráficos
        # En JavaFX se usa GridPane. Aqui usamos Frame con grid() o directamente root.grid()
        # Usaremos un frame principal para dar padding como en el CSS del ejemplo
        
        main_frame = tk.Frame(self, padx=10, pady=10, highlightbackground="green", highlightcolor="green", highlightthickness=2)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Etiquetas
        tk.Label(main_frame, text="Nombres:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Label(main_frame, text="Apellidos:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Label(main_frame, text="Fecha nacimiento:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Label(main_frame, text="Dirección:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Label(main_frame, text="Teléfono:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tk.Label(main_frame, text="Correo:").grid(row=5, column=0, sticky="w", padx=5, pady=5)

        # Campos de texto
        self.campo_nombres = tk.Entry(main_frame)
        self.campo_nombres.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        self.campo_apellidos = tk.Entry(main_frame)
        self.campo_apellidos.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # DatePicker no existe nativo en Tkinter, usamos Entry
        self.campo_fecha_nacimiento = tk.Entry(main_frame) 
        # Placeholder visual o tooltip seria ideal, pero mantengamos simpleza
        self.campo_fecha_nacimiento.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        self.campo_direccion = tk.Entry(main_frame)
        self.campo_direccion.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        self.campo_telefono = tk.Entry(main_frame)
        self.campo_telefono.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        
        self.campo_correo = tk.Entry(main_frame)
        self.campo_correo.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        # Lista (ListView) -> Listbox
        self.lista_view = tk.Listbox(main_frame)
        # grid.add(lista, 2, 0, 1, 7) -> row=0, col=2, rowspan=7
        self.lista_view.grid(row=0, column=2, rowspan=7, sticky="nsew", padx=5, pady=5)

        # Botón
        self.agregar = tk.Button(main_frame, text="Agregar", command=self.mostrar_datos)
        # grid.add(buttonBox, 0, 6, 1, 2) -> row=6, col=0, colspan=2 (ya que buttonBox contiene el boton)
        # En Tkinter el boton se estira si usamos sticky ew
        self.agregar.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # Configurar pesos para que se estire bonito
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)

    def mostrar_datos(self):
        # Captura los datos ingresados
        a = self.campo_nombres.get()
        b = self.campo_apellidos.get()
        c_str = self.campo_fecha_nacimiento.get() # Es string en Entry
        d = self.campo_direccion.get()
        e = self.campo_telefono.get()
        f = self.campo_correo.get()

        # Evalua que los campos no estén vacíos
        if not a or not b or not c_str or not d or not e or not f:
            messagebox.showinfo("Mensaje", "No se permiten campos vacíos")
            # Nota: En el codigo Java dice setHeaderText("Error en ingreso de datos")... 
            # Tkinter messagebox simple no tiene header text separado del titulo y contenido tan claro.
        else:
            # Intentar parsear fecha para mantener fidelidad con lógica de DatePicker que devuelve objeto fecha
            # Aunque en Tkinter Entry devuelve string.
            try:
                # Asumimos formato yyyy-mm-dd si es texto manual, o simplemente guardamos string si fallase
                # Pero el ejercicio Java usa LocalDate.
                # Trataremos de parsear para simular el objeto fecha
                c = datetime.strptime(c_str, "%Y-%m-%d").date() # LocalDate equivalente
            except ValueError:
                # Si falla, simplemente lo dejamos como string o lanzamos error?
                # El ejercicio original usa un DatePicker que garantiza fecha valida (o null).
                # Aqui alertamos si no es fecha valida para ser estrictos.
                if c_str: 
                     # Si no esta vacio pero fallo parseo... asumiremos que es texto libre para no complicar 
                     # al usuario de tkinter sin DatePicker, O lanzamos error.
                     # Vamos a ser flexibles:
                     c = c_str 

            # Crear contacto
            contacto = Contacto(a, b, c, d, e, f)
            
            # Agregar a lista lógica
            lista_contactos = ListaContactos() # Se crea nueva en cada click según el código Java?
            # SI: "ListaContactos listaContactos = new ListaContactos();" dentro del else.
            # Esto parece un error lógico del ejemplo Java original (perdería los anteriores), 
            # pero la instrucción dice "siguiendo al pie de la letra".
            lista_contactos.agregar_contacto(contacto)
            
            # Agregar a lista gráfica
            data = f"{a}-{b}-{c}-{d}-{e}-{f}"
            self.lista_view.insert(tk.END, data)
            
            # Limpiar campos
            self.campo_nombres.delete(0, tk.END)
            self.campo_apellidos.delete(0, tk.END)
            self.campo_fecha_nacimiento.delete(0, tk.END)
            self.campo_direccion.delete(0, tk.END)
            self.campo_telefono.delete(0, tk.END)
            self.campo_correo.delete(0, tk.END)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app = VentanaContacto()
    app.mainloop()
