import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from vista_clases import VistaClases
from vista_horarios import VistaHorarios
from vista_instructor import VistaInstructor
from vista_socio import VistaSocio
from vista_ejercicio import VistaEjercicio
from vista_equipamiento import VistaEquipamiento
from vista_rutina import VistaRutina

import gimnasio_modelo as gc


ventana_principal = tk.Tk()
ventana_principal.state('zoomed')
ventana_principal.title("GIMNASIO")
ventana_principal.geometry("800x600")
#ventana_principal.resizable(0,0)
principal = ttk.Notebook(ventana_principal)
principal.pack(fill='both', expand=True, padx=10, pady=10)

socio_frame = VistaSocio(principal)

instructor_frame = VistaInstructor(principal)

clases_frame = VistaClases(principal)

ejercicio_frame = VistaEjercicio(principal)

horarios_frame = VistaHorarios(principal)

equipamiento_frame = VistaEquipamiento(principal)

rutina_frame = VistaRutina(principal)

style = ttk.Style()
style.configure("Alta.TButton", foreground="white", bordercolor="green", relief="solid", font=("Arial", 12, "bold"))


ventana_principal.mainloop()