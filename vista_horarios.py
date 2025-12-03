from  tkinter import ttk, messagebox
import tkinter as tk
import gimnasio_modelo as gc

# --- Pestaña Horarios---
class VistaHorarios(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Horarios")
        self.horarios_creados = []

        # --- Botón y Formulario de Creación de Horarios ---
        self.btn_crear_horario = ttk.Button(self, text="Crear Nuevo Horario", command=self.mostrar_form_crear_horario)
        self.btn_crear_horario.pack(pady=10)

        # ---Formulario de Creacion de Horarios---
        self.form_crear_horario_frame = ttk.LabelFrame(self, text="Crear Horario", padding=(20, 10))   
        ttk.Label(self.form_crear_horario_frame, text="Día de la semana:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_horario_dia = ttk.Combobox(self.form_crear_horario_frame, values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"], state="readonly")
        self.combo_horario_dia.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_horario_inicio = ttk.Entry(self.form_crear_horario_frame)
        self.entry_horario_inicio.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self.form_crear_horario_frame, text="Hora de Fin (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_horario_fin = ttk.Entry(self.form_crear_horario_frame)
        self.entry_horario_fin.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.form_crear_horario_frame.columnconfigure(1, weight=1)
        self.btn_guardar_horario = ttk.Button(self.form_crear_horario_frame, text="Guardar Horario", command=self.guardar_nuevo_horario)
        self.btn_guardar_horario.grid(row=3, column=0, columnspan=2, pady=10)
        self.btn_cancelar_horario = ttk.Button(self.form_crear_horario_frame, text="Cancelar", command=self.ocultar_form_crear_horario)
        self.btn_cancelar_horario.grid(row=4, column=0, columnspan=2, pady=5)

        # --- Vista de Horarios Creados ---
        self.vista_horarios_frame = ttk.LabelFrame(self, text="Horarios Programados", padding=(10, 5))
        self.vista_horarios_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.search_frame_horarios = ttk.Frame(self.vista_horarios_frame)
        self.search_frame_horarios.pack(fill='x', padx=5, pady=5)

        self.entry_buscar_horario = ttk.Entry(self.search_frame_horarios)
        self.entry_buscar_horario.pack(side='left', fill='x', expand=True)

        self.btn_buscar_horario = ttk.Button(self.search_frame_horarios, text="Buscar 🔎", command=self.buscar_horarios)
        self.btn_buscar_horario.pack(side='right', padx=(5, 0))

        columns = ('id', 'dia', 'inicio', 'fin')
        self.tree_horarios = ttk.Treeview(self.vista_horarios_frame, columns=columns, show='headings')
        self.tree_horarios.heading('id', text='ID')
        self.tree_horarios.heading('dia', text='Día')
        self.tree_horarios.heading('inicio', text='Hora Inicio')
        self.tree_horarios.heading('fin', text='Hora Fin')
        self.tree_horarios.column('id', width=50, anchor=tk.CENTER)
        self.tree_horarios.pack(fill="both", expand=True)

        self.btn_borrar_horario = ttk.Button(self.vista_horarios_frame, text="Borrar Horario Seleccionado", command=self.borrar_horario_seleccionado)
        self.btn_borrar_horario.pack(pady=5)

    def actualizar_vista_horarios(self):
        """Limpia y actualiza la tabla de horarios con los datos más recientes."""
        # Limpiar vista previa
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)
        # Llenar con datos actualizados
        for h in self.horarios_creados:
            self.tree_horarios.insert("", tk.END, values=(h.id_dias, h.dia_semana, h.hora_inicio, h.hora_final))

    def mostrar_form_crear_horario(self):
        """Muestra el formulario para crear un nuevo horario."""
        self.btn_crear_horario.pack_forget()
        self.form_crear_horario_frame.pack(padx=10, pady=10, fill="x")

    def ocultar_form_crear_horario(self):
        """Oculta el formulario de creación y vuelve a mostrar el botón principal."""
        self.form_crear_horario_frame.pack_forget()
        self.btn_crear_horario.pack(pady=10)

    def guardar_nuevo_horario(self):
        """Guarda un nuevo horario y actualiza la vista."""
        dia = self.combo_horario_dia.get()
        inicio = self.entry_horario_inicio.get()
        fin = self.entry_horario_fin.get()

        if not all([dia, inicio, fin]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        id_horario = len(self.horarios_creados) + 1
        nuevo_horario = gc.horarios(id_horario, dia, inicio, fin)
        self.horarios_creados.append(nuevo_horario)

        messagebox.showinfo("Éxito", f"Horario para el {dia} de {inicio} a {fin} creado.")
        print(f"Nuevo horario creado: ID={nuevo_horario.id_dias}, Día={nuevo_horario.dia_semana}")

        self.entry_horario_inicio.delete(0, tk.END)
        self.entry_horario_fin.delete(0, tk.END)
        self.ocultar_form_crear_horario()
        self.actualizar_vista_horarios()
        self.actualizar_comboboxes_asignacion() # Actualiza el combo en la pestaña Clases

    def borrar_horario_seleccionado(self):
        """Borra el horario seleccionado en la tabla Treeview."""
        selected_item = self.tree_horarios.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un horario para borrar.")
            return

        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar el horario seleccionado?"):
            return

        item_values = self.tree_horarios.item(selected_item, 'values')
        id_a_borrar = int(item_values[0])

        horario_a_borrar = next((h for h in self.horarios_creados if h.id_dias == id_a_borrar), None)
        
        if horario_a_borrar:
            self.horarios_creados.remove(horario_a_borrar)
            messagebox.showinfo("Éxito", "Horario borrado correctamente.")
            actualizar_vista_horarios()

    def buscar_horarios(self):
        """Filtra la tabla de horarios según el término de búsqueda."""
        termino_busqueda = self.entry_buscar_horario.get().lower()

        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)

        if not termino_busqueda:
            actualizar_vista_horarios()
            return

        for h in self.horarios_creados:
            if termino_busqueda in str(h.id_dias).lower() or \
            termino_busqueda in str(h.dia_semana).lower() or \
            termino_busqueda in str(h.hora_inicio).lower() or \
            termino_busqueda in str(h.hora_final).lower():
                self.tree_horarios.insert("", tk.END, values=(h.id_dias, h.dia_semana, h.hora_inicio, h.hora_final))
