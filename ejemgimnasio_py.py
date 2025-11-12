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

def mostrar_formulario_alta():
    """Muestra el formulario de registro y oculta el botón 'Alta'."""
    btn_alta_socio.pack_forget()
    form_frame.pack(padx=10, pady=10, fill="x")
    btn_registrar.pack(pady=10)
    btn_cancelar.pack(pady=5)

def ocultar_formulario_alta():
    """Oculta el formulario de registro y vuelve a mostrar el botón 'Alta'."""
    form_frame.pack_forget()
    btn_registrar.pack_forget()
    btn_cancelar.pack_forget()
    btn_alta_socio.pack(pady=20)


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
    
    ocultar_formulario_alta()

# --- Formulario de Registro de Socios ---
# Se crea el frame del formulario pero no se muestra inicialmente (sin .pack())
form_frame = ttk.LabelFrame(socio_frame, text="Registrar Nuevo Socio", padding=(20, 10))

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

# --- Botones ---
# Botón principal para mostrar el formulario
btn_alta_socio = ttk.Button(socio_frame, text="Alta Socio", command=mostrar_formulario_alta)
btn_alta_socio.pack(pady=20)

# Botones del formulario (se crean pero no se muestran)
btn_registrar = ttk.Button(socio_frame, text="Registrar Socio", command=registrar_nuevo_socio)
btn_cancelar = ttk.Button(socio_frame, text="Cancelar", command=ocultar_formulario_alta)

# --- Otras Pestañas ---

# --- Pestaña Instructor ---
instructor_frame = ttk.Frame(principal)
principal.add(instructor_frame, text="instructor")

instructores_creados = []

def actualizar_vista_instructores():
    """Limpia y actualiza la tabla de instructores."""
    for item in tree_instructores.get_children():
        tree_instructores.delete(item)
    for inst in instructores_creados:
        tree_instructores.insert("", tk.END, values=(inst.id_instructor, inst.nombre, inst.telefono, inst.sueldo))

def mostrar_form_alta_instructor():
    """Muestra el formulario para dar de alta un instructor."""
    btn_alta_instructor.pack_forget()
    vista_instructores_frame.pack_forget()
    form_alta_instructor_frame.pack(padx=10, pady=10, fill="x")

def ocultar_form_alta_instructor():
    """Oculta el formulario de alta y muestra la vista principal."""
    form_alta_instructor_frame.pack_forget()
    btn_alta_instructor.pack(pady=10)
    vista_instructores_frame.pack(padx=10, pady=10, fill="both", expand=True)

