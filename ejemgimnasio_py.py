import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime
from tkinter import messagebox
from vista_clases import VistaClases
from vista_horarios import VistaHorarios
from vista_instructor import VistaInstructor
from vista_socio import VistaSocio
from vista_ejercicio import VistaEjercicio
from vista_equipamiento import VistaEquipamiento

import gimnasio_modelo as gc

ventana_principal = tk.Tk()
ventana_principal.title("GIMNASIO")
ventana_principal.geometry("800x600")
#ventana_principal.resizable(0,0)
principal = ttk.Notebook(ventana_principal)
principal.pack(fill='both', expand=True, padx=10, pady=10)

# --- Pestaña Socios ---
socio_frame = VistaSocio(principal)

# --- Pestaña Instructor ---
instructor_frame = VistaInstructor(principal)

#############################################
# --- Pestaña Clases ---

clases_frame_2 = VistaClases(principal)

ejercicio_frame_2 = VistaEjercicio(principal)

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

def borrar_clase_seleccionada():
    """Borra la clase seleccionada en la tabla Treeview."""
    selected_item = tree_clases.focus()
    if not selected_item:
        messagebox.showerror("Error", "Por favor, seleccione una clase para borrar.")
        return

    if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar la clase seleccionada?"):
        return

    item_values = tree_clases.item(selected_item, 'values')
    id_a_borrar = int(item_values[0])

    clase_a_borrar = next((c for c in clases_creadas if c.id_clase == id_a_borrar), None)
    
    if clase_a_borrar:
        clases_creadas.remove(clase_a_borrar)
        messagebox.showinfo("Éxito", f"Clase '{clase_a_borrar.tipo}' borrada correctamente.")
        actualizar_vista_clases()
        actualizar_comboboxes_asignacion()

def buscar_clases():
    """Filtra la tabla de clases según el término de búsqueda."""
    termino_busqueda = entry_buscar_clase.get().lower()

    for item in tree_clases.get_children():
        tree_clases.delete(item)

    if not termino_busqueda:
        actualizar_vista_clases()
        return

    for c in clases_creadas:
        instructor_nombre = c.instructor.nombre if hasattr(c, 'instructor') else ""
        if termino_busqueda in str(c.id_clase).lower() or \
           termino_busqueda in str(c.tipo).lower() or \
           termino_busqueda in str(c.capacidad).lower() or \
           termino_busqueda in instructor_nombre.lower():
            tree_clases.insert("", tk.END, values=(c.id_clase, c.tipo, c.capacidad, instructor_nombre))

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

search_frame_clases = ttk.Frame(vista_clases_frame)
search_frame_clases.pack(fill='x', padx=5, pady=5)

entry_buscar_clase = ttk.Entry(search_frame_clases)
entry_buscar_clase.pack(side='left', fill='x', expand=True)

btn_buscar_clase = ttk.Button(search_frame_clases, text="Buscar 🔎", command=buscar_clases)
btn_buscar_clase.pack(side='right', padx=(5, 0))

columns_clases = ('id', 'tipo', 'capacidad', 'instructor')
tree_clases = ttk.Treeview(vista_clases_frame, columns=columns_clases, show='headings')
tree_clases.heading('id', text='ID')
tree_clases.heading('tipo', text='Tipo')
tree_clases.heading('capacidad', text='Capacidad')
tree_clases.heading('instructor', text='Instructor Asignado')
tree_clases.column('id', width=50, anchor=tk.CENTER)
tree_clases.pack(fill="both", expand=True)

btn_borrar_clase = ttk.Button(vista_clases_frame, text="Borrar Clase Seleccionada", command=borrar_clase_seleccionada)
btn_borrar_clase.pack(pady=5)

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

#################################
horarios_frame_2 = VistaHorarios(principal)
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
    actualizar_comboboxes_asignacion() # Actualiza el combo en la pestaña Clases

