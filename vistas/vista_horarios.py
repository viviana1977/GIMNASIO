from  tkinter import ttk, messagebox
import tkinter as tk
from modelos import Horario, Instructor, Clases

# --- Pestaña Horarios---
class VistaHorarios(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Horarios")
        self.horarios_creados = []
        self.instructores = []
        self.clases = []
        self.id_horario_a_editar = None

        # ---Formulario de Creacion de Horarios---
        self.form_crear_horario_frame = ttk.LabelFrame(self, text="Crear Horario", padding=(20, 10))   
        ttk.Label(self.form_crear_horario_frame, text="Día de la semana:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_horario_dia = ttk.Combobox(self.form_crear_horario_frame, values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"], state="readonly")
        self.combo_horario_dia.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self.form_crear_horario_frame, text="Hora de Inicio (HH:MM):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_horario_inicio = ttk.Entry(self.form_crear_horario_frame)
        self.entry_horario_inicio.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self.form_crear_horario_frame, text="Hora de Fin (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_horario_fin = ttk.Entry(self.form_crear_horario_frame)
        self.entry_horario_fin.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_crear_horario_frame, text="Instructor:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.combo_instructor = ttk.Combobox(self.form_crear_horario_frame, state="readonly")
        self.combo_instructor.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_crear_horario_frame, text="Clase:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.combo_clase = ttk.Combobox(self.form_crear_horario_frame, state="readonly")
        self.combo_clase.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.form_crear_horario_frame.columnconfigure(1, weight=1)
        self.btn_guardar_horario = ttk.Button(self.form_crear_horario_frame, text="Guardar Horario", command=self.guardar_horario)
        self.btn_guardar_horario.grid(row=5, column=0, columnspan=2, pady=10)
        self.btn_cancelar_horario = ttk.Button(self.form_crear_horario_frame, text="Cancelar", command=self.ocultar_form_crear_horario)
        self.btn_cancelar_horario.grid(row=6, column=0, columnspan=2, pady=5)

        # --- Vista de Horarios Creados ---
        self.vista_horarios_frame = ttk.LabelFrame(self, text="Horarios Programados", padding=(10, 5))
        self.vista_horarios_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.search_frame_horarios = ttk.Frame(self.vista_horarios_frame)
        self.search_frame_horarios.pack(fill='x', padx=5, pady=5)

        self.entry_buscar_horario = ttk.Entry(self.search_frame_horarios)
        self.entry_buscar_horario.pack(side='left', fill='x', expand=True)

        self.btn_buscar_horario = ttk.Button(self.search_frame_horarios, text="Buscar 🔎", command=self.buscar_horarios)
        self.btn_buscar_horario.pack(side='right', padx=(5, 0))

        columns = ('dia', 'inicio', 'fin', 'instructor', 'clase')
        self.tree_horarios = ttk.Treeview(self.vista_horarios_frame, columns=columns, show='headings')
        self.tree_horarios.heading('dia', text='Día')
        self.tree_horarios.heading('inicio', text='Hora Inicio')
        self.tree_horarios.heading('fin', text='Hora Fin')
        self.tree_horarios.heading('instructor', text='Instructor')
        self.tree_horarios.heading('clase', text='Clase')
        self.tree_horarios.pack(fill="both", expand=True)

        self.btn_crear_horario = ttk.Button(self.vista_horarios_frame, text="Crear Horario", command=self.mostrar_form_crear_horario)
        self.btn_crear_horario.pack(pady=10, side=tk.LEFT)

        self.btn_modificar_horario = ttk.Button(self.vista_horarios_frame, text="Modificar Horario", command=self.mostrar_form_modificar_horario)
        self.btn_modificar_horario.pack(pady=10, side=tk.LEFT, padx=5)

        self.btn_borrar_horario = ttk.Button(self.vista_horarios_frame, text="Borrar Horario", command=self.borrar_horario)
        self.btn_borrar_horario.pack(pady=10, side=tk.LEFT)

        self.actualizar_vista_horarios()

    def actualizar_vista_horarios(self):
        """Limpia y actualiza la tabla de horarios con los datos más recientes."""
        # Limpiar vista previa
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)

        self.horarios_creados: list[Horario] = Horario.obtener_todos_con_relaciones()

        # Llenar con datos actualizados
        for h in self.horarios_creados:
            # i = Instructor.obtener_por_id(h.id_instructor)
            # c = Clases.obtener_por_id(h.id_clase)
            # nombre_instructor = i.nombre if i else ''
            # nombre_clase = c.nombre if c else ''
            self.tree_horarios.insert("", tk.END, text=h.id_horario, values=(h.dia_semana, h.hora_inicio, h.hora_final, h.nombre_instructor, h.nombre_clase))

    def _cargar_comboboxes(self):
        """Carga los datos de instructores y clases en los comboboxes."""
        self.instructores = Instructor.obtener_todos()
        self.clases = Clases.obtener_todos()

        self.combo_instructor['values'] = [f"{i.id_instructor} - {i.nombre}" for i in self.instructores]
        self.combo_clase['values'] = [f"{c.id_clase} - {c.nombre}" for c in self.clases]

    def mostrar_form_crear_horario(self):
        self.entry_horario_inicio.delete(0, tk.END)
        self.entry_horario_fin.delete(0, tk.END)
        self.combo_horario_dia.set('')
        self.combo_instructor.set('')
        self.combo_clase.set('')

        self._cargar_comboboxes()

        self.form_crear_horario_frame.config(text="Crear Horario")
        self.btn_guardar_horario.config(text="Guardar Horario", command=self.guardar_horario)
        self.id_horario_a_editar = None

        self.form_crear_horario_frame.pack(padx=10, pady=10, fill="x")
        self.vista_horarios_frame.pack_forget()

    def mostrar_form_modificar_horario(self):
        selected_item = self.tree_horarios.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un horario para modificar.")
            return

        id_horario = self.tree_horarios.item(selected_item, 'text')
        horario_a_modificar = next((h for h in self.horarios_creados if h.id_horario == int(id_horario)), None)

        if not horario_a_modificar:
            messagebox.showerror("Error", "No se encontró el horario seleccionado.")
            return
        
        self._cargar_comboboxes()

        self.entry_horario_inicio.delete(0, tk.END)
        self.entry_horario_fin.delete(0, tk.END)

        self.combo_horario_dia.set(horario_a_modificar.dia_semana)
        self.entry_horario_inicio.insert(0, horario_a_modificar.hora_inicio)
        self.entry_horario_fin.insert(0, horario_a_modificar.hora_final)
        self.combo_clase.set(f"{horario_a_modificar.id_clase} - {horario_a_modificar.nombre_clase}")
        self.combo_instructor.set(f"{horario_a_modificar.id_instructor} - {horario_a_modificar.nombre_instructor}")
        
        # Seleccionar instructor en combobox
        if horario_a_modificar.id_instructor:
            instructor_str = f"{horario_a_modificar.id_instructor} - {horario_a_modificar.nombre_instructor}"
            if instructor_str in self.combo_instructor['values']:
                self.combo_instructor.set(instructor_str)

        # Seleccionar clase en combobox
        if horario_a_modificar.id_clase:
            clase_str = f"{horario_a_modificar.id_clase} - {horario_a_modificar.nombre_clase}"
            if clase_str in self.combo_clase['values']:
                self.combo_clase.set(clase_str)

        self.id_horario_a_editar = id_horario
        self.form_crear_horario_frame.config(text="Modificar Horario")
        self.btn_guardar_horario.config(text="Actualizar Horario", command=self.actualizar_horario)

        self.form_crear_horario_frame.pack(padx=10, pady=10, fill="x")
        self.vista_horarios_frame.pack_forget()

    def ocultar_form_crear_horario(self):
        self.form_crear_horario_frame.pack_forget()
        self.vista_horarios_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def guardar_horario(self):
        dia = self.combo_horario_dia.get()
        inicio = self.entry_horario_inicio.get()
        fin = self.entry_horario_fin.get()
        instructor_seleccionado = self.combo_instructor.get()
        clase_seleccionada = self.combo_clase.get()

        if not all([dia, inicio, fin]):
            messagebox.showerror("Error", "Los campos de día y hora son obligatorios.")
            return

        # Extraer IDs de los strings de los comboboxes
        id_instructor = int(instructor_seleccionado.split(' - ')[0]) if instructor_seleccionado else None
        id_clase = int(clase_seleccionada.split(' - ')[0]) if clase_seleccionada else None

        nuevo_horario = Horario(self.id_horario_a_editar, dia, inicio, fin, id_instructor, id_clase)
        nuevo_horario.guardar()

        self.id_horario_a_editar = None # Limpiar para el próximo guardado

        messagebox.showinfo("Éxito", f"Horario para el {dia} de {inicio} a {fin} creado.")

        self.ocultar_form_crear_horario()
        self.actualizar_vista_horarios()

    def actualizar_horario(self):
        dia = self.combo_horario_dia.get()
        inicio = self.entry_horario_inicio.get()
        fin = self.entry_horario_fin.get()
        instructor_seleccionado = self.combo_instructor.get()
        clase_seleccionada = self.combo_clase.get()


        if not all([dia, inicio, fin, self.id_horario_a_editar, instructor_seleccionado, clase_seleccionada]):
            messagebox.showerror("Error", "Todos los campos son obligatorios para actualizar.")
            return

        self.guardar_horario()

    def borrar_horario(self):
        selected_item = self.tree_horarios.focus()

        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un horario para borrar.")
            return

        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar el horario seleccionado?"):
            return

        id_a_borrar = int(self.tree_horarios.item(selected_item, 'text'))

        horario_a_borrar = next((h for h in self.horarios_creados if h.id_horario == id_a_borrar), None)
        
        if horario_a_borrar:
            horario_a_borrar.eliminar()
            messagebox.showinfo("Éxito", "Horario borrado correctamente.")
            self.actualizar_vista_horarios()

    def buscar_horarios(self):
        termino_busqueda = self.entry_buscar_horario.get().lower()

        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)

        if not termino_busqueda:
            self.actualizar_vista_horarios()
            return

        for h in self.horarios_creados:
            if termino_busqueda in str(h.id_horario).lower() or \
               termino_busqueda in str(h.dia_semana).lower() or \
               termino_busqueda in str(h.hora_inicio).lower() or \
               termino_busqueda in str(h.hora_final).lower() or \
               (h.nombre_instructor and termino_busqueda in str(h.nombre_instructor).lower()) or \
               (h.nombre_clase and termino_busqueda in str(h.nombre_clase).lower()):
                self.tree_horarios.insert("", tk.END, text=h.id_horario, values=(h.dia_semana, h.hora_inicio, h.hora_final, h.nombre_instructor, h.nombre_clase))
