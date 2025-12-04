import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

from vista_clases import VistaClases
from vista_horarios import VistaHorarios
from vista_instructor import VistaInstructor
from vista_socio import VistaSocio
from vista_ejercicio import VistaEjercicio
from vista_equipamiento import VistaEquipamiento
from vista_rutina import VistaRutina

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GIMNASIO")
        
        # Centrar la ventana de login inicial
        self._centrar_ventana(500, 300)

        self.resizable(False, False)

        self.login_frame = ttk.Frame(self, padding="20")
        self.login_frame.pack(expand=True)

        self.crear_widgets_login()

    def _centrar_ventana(self, ancho, alto):
        """Método auxiliar para centrar la ventana en la pantalla."""
        self.update_idletasks()
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.geometry(f'{ancho}x{alto}+{x}+{y}')

    def crear_widgets_login(self):
        """Crea los widgets para el formulario de inicio de sesión."""
        ttk.Label(self.login_frame, text="Usuario:").pack(pady=5)
        self.usuario_entry = ttk.Entry(self.login_frame)
        self.usuario_entry.pack(pady=5)

        ttk.Label(self.login_frame, text="Contraseña:").pack(pady=5)
        self.contraseña_entry = ttk.Entry(self.login_frame, show="*")
        self.contraseña_entry.pack(pady=5)

        ttk.Button(self.login_frame, text="Iniciar Sesión", command=self.intentar_login).pack(pady=10)

    def intentar_login(self):
        """Verifica las credenciales del usuario contra la base de datos."""
        usuario = self.usuario_entry.get()
        contraseña = self.contraseña_entry.get()

        if not usuario or not contraseña:
            messagebox.showerror("Error de Login", "Usuario y contraseña no pueden estar vacíos.")
            return

        try:
            conn = sqlite3.connect('gimnasio.db')
            cursor = conn.cursor()
            cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario = ? AND contraseña = ?", (usuario, contraseña))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                rol = resultado[0]
                self.mostrar_ventana_principal(rol)
            else:
                messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo conectar a la base de datos: {e}")




    def mostrar_ventana_principal(self, rol):
        """Destruye la ventana de login y muestra la aplicación principal."""
        self.login_frame.destroy()
        
        # Centrar la ventana principal después del login
        self._centrar_ventana(800, 600)
        self.state('zoomed')
        self.resizable(True, True)
        self.title(f"GIMNASIO - Rol: {rol.capitalize()}")

        # Aquí es donde limitaremos las pestañas según el rol en el futuro.
        # Por ahora, mostramos todo.
        principal = ttk.Notebook(self)
        principal.pack(fill='both', expand=True, padx=10, pady=10)

        VistaSocio(principal)
        VistaInstructor(principal)
        VistaClases(principal)
        VistaEjercicio(principal)
        VistaHorarios(principal)
        VistaEquipamiento(principal)
        VistaRutina(principal)

        # --- Pestaña Salir ---
        salir_frame = ttk.Frame(principal)
        principal.add(salir_frame, text="Salir")

        def salir_aplicacion():
            """Muestra un cuadro de diálogo de confirmación y cierra la aplicación si se confirma."""
            if messagebox.askyesno("Salir", "¿Está seguro de que desea salir de la aplicación?"):
                self.destroy()

        # Configurar el frame para centrar el botón
        salir_frame.columnconfigure(0, weight=1)
        salir_frame.rowconfigure(0, weight=1)

        btn_salir = ttk.Button(salir_frame, text="Cerrar Aplicación", command=salir_aplicacion, style="Baja.TButton")
        btn_salir.grid(row=0, column=0, ipadx=30, ipady=15)







        style = ttk.Style()
        style.configure("Alta.TButton", foreground="black", background='green', font=("Arial", 12, "normal"))
        style.configure("Baja.TButton", foreground="black", background="red", font=("Arial", 12, "normal"))

        self.protocol("WM_DELETE_WINDOW", salir_aplicacion) # Captura el evento de cierre de la ventana

if __name__ == "__main__":
    app = App()
    app.mainloop()