def borrar_horario_seleccionado():
    """Borra el horario seleccionado en la tabla Treeview."""
    selected_item = tree_horarios.focus()
    if not selected_item:
        messagebox.showerror("Error", "Por favor, seleccione un horario para borrar.")
        return

    if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar el horario seleccionado?"):
        return

    item_values = tree_horarios.item(selected_item, 'values')
    id_a_borrar = int(item_values[0])

    horario_a_borrar = next((h for h in horarios_creados if h.id_dias == id_a_borrar), None)
    
    if horario_a_borrar:
        horarios_creados.remove(horario_a_borrar)
        messagebox.showinfo("Éxito", "Horario borrado correctamente.")
        actualizar_vista_horarios()

def buscar_horarios():
    """Filtra la tabla de horarios según el término de búsqueda."""
    termino_busqueda = entry_buscar_horario.get().lower()

    for item in tree_horarios.get_children():
        tree_horarios.delete(item)

    if not termino_busqueda:
        actualizar_vista_horarios()
        return

    for h in horarios_creados:
        if termino_busqueda in str(h.id_dias).lower() or \
           termino_busqueda in str(h.dia_semana).lower() or \
           termino_busqueda in str(h.hora_inicio).lower() or \
           termino_busqueda in str(h.hora_final).lower():
            tree_horarios.insert("", tk.END, values=(h.id_dias, h.dia_semana, h.hora_inicio, h.hora_final))

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

search_frame_horarios = ttk.Frame(vista_horarios_frame)
search_frame_horarios.pack(fill='x', padx=5, pady=5)

entry_buscar_horario = ttk.Entry(search_frame_horarios)
entry_buscar_horario.pack(side='left', fill='x', expand=True)

btn_buscar_horario = ttk.Button(search_frame_horarios, text="Buscar 🔎", command=buscar_horarios)
btn_buscar_horario.pack(side='right', padx=(5, 0))

columns = ('id', 'dia', 'inicio', 'fin')
tree_horarios = ttk.Treeview(vista_horarios_frame, columns=columns, show='headings')
tree_horarios.heading('id', text='ID')
tree_horarios.heading('dia', text='Día')
tree_horarios.heading('inicio', text='Hora Inicio')
tree_horarios.heading('fin', text='Hora Fin')
tree_horarios.column('id', width=50, anchor=tk.CENTER)
tree_horarios.pack(fill="both", expand=True)

btn_borrar_horario = ttk.Button(vista_horarios_frame, text="Borrar Horario Seleccionado", command=borrar_horario_seleccionado)
btn_borrar_horario.pack(pady=5)

############################################
# --- Pestaña Equipamiento ---
equipamiento_frame_2 = VistaEquipamiento(principal)

equipamiento_frame = ttk.Frame(principal)
principal.add(equipamiento_frame, text="equipamiento")

equipos_creados = []

def actualizar_vista_equipos():
    """Limpia y actualiza la tabla de equipos."""
    for item in tree_equipos.get_children():
        tree_equipos.delete(item)
    for eq in equipos_creados:
        tree_equipos.insert("", tk.END, values=(eq.id_equipamiento, eq.tipo_maquina, eq.musculos, eq.estado))
    
    # También actualiza el combo de la pestaña rutina si es necesario
    # (Aunque no se usa directamente, es buena práctica mantenerlo)
    nombres_equipos = [f"ID {e.id_equipamiento}: {e.tipo_maquina}" for e in equipos_creados]
    # combo_equipos_gestion['values'] = nombres_equipos


def mostrar_form_agregar_equipo():
    """Muestra el formulario para agregar un nuevo equipo."""
    btn_agregar_equipo.pack_forget()
    form_agregar_equipo_frame.pack(padx=10, pady=10, fill="x")
    vista_equipos_frame.pack_forget()

