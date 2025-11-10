import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

import gimnasio_modelo as gc

ventana_principal = tk.Tk()
ventana_principal.title("GIMNASIO")
ventana_principal.geometry("800x600")
ventana_principal.resizable(0,0)
principal = ttk.Notebook(ventana_principal)
principal.pack(fill='both', expand=True, padx=10, pady=10)

# --- Pestaña Socios ---
socio_frame = ttk.Frame(principal)
principal.add(socio_frame, text="socio")

def registrar_nuevo_socio():
    """Captura datos del formulario y crea un nuevo objeto Socio."""
    nombre = entry_nombre.get()
    dni = entry_dni.get()
    direccion = entry_direccion.get()
    fecha_nac = entry_fecha_nac.get()
    telefono = entry_telefono.get()
    email = entry_email.get()
    talle = entry_talle.get()
    peso = entry_peso.get()
    objetivo = entry_objetivo.get()

    # Validación simple
    if not all([nombre, dni, direccion, fecha_nac, telefono, email, talle, peso, objetivo]):
        messagebox.showerror("Error de validación", "Todos los campos son obligatorios.")
        return

    # Aquí crearías el objeto y lo guardarías (por ahora solo imprimimos)
    # nuevo_socio = gc.Socio(...)
    print("Registrando nuevo socio:")
    print(f"  Nombre: {nombre}, DNI: {dni}, Dirección: {direccion}")
    print(f"  Nacimiento: {fecha_nac}, Teléfono: {telefono}, Email: {email}")
    print(f"  Talle: {talle}, Peso: {peso}, Objetivo: {objetivo}")
    
    messagebox.showinfo("Registro Exitoso", f"Socio {nombre} registrado correctamente.")
    
    # Limpiar campos del formulario
    for entry in [entry_nombre, entry_dni, entry_direccion, entry_fecha_nac, entry_telefono, entry_email, entry_talle, entry_peso, entry_objetivo]:
        entry.delete(0, tk.END)

# --- Formulario de Registro de Socios ---
form_frame = ttk.LabelFrame(socio_frame, text="Registrar Nuevo Socio", padding=(20, 10))
form_frame.pack(padx=10, pady=10, fill="x")

# Creación de etiquetas y campos de entrada
labels = ["Nombre y Apellido:", "DNI:", "Dirección:", "Fecha Nacimiento (DD/MM/AAAA):", "Teléfono:", "Email:", "Talle:", "Peso (kg):", "Objetivo:"]
entries = []

for i, label_text in enumerate(labels):
    label = ttk.Label(form_frame, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
    entry = ttk.Entry(form_frame)
    entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
    entries.append(entry)

# Asignar variables a los campos de entrada para fácil acceso
(entry_nombre, entry_dni, entry_direccion, entry_fecha_nac, 
 entry_telefono, entry_email, entry_talle, entry_peso, entry_objetivo) = entries

# Configurar la columna de los campos de entrada para que se expanda
form_frame.columnconfigure(1, weight=1)

# Botón de registro
btn_registrar = ttk.Button(socio_frame, text="Registrar Socio", command=registrar_nuevo_socio)
btn_registrar.pack(pady=10)

# --- Otras Pestañas ---
instructor_frame = ttk.Frame(principal)
principal.add(instructor_frame, text="instructor")
clases_frame = ttk.Frame(principal)
principal.add(clases_frame, text="clases")
horarios_frame = ttk.Frame(principal)
principal.add(horarios_frame, text="horarios")
equipamiento_frame = ttk.Frame(principal)
principal.add(equipamiento_frame, text="equipamiento")
rutina_frame = ttk.Frame(principal)
principal.add(rutina_frame, text="rutina")
ventana_principal.mainloop()