def guardar_nuevo_instructor():
    """Guarda un nuevo instructor y actualiza la vista."""
    nombre = entry_instructor_nombre.get()
    direccion = entry_instructor_direccion.get()
    telefono = entry_instructor_telefono.get()
    sueldo = entry_instructor_sueldo.get()

    if not all([nombre, direccion, telefono, sueldo]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    id_instructor = len(instructores_creados) + 1
    nuevo_instructor = gc.instructor(id_instructor, nombre, direccion, telefono, sueldo)
    instructores_creados.append(nuevo_instructor)

    messagebox.showinfo("Éxito", f"Instructor {nombre} registrado correctamente.")
    print(f"Nuevo instructor registrado: ID={nuevo_instructor.id_instructor}, Nombre={nuevo_instructor.nombre}")

    for entry in [entry_instructor_nombre, entry_instructor_direccion, entry_instructor_telefono, entry_instructor_sueldo]:
        entry.delete(0, tk.END)
    ocultar_form_alta_instructor()
    actualizar_vista_instructores()

# --- Botón y Formulario de Alta de Instructores ---
btn_alta_instructor = ttk.Button(instructor_frame, text="Alta Instructor", command=mostrar_form_alta_instructor)
btn_alta_instructor.pack(pady=10)

form_alta_instructor_frame = ttk.LabelFrame(instructor_frame, text="Registrar Nuevo Instructor", padding=(20, 10))
labels_instructor = {"Nombre:": 0, "Dirección:": 1, "Teléfono:": 2, "Sueldo:": 3}
entry_instructor_nombre = ttk.Entry(form_alta_instructor_frame)
entry_instructor_direccion = ttk.Entry(form_alta_instructor_frame)
entry_instructor_telefono = ttk.Entry(form_alta_instructor_frame)
entry_instructor_sueldo = ttk.Entry(form_alta_instructor_frame)

for i, (text, widget) in enumerate(zip(labels_instructor.keys(), [entry_instructor_nombre, entry_instructor_direccion, entry_instructor_telefono, entry_instructor_sueldo])):
    ttk.Label(form_alta_instructor_frame, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

form_alta_instructor_frame.columnconfigure(1, weight=1)
btn_guardar_instructor = ttk.Button(form_alta_instructor_frame, text="Guardar Instructor", command=guardar_nuevo_instructor)
btn_guardar_instructor.grid(row=4, column=0, columnspan=2, pady=10)
btn_cancelar_instructor = ttk.Button(form_alta_instructor_frame, text="Cancelar", command=ocultar_form_alta_instructor)
btn_cancelar_instructor.grid(row=5, column=0, columnspan=2, pady=5)

# --- Vista de Instructores Registrados ---
vista_instructores_frame = ttk.LabelFrame(instructor_frame, text="Instructores Registrados", padding=(10, 5))
vista_instructores_frame.pack(padx=10, pady=10, fill="both", expand=True)

columns_inst = ('id', 'nombre', 'telefono', 'sueldo')
tree_instructores = ttk.Treeview(vista_instructores_frame, columns=columns_inst, show='headings')
tree_instructores.heading('id', text='ID')
tree_instructores.heading('nombre', text='Nombre')
tree_instructores.heading('telefono', text='Teléfono')
tree_instructores.heading('sueldo', text='Sueldo')
tree_instructores.column('id', width=50, anchor=tk.CENTER)
tree_instructores.pack(fill="both", expand=True)

# --- Pestaña Clases ---
clases_frame = ttk.Frame(principal)
principal.add(clases_frame, text="clases")

clases_creadas = []

def actualizar_vista_clases():
    """Limpia y actualiza la tabla de clases."""
    for item in tree_clases.get_children():
        tree_clases.delete(item)
    for c in clases_creadas:
        instructor_nombre = c.instructor.nombre if hasattr(c, 'instructor') else "No asignado"
        tree_clases.insert("", tk.END, values=(c.id_clase, c.tipo, c.capacidad, instructor_nombre))

def actualizar_comboboxes_asignacion():
    """Actualiza los comboboxes de la sección de asignación."""
    combo_asignar_clase['values'] = [f"ID {c.id_clase}: {c.tipo}" for c in clases_creadas]
    combo_asignar_instructor['values'] = [f"ID {i.id_instructor}: {i.nombre}" for i in instructores_creados]
    combo_asignar_horario['values'] = [f"ID {h.id_dias}: {h.dia_semana} ({h.hora_inicio}-{h.hora_final})" for h in horarios_creados]

def mostrar_form_crear_clase():
    btn_crear_clase.pack_forget()
    form_crear_clase_frame.pack(padx=10, pady=10, fill="x")

def ocultar_form_crear_clase():
    form_crear_clase_frame.pack_forget()
    btn_crear_clase.pack(pady=10)

def guardar_nueva_clase():
    tipo = entry_clase_tipo.get()
    capacidad = entry_clase_capacidad.get()
    nombres = entry_clase_nombres.get()

    if not all([tipo, capacidad, nombres]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    id_clase = len(clases_creadas) + 1
    nueva_clase = gc.clases(id_clase, tipo, capacidad, nombres)
    clases_creadas.append(nueva_clase)

    messagebox.showinfo("Éxito", f"Clase '{tipo}' creada correctamente.")
    for entry in [entry_clase_tipo, entry_clase_capacidad, entry_clase_nombres]:
        entry.delete(0, tk.END)
    ocultar_form_crear_clase()
    actualizar_vista_clases()
    actualizar_comboboxes_asignacion()

def asignar_instructor_a_clase():
    clase_sel = combo_asignar_clase.get()
    instructor_sel = combo_asignar_instructor.get()

    if not all([clase_sel, instructor_sel]):
        messagebox.showerror("Error", "Debe seleccionar una clase y un instructor.")
        return

    id_clase = int(clase_sel.split(":")[0].replace("ID ", ""))
    id_instructor = int(instructor_sel.split(":")[0].replace("ID ", ""))

    clase_obj = next((c for c in clases_creadas if c.id_clase == id_clase), None)
    instructor_obj = next((i for i in instructores_creados if i.id_instructor == id_instructor), None)

    if clase_obj and instructor_obj:
        clase_obj.agregar_instructor(instructor_obj)
        messagebox.showinfo("Éxito", f"Instructor '{instructor_obj.nombre}' asignado a la clase '{clase_obj.tipo}'.")
        actualizar_vista_clases()
    else:
        messagebox.showerror("Error", "No se encontró la clase o el instructor.")

# --- Widgets de la Pestaña Clases ---
btn_crear_clase = ttk.Button(clases_frame, text="Crear Nueva Clase", command=mostrar_form_crear_clase)
btn_crear_clase.pack(pady=10)

form_crear_clase_frame = ttk.LabelFrame(clases_frame, text="Crear Clase", padding=(20, 10))
entry_clase_tipo = ttk.Entry(form_crear_clase_frame)
entry_clase_capacidad = ttk.Entry(form_crear_clase_frame)
entry_clase_nombres = ttk.Entry(form_crear_clase_frame)

for i, (text, widget) in enumerate(zip(["Tipo:", "Capacidad:", "Nombre:"], [entry_clase_tipo, entry_clase_capacidad, entry_clase_nombres])):
    ttk.Label(form_crear_clase_frame, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

form_crear_clase_frame.columnconfigure(1, weight=1)
btn_guardar_clase = ttk.Button(form_crear_clase_frame, text="Guardar Clase", command=guardar_nueva_clase).grid(row=3, column=0, columnspan=2, pady=10)
btn_cancelar_clase = ttk.Button(form_crear_clase_frame, text="Cancelar", command=ocultar_form_crear_clase).grid(row=4, column=0, columnspan=2, pady=5)

vista_clases_frame = ttk.LabelFrame(clases_frame, text="Clases Disponibles", padding=(10, 5))
vista_clases_frame.pack(padx=10, pady=10, fill="both", expand=True)

columns_clases = ('id', 'tipo', 'capacidad', 'instructor')
tree_clases = ttk.Treeview(vista_clases_frame, columns=columns_clases, show='headings')
tree_clases.heading('id', text='ID')
tree_clases.heading('tipo', text='Tipo')
tree_clases.heading('capacidad', text='Capacidad')
tree_clases.heading('instructor', text='Instructor Asignado')
tree_clases.column('id', width=50, anchor=tk.CENTER)
tree_clases.pack(fill="both", expand=True)

form_asignar_frame = ttk.LabelFrame(clases_frame, text="Asignar Instructor y Horario", padding=(20, 10))
form_asignar_frame.pack(padx=10, pady=10, fill="x")

ttk.Label(form_asignar_frame, text="Seleccionar Clase:").pack(pady=2)
combo_asignar_clase = ttk.Combobox(form_asignar_frame, state="readonly")
combo_asignar_clase.pack(pady=2, fill="x")

ttk.Label(form_asignar_frame, text="Asignar Instructor:").pack(pady=2)
combo_asignar_instructor = ttk.Combobox(form_asignar_frame, state="readonly")
combo_asignar_instructor.pack(pady=2, fill="x")

ttk.Label(form_asignar_frame, text="Asignar Horario:").pack(pady=2)
combo_asignar_horario = ttk.Combobox(form_asignar_frame, state="readonly")
combo_asignar_horario.pack(pady=2, fill="x")

btn_asignar = ttk.Button(form_asignar_frame, text="Asignar", command=asignar_instructor_a_clase)
btn_asignar.pack(pady=10)

# --- Pestaña Horarios ---
horarios_frame = ttk.Frame(principal)
principal.add(horarios_frame, text="horarios")

horarios_creados = []

def actualizar_vista_horarios():
    """Limpia y actualiza la tabla de horarios con los datos más recientes."""
    # Limpiar vista previa
    for item in tree_horarios.get_children():
        tree_horarios.delete(item)
    # Llenar con datos actualizados
    for h in horarios_creados:
        tree_horarios.insert("", tk.END, values=(h.id_dias, h.dia_semana, h.hora_inicio, h.hora_final))

def mostrar_form_crear_horario():
    """Muestra el formulario para crear un nuevo horario."""
    btn_crear_horario.pack_forget()
    form_crear_horario_frame.pack(padx=10, pady=10, fill="x")

def ocultar_form_crear_horario():
    """Oculta el formulario de creación y vuelve a mostrar el botón principal."""
    form_crear_horario_frame.pack_forget()
    btn_crear_horario.pack(pady=10)

def guardar_nuevo_horario():
    """Guarda un nuevo horario y actualiza la vista."""
    dia = combo_horario_dia.get()
    inicio = entry_horario_inicio.get()
    fin = entry_horario_fin.get()

    if not all([dia, inicio, fin]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    id_horario = len(horarios_creados) + 1
    nuevo_horario = gc.horarios(id_horario, dia, inicio, fin)
    horarios_creados.append(nuevo_horario)

    messagebox.showinfo("Éxito", f"Horario para el {dia} de {inicio} a {fin} creado.")
    print(f"Nuevo horario creado: ID={nuevo_horario.id_dias}, Día={nuevo_horario.dia_semana}")

    entry_horario_inicio.delete(0, tk.END)
    entry_horario_fin.delete(0, tk.END)
    ocultar_form_crear_horario()
    actualizar_vista_horarios()

# --- Botón y Formulario de Creación de Horarios ---
btn_crear_horario = ttk.Button(horarios_frame, text="Crear Nuevo Horario", command=mostrar_form_crear_horario)
btn_crear_horario.pack(pady=10)

form_crear_horario_frame = ttk.LabelFrame(horarios_frame, text="Crear Horario", padding=(20, 10))
ttk.Label(form_crear_horario_frame, text="Día de la semana:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
combo_horario_dia = ttk.Combobox(form_crear_horario_frame, values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"], state="readonly")
combo_horario_dia.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
ttk.Label(form_crear_horario_frame, text="Hora de Inicio (HH:MM):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_horario_inicio = ttk.Entry(form_crear_horario_frame)
entry_horario_inicio.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
ttk.Label(form_crear_horario_frame, text="Hora de Fin (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_horario_fin = ttk.Entry(form_crear_horario_frame)
entry_horario_fin.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
form_crear_horario_frame.columnconfigure(1, weight=1)
btn_guardar_horario = ttk.Button(form_crear_horario_frame, text="Guardar Horario", command=guardar_nuevo_horario)
btn_guardar_horario.grid(row=3, column=0, columnspan=2, pady=10)
btn_cancelar_horario = ttk.Button(form_crear_horario_frame, text="Cancelar", command=ocultar_form_crear_horario)
btn_cancelar_horario.grid(row=4, column=0, columnspan=2, pady=5)

# --- Vista de Horarios Creados ---
vista_horarios_frame = ttk.LabelFrame(horarios_frame, text="Horarios Programados", padding=(10, 5))
vista_horarios_frame.pack(padx=10, pady=10, fill="both", expand=True)

columns = ('id', 'dia', 'inicio', 'fin')
tree_horarios = ttk.Treeview(vista_horarios_frame, columns=columns, show='headings')
tree_horarios.heading('id', text='ID')
tree_horarios.heading('dia', text='Día')
tree_horarios.heading('inicio', text='Hora Inicio')
tree_horarios.heading('fin', text='Hora Fin')
tree_horarios.column('id', width=50, anchor=tk.CENTER)
tree_horarios.pack(fill="both", expand=True)

# --- Pestaña Equipamiento ---
equipamiento_frame = ttk.Frame(principal)
principal.add(equipamiento_frame, text="equipamiento")

equipos_creados = []

def actualizar_combobox_equipos():
    """Actualiza la lista de equipos en el Combobox de gestión."""
    nombres_equipos = [f"ID {e.id_equipamiento}: {e.tipo_maquina}" for e in equipos_creados]
    combo_equipos_gestion['values'] = nombres_equipos
    if nombres_equipos:
        combo_equipos_gestion.current(0)

def mostrar_form_agregar_equipo():
    """Muestra el formulario para agregar un nuevo equipo."""
    btn_agregar_equipo.pack_forget()
    form_agregar_equipo_frame.pack(padx=10, pady=10, fill="x")
    form_gestionar_equipo_frame.pack_forget()

def ocultar_form_agregar_equipo():
    """Oculta el formulario de agregación y muestra los otros widgets."""
    form_agregar_equipo_frame.pack_forget()
    btn_agregar_equipo.pack(pady=10)
    form_gestionar_equipo_frame.pack(padx=10, pady=10, fill="x", expand=True)

def guardar_nuevo_equipo():
    """Crea un nuevo objeto equipamiento y lo guarda."""
    tipo_maquina = entry_equipo_tipo.get()
    capacidad = entry_equipo_capacidad.get()
    musculos = entry_equipo_musculos.get()
    estado = combo_equipo_estado.get()

    if not all([tipo_maquina, capacidad, musculos, estado]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    id_equipo = len(equipos_creados) + 1
    nuevo_equipo = gc.equipamiento(id_equipo, capacidad, tipo_maquina, musculos, estado)
    equipos_creados.append(nuevo_equipo)

    messagebox.showinfo("Éxito", f"Equipo '{tipo_maquina}' agregado correctamente.")
    print(f"Nuevo equipo agregado: ID={nuevo_equipo.id_equipamiento}, Tipo={nuevo_equipo.tipo_maquina}, Estado={nuevo_equipo.estado}")

    for entry in [entry_equipo_tipo, entry_equipo_capacidad, entry_equipo_musculos]:
        entry.delete(0, tk.END)
    ocultar_form_agregar_equipo()
    actualizar_combobox_equipos()

def actualizar_estado_equipo():
    """Actualiza el estado (habilita/deshabilita) de un equipo seleccionado."""
    seleccion = combo_equipos_gestion.get()
    nuevo_estado = combo_estado_gestion.get()

    if not seleccion or not nuevo_estado:
        messagebox.showerror("Error", "Debe seleccionar un equipo y un nuevo estado.")
        return

    id_equipo_sel = int(seleccion.split(":")[0].replace("ID ", ""))
    equipo_encontrado = next((e for e in equipos_creados if e.id_equipamiento == id_equipo_sel), None)

    if equipo_encontrado:
        equipo_encontrado.habilitar_deshabilitar(nuevo_estado)
        messagebox.showinfo("Éxito", f"El estado de '{equipo_encontrado.tipo_maquina}' ha sido actualizado a '{nuevo_estado}'.")
        print(f"Equipo ID {equipo_encontrado.id_equipamiento} actualizado. Nuevo estado: {equipo_encontrado.estado}")
    else:
        messagebox.showerror("Error", "No se encontró el equipo seleccionado.")

# --- Botón principal y formularios de Equipamiento ---
btn_agregar_equipo = ttk.Button(equipamiento_frame, text="Agregar Equipamiento", command=mostrar_form_agregar_equipo)
btn_agregar_equipo.pack(pady=10)

form_agregar_equipo_frame = ttk.LabelFrame(equipamiento_frame, text="Agregar Nuevo Equipamiento", padding=(20, 10))
labels_equipo = {"Tipo de Máquina:": 0, "Capacidad:": 1, "Músculos que trabaja:": 2, "Estado Inicial:": 3}
entry_equipo_tipo = ttk.Entry(form_agregar_equipo_frame)
entry_equipo_capacidad = ttk.Entry(form_agregar_equipo_frame)
entry_equipo_musculos = ttk.Entry(form_agregar_equipo_frame)
combo_equipo_estado = ttk.Combobox(form_agregar_equipo_frame, values=["Habilitado", "Deshabilitado"], state="readonly")

for i, (text, widget) in enumerate(zip(labels_equipo.keys(), [entry_equipo_tipo, entry_equipo_capacidad, entry_equipo_musculos, combo_equipo_estado])):
    ttk.Label(form_agregar_equipo_frame, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

form_agregar_equipo_frame.columnconfigure(1, weight=1)
btn_guardar_equipo = ttk.Button(form_agregar_equipo_frame, text="Guardar Equipo", command=guardar_nuevo_equipo)
btn_guardar_equipo.grid(row=4, column=0, columnspan=2, pady=10)
btn_cancelar_equipo = ttk.Button(form_agregar_equipo_frame, text="Cancelar", command=ocultar_form_agregar_equipo)
btn_cancelar_equipo.grid(row=5, column=0, columnspan=2, pady=5)

form_gestionar_equipo_frame = ttk.LabelFrame(equipamiento_frame, text="Gestionar Equipamiento", padding=(20, 10))
form_gestionar_equipo_frame.pack(padx=10, pady=10, fill="x", expand=True)

ttk.Label(form_gestionar_equipo_frame, text="Seleccionar Equipo:").pack(pady=5)
combo_equipos_gestion = ttk.Combobox(form_gestionar_equipo_frame, state="readonly")
combo_equipos_gestion.pack(pady=5, fill="x")

ttk.Label(form_gestionar_equipo_frame, text="Cambiar Estado a:").pack(pady=5)
combo_estado_gestion = ttk.Combobox(form_gestionar_equipo_frame, values=["Habilitado", "Deshabilitado"], state="readonly")
combo_estado_gestion.pack(pady=5, fill="x")

btn_actualizar_estado = ttk.Button(form_gestionar_equipo_frame, text="Actualizar Estado", command=actualizar_estado_equipo)
btn_actualizar_estado.pack(pady=10)

# --- Pestaña Rutina ---
rutina_frame = ttk.Frame(principal)
principal.add(rutina_frame, text="rutina")

# --- Pestaña Rutina ---

# Lista para almacenar las rutinas creadas (simulación en memoria)
rutinas_creadas = []

def actualizar_combobox_rutinas():
    """Actualiza la lista de rutinas en el Combobox."""
    nombres_rutinas = [f"ID {r.id_rutina}: {r.tipo}" for r in rutinas_creadas]
    combo_rutinas['values'] = nombres_rutinas
    if nombres_rutinas:
        combo_rutinas.current(0)

def mostrar_form_crear_rutina():
    """Muestra el formulario para crear una nueva rutina."""
    btn_crear_rutina.pack_forget()
    form_crear_rutina_frame.pack(padx=10, pady=10, fill="x")
    form_asignar_ejercicio_frame.pack_forget() # Ocultar el otro form

def ocultar_form_crear_rutina():
    """Oculta el formulario de creación de rutinas."""
    form_crear_rutina_frame.pack_forget()
    btn_crear_rutina.pack(pady=10)
    form_asignar_ejercicio_frame.pack(padx=10, pady=10, fill="x", expand=True) # Volver a mostrar

def guardar_nueva_rutina():
    """Crea un nuevo objeto rutina y lo guarda."""
    tipo = entry_rutina_tipo.get()
    duracion = entry_rutina_duracion.get()
    ejercicio_inicial = entry_rutina_ejercicio.get()

    if not all([tipo, duracion, ejercicio_inicial]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    
    # Simular un ID único para la rutina
    id_rutina = len(rutinas_creadas) + 1
    nueva_rutina = gc.rutina(id_rutina, tipo, duracion)
    
    # Asignar el ejercicio inicial
    nueva_rutina.asignar_ejercicio(ejercicio_inicial)
    
    rutinas_creadas.append(nueva_rutina)

    print(f"Nueva rutina creada: ID={nueva_rutina.id_rutina}, Tipo={nueva_rutina.tipo}, Ejercicios: {nueva_rutina.ejercicios}")
    messagebox.showinfo("Éxito", f"Rutina '{tipo}' creada correctamente.")

    # Limpiar campos y ocultar formulario
    entry_rutina_tipo.delete(0, tk.END)
    entry_rutina_duracion.delete(0, tk.END)
    entry_rutina_ejercicio.delete(0, tk.END)
    ocultar_form_crear_rutina()
    actualizar_combobox_rutinas()

def asignar_ejercicio_a_rutina():
    """Asigna un nuevo ejercicio a la rutina seleccionada en el Combobox."""
    seleccion = combo_rutinas.get()
    nuevo_ejercicio = entry_nuevo_ejercicio.get()

    if not seleccion or not nuevo_ejercicio:
        messagebox.showerror("Error", "Debe seleccionar una rutina y escribir un ejercicio.")
        return

    # Encontrar la rutina seleccionada en la lista rutinas_creadas
    id_rutina_seleccionada = int(seleccion.split(":")[0].replace("ID ", ""))
    rutina_encontrada = None
    for r in rutinas_creadas:
        if r.id_rutina == id_rutina_seleccionada:
            rutina_encontrada = r
            break
    
    if rutina_encontrada:
        rutina_encontrada.asignar_ejercicio(nuevo_ejercicio)
        messagebox.showinfo("Éxito", f"Ejercicio '{nuevo_ejercicio}' asignado a la rutina '{rutina_encontrada.tipo}'.")
        entry_nuevo_ejercicio.delete(0, tk.END)
        print(f"Rutina ID {rutina_encontrada.id_rutina} actualizada. Ejercicios: {rutina_encontrada.ejercicios}")
    else:
        messagebox.showerror("Error", "No se encontró la rutina seleccionada.")

# --- Botón principal para crear rutina ---
btn_crear_rutina = ttk.Button(rutina_frame, text="Crear Rutina", command=mostrar_form_crear_rutina)
btn_crear_rutina.pack(pady=10)

# --- Formulario para Crear Rutina (inicialmente oculto) ---
form_crear_rutina_frame = ttk.LabelFrame(rutina_frame, text="Crear Nueva Rutina", padding=(20, 10))

ttk.Label(form_crear_rutina_frame, text="Tipo de Rutina:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_rutina_tipo = ttk.Entry(form_crear_rutina_frame)
entry_rutina_tipo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(form_crear_rutina_frame, text="Duración:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_rutina_duracion = ttk.Entry(form_crear_rutina_frame)
entry_rutina_duracion.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(form_crear_rutina_frame, text="Ejercicio Inicial:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_rutina_ejercicio = ttk.Entry(form_crear_rutina_frame)
entry_rutina_ejercicio.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

form_crear_rutina_frame.columnconfigure(1, weight=1)

btn_guardar_rutina = ttk.Button(form_crear_rutina_frame, text="Guardar Rutina", command=guardar_nueva_rutina)
btn_guardar_rutina.grid(row=3, column=0, columnspan=2, pady=10)

btn_cancelar_rutina = ttk.Button(form_crear_rutina_frame, text="Cancelar", command=ocultar_form_crear_rutina)
btn_cancelar_rutina.grid(row=4, column=0, columnspan=2, pady=5)

# --- Formulario para Asignar Ejercicio ---
form_asignar_ejercicio_frame = ttk.LabelFrame(rutina_frame, text="Asignar Ejercicio a Rutina", padding=(20, 10))
form_asignar_ejercicio_frame.pack(padx=10, pady=10, fill="x", expand=True)

ttk.Label(form_asignar_ejercicio_frame, text="Seleccionar Rutina:").pack(pady=5)
combo_rutinas = ttk.Combobox(form_asignar_ejercicio_frame, state="readonly")
combo_rutinas.pack(pady=5, fill="x")

ttk.Label(form_asignar_ejercicio_frame, text="Nuevo Ejercicio:").pack(pady=5)
entry_nuevo_ejercicio = ttk.Entry(form_asignar_ejercicio_frame)
entry_nuevo_ejercicio.pack(pady=5, fill="x")

btn_asignar_ejercicio = ttk.Button(form_asignar_ejercicio_frame, text="Asignar Ejercicio", command=asignar_ejercicio_a_rutina)
btn_asignar_ejercicio.pack(pady=10)

# --- Iniciar el bucle principal de la aplicación ---
ventana_principal.mainloop()