def ocultar_form_agregar_equipo():
    """Oculta el formulario de agregación y muestra los otros widgets."""
    form_agregar_equipo_frame.pack_forget()
    btn_agregar_equipo.pack(pady=10)
    vista_equipos_frame.pack(padx=10, pady=10, fill="both", expand=True)

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
    actualizar_vista_equipos()

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

def borrar_equipo_seleccionado():
    """Borra el equipo seleccionado en la tabla Treeview."""
    selected_item = tree_equipos.focus()
    if not selected_item:
        messagebox.showerror("Error", "Por favor, seleccione un equipo para borrar.")
        return

    if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar el equipo seleccionado?"):
        return

    item_values = tree_equipos.item(selected_item, 'values')
    id_a_borrar = int(item_values[0])

    equipo_a_borrar = next((eq for eq in equipos_creados if eq.id_equipamiento == id_a_borrar), None)
    
    if equipo_a_borrar:
        equipos_creados.remove(equipo_a_borrar)
        messagebox.showinfo("Éxito", f"Equipo '{equipo_a_borrar.tipo_maquina}' borrado correctamente.")
        actualizar_vista_equipos()

def buscar_equipos():
    """Filtra la tabla de equipos según el término de búsqueda."""
    termino_busqueda = entry_buscar_equipo.get().lower()

    for item in tree_equipos.get_children():
        tree_equipos.delete(item)

    if not termino_busqueda:
        actualizar_vista_equipos()
        return

    for eq in equipos_creados:
        if termino_busqueda in str(eq.id_equipamiento).lower() or \
           termino_busqueda in str(eq.tipo_maquina).lower() or \
           termino_busqueda in str(eq.musculos).lower() or \
           termino_busqueda in str(eq.estado).lower():
            tree_equipos.insert("", tk.END, values=(eq.id_equipamiento, eq.tipo_maquina, eq.musculos, eq.estado))

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

# --- Vista de Equipos Registrados ---
vista_equipos_frame = ttk.LabelFrame(equipamiento_frame, text="Equipos Registrados", padding=(10, 5))
vista_equipos_frame.pack(padx=10, pady=10, fill="both", expand=True)

search_frame_equipos = ttk.Frame(vista_equipos_frame)
search_frame_equipos.pack(fill='x', padx=5, pady=5)

entry_buscar_equipo = ttk.Entry(search_frame_equipos)
entry_buscar_equipo.pack(side='left', fill='x', expand=True)

btn_buscar_equipo = ttk.Button(search_frame_equipos, text="Buscar 🔎", command=buscar_equipos)
btn_buscar_equipo.pack(side='right', padx=(5, 0))

columns_equipos = ('id', 'tipo', 'musculos', 'estado')
tree_equipos = ttk.Treeview(vista_equipos_frame, columns=columns_equipos, show='headings')
tree_equipos.heading('id', text='ID')
tree_equipos.heading('tipo', text='Tipo de Máquina')
tree_equipos.heading('musculos', text='Músculos')
tree_equipos.heading('estado', text='Estado')
tree_equipos.column('id', width=50, anchor=tk.CENTER)
tree_equipos.pack(fill="both", expand=True)

btn_borrar_equipo = ttk.Button(vista_equipos_frame, text="Borrar Equipo Seleccionado", command=borrar_equipo_seleccionado)
btn_borrar_equipo.pack(pady=5)
#############################################################################
# --- Pestaña Rutina ---
rutina_frame = ttk.Frame(principal)
principal.add(rutina_frame, text="rutina")

rutinas_creadas = []

def actualizar_vista_rutinas():
    """Limpia y actualiza la tabla de rutinas."""
    for item in tree_rutinas.get_children():
        tree_rutinas.delete(item)
    for r in rutinas_creadas:
        # Contar ejercicios para mostrar en la tabla
        num_ejercicios = len(r.ejercicios)
        tree_rutinas.insert("", tk.END, values=(r.id_rutina, r.tipo, r.duracion, num_ejercicios))

def mostrar_form_crear_rutina():
    """Muestra el formulario para crear una nueva rutina."""
    btn_crear_rutina.pack_forget()
    vista_rutinas_frame.pack_forget()
    form_crear_rutina_frame.pack(padx=10, pady=10, fill="x")
    # form_asignar_ejercicio_frame.pack_forget() # Ocultar el otro form

def ocultar_form_crear_rutina():
    """Oculta el formulario de creación de rutinas."""
    form_crear_rutina_frame.pack_forget()
    btn_crear_rutina.pack(pady=10)
    vista_rutinas_frame.pack(padx=10, pady=10, fill="both", expand=True)
    # form_asignar_ejercicio_frame.pack(padx=10, pady=10, fill="x", expand=True) # Volver a mostrar

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
    actualizar_vista_rutinas()

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

def borrar_rutina_seleccionada():
    """Borra la rutina seleccionada en la tabla Treeview."""
    selected_item = tree_rutinas.focus()
    if not selected_item:
        messagebox.showerror("Error", "Por favor, seleccione una rutina para borrar.")
        return

    if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar la rutina seleccionada?"):
        return

    item_values = tree_rutinas.item(selected_item, 'values')
    id_a_borrar = int(item_values[0])

    rutina_a_borrar = next((r for r in rutinas_creadas if r.id_rutina == id_a_borrar), None)
    
    if rutina_a_borrar:
        rutinas_creadas.remove(rutina_a_borrar)
        messagebox.showinfo("Éxito", f"Rutina '{rutina_a_borrar.tipo}' borrada correctamente.")
        actualizar_vista_rutinas()

def buscar_rutinas():
    """Filtra la tabla de rutinas según el término de búsqueda."""
    termino_busqueda = entry_buscar_rutina.get().lower()

    for item in tree_rutinas.get_children():
        tree_rutinas.delete(item)

    if not termino_busqueda:
        actualizar_vista_rutinas()
        return

    for r in rutinas_creadas:
        if termino_busqueda in str(r.id_rutina).lower() or \
           termino_busqueda in str(r.tipo).lower() or \
           termino_busqueda in str(r.duracion).lower():
            tree_rutinas.insert("", tk.END, values=(r.id_rutina, r.tipo, r.duracion, len(r.ejercicios)))

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

# --- Vista de Rutinas Creadas ---
vista_rutinas_frame = ttk.LabelFrame(rutina_frame, text="Rutinas Creadas", padding=(10, 5))
vista_rutinas_frame.pack(padx=10, pady=10, fill="both", expand=True)

search_frame_rutinas = ttk.Frame(vista_rutinas_frame)
search_frame_rutinas.pack(fill='x', padx=5, pady=5)

entry_buscar_rutina = ttk.Entry(search_frame_rutinas)
entry_buscar_rutina.pack(side='left', fill='x', expand=True)

btn_buscar_rutina = ttk.Button(search_frame_rutinas, text="Buscar 🔎", command=buscar_rutinas)
btn_buscar_rutina.pack(side='right', padx=(5, 0))

columns_rutinas = ('id', 'tipo', 'duracion', 'num_ejercicios')
tree_rutinas = ttk.Treeview(vista_rutinas_frame, columns=columns_rutinas, show='headings')
tree_rutinas.heading('id', text='ID')
tree_rutinas.heading('tipo', text='Tipo')
tree_rutinas.heading('duracion', text='Duración')
tree_rutinas.heading('num_ejercicios', text='N° Ejercicios')
tree_rutinas.column('id', width=50, anchor=tk.CENTER)
tree_rutinas.pack(fill="both", expand=True)

btn_borrar_rutina = ttk.Button(vista_rutinas_frame, text="Borrar Rutina Seleccionada", command=borrar_rutina_seleccionada)
btn_borrar_rutina.pack(pady=5)


# --- Iniciar el bucle principal de la aplicación ---
ventana_principal.mainloop()