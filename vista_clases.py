from tkinter import ttk, messagebox
import tkinter as tk
import gimnasio_modelo as gc

# --- Pestaña Clases ---
class VistaClases(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Clases") # Changed text to "Clases" for consistency
        self.clases_creadas = []

        #---button to show the registration form---
        self.btn_crear_clase = ttk.Button(self, text="Crear Nueva Clase", command=self.mostrar_form_crear_clase, style="Alta.TButton")
        self.btn_crear_clase.pack(pady=10)

        #-- Formulario de Creación de Clases (initially hidden) ---
        self.form_crear_clase_frame = ttk.LabelFrame(self, text="Crear Clase", padding=(20, 10))

        labels_clases_text = ["Tipo:", "Capacidad:", "Nombre:"]
        self.entries_clases = []

        for i, label_text in enumerate(labels_clases_text):
            ttk.Label(self.form_crear_clase_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.form_crear_clase_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries_clases.append(entry)

        # Assign variables to entry fields for easy access
        (self.entry_clase_tipo, self.entry_clase_capacidad, 
        self.entry_clase_nombres) = self.entries_clases
        
        # Configure the column for entry fields to expand
        self.form_crear_clase_frame.columnconfigure(1, weight=1)

        # Buttons for the form
        self.btn_guardar_clase = ttk.Button(self.form_crear_clase_frame, 
                                            text="Guardar Clase", 
                                            command=self.guardar_nueva_clase)
        self.btn_guardar_clase.grid(row=len(labels_clases_text), column=0, 
                                    columnspan=2, pady=10)
        self.btn_cancelar_clase = ttk.Button(self.form_crear_clase_frame, 
                                            text="Cancelar", 
                                            command=self.ocultar_form_crear_clase)
        self.btn_cancelar_clase.grid(row=len(labels_clases_text) + 1, 
                                    column=0, columnspan=2, pady=5)

        # --- View of Registered Classes ---
        self.vista_clases_frame = ttk.LabelFrame(self, text="Clases Disponibles", padding=(10, 5))
        self.vista_clases_frame.pack(padx=10, pady=10, fill="both", expand=True)    

        # --- Search Widget ---
        search_frame_clases = ttk.Frame(self.vista_clases_frame)
        search_frame_clases.pack(fill='x', padx=5, pady=5)

        self.entry_buscar_clase = ttk.Entry(search_frame_clases)
        self.entry_buscar_clase.pack(side='left', fill='x', expand=True)

        self.btn_buscar_clase = ttk.Button(search_frame_clases, text="Buscar 🔎", command=self.buscar_clases)
        self.btn_buscar_clase.pack(side='right', padx=(5, 0))

        
        columns_clases = ('id', 'tipo', 'capacidad', 'instructor')
        tree_clases = ttk.Treeview(self.vista_clases_frame, columns=columns_clases, show='headings')
        tree_clases.heading('id', text='ID')
        tree_clases.heading('tipo', text='Tipo')
        tree_clases.heading('capacidad', text='Capacidad')
        tree_clases.heading('instructor', text='Instructor Asignado')
        tree_clases.column('id', width=50, anchor=tk.CENTER)
        tree_clases.pack(fill="both", expand=True)

        self.btn_borrar_clase = ttk.Button(self.vista_clases_frame, 
                                           text="Borrar Clase Seleccionada",
                                           command=self.borrar_clase_seleccionada, style="Baja.TButton")
        self.btn_borrar_clase.pack(pady=5)
        # --- Formulario de Asignación de Instructores y Horarios ---
        form_asignar_frame = ttk.LabelFrame(self, text="Asignar Instructor y Horario", padding=(20, 10))
        form_asignar_frame.pack(padx=10, pady=10, fill="x")


        ttk.Label(form_asignar_frame, text="Seleccionar Clase:").pack(pady=2)
        self.combo_asignar_clase = ttk.Combobox(form_asignar_frame, state="readonly")
        self.combo_asignar_clase.pack(pady=2, fill="x")

        ttk.Label(form_asignar_frame, text="Asignar Instructor:").pack(pady=2)
        self.combo_asignar_instructor = ttk.Combobox(form_asignar_frame, state="readonly")
        self.combo_asignar_instructor.pack(pady=2, fill="x")

        ttk.Label(form_asignar_frame, text="Asignar Horario:").pack(pady=2)
        combo_asignar_horario = ttk.Combobox(form_asignar_frame, state="readonly")
        combo_asignar_horario.pack(pady=2, fill="x")

        btn_asignar = ttk.Button(form_asignar_frame, text="Asignar", command=self.asignar_instructor_a_clase)
        btn_asignar.pack(pady=10)

         
    def actualizar_vista_clases(self):
            """Limpia y actualiza la tabla de clases."""    
            for item in self.tree_clases.get_children():
                self.tree_clases.delete(item)
            for c in self.clases_creadas:
                instructor_nombre = c.instructor.nombre if hasattr(c, 'instructor') else "No asignado"
                self.tree_clases.insert("", tk.END, values=(c.id_clase, c.tipo, c.capacidad, instructor_nombre))

    def actualizar_comboboxes_asignacion(self):
        """Actualiza los comboboxes de la sección de asignación."""
        self.combo_asignar_clase['values'] = [f"ID {c.id_clase}: {c.tipo}" for c in self.clases_creadas]
        self.combo_asignar_instructor['values'] = [f"ID {i.id_instructor}: {i.nombre}" for i in self.instructores_creados]
        self.combo_asignar_horario['values'] = [f"ID {h.id_dias}: {h.dia_semana} ({h.hora_inicio}-{h.hora_final})" for h in self.horarios_creados]

    def mostrar_form_crear_clase(self):
        self.btn_crear_clase.pack_forget()
        self.form_crear_clase_frame.pack(padx=10, pady=10, fill="x")

    def ocultar_form_crear_clase(self):
        self.form_crear_clase_frame.pack_forget()
        self.btn_crear_clase.pack(pady=10)

    def guardar_nueva_clase(self):
        tipo = self.entry_clase_tipo.get()
        capacidad = self.entry_clase_capacidad.get()
        nombres = self.entry_clase_nombres.get()

        if not all([tipo, capacidad, nombres]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        id_clase = len(self.clases_creadas) + 1
        nueva_clase = gc.clases(id_clase, tipo, capacidad, nombres)
        self.clases_creadas.append(nueva_clase)

        messagebox.showinfo("Éxito", f"Clase '{tipo}' creada correctamente.")
        for entry in [self.entry_clase_tipo, self.entry_clase_capacidad, self.entry_clase_nombres]:
            entry.delete(0, tk.END)
        self.ocultar_form_crear_clase()
        self.actualizar_vista_clases()
        self.actualizar_comboboxes_asignacion()

    def asignar_instructor_a_clase(self):
        clase_sel = self.combo_asignar_clase.get()
        instructor_sel = self.combo_asignar_instructor.get()

        if not all([clase_sel, instructor_sel]):
            messagebox.showerror("Error", "Debe seleccionar una clase y un instructor.")
            return

        id_clase = int(clase_sel.split(":")[0].replace("ID ", ""))
        id_instructor = int(instructor_sel.split(":")[0].replace("ID ", ""))

        clase_obj = next((c for c in self.clases_creadas if c.id_clase == id_clase), None)
        instructor_obj = next((i for i in self.instructores_creados if i.id_instructor == id_instructor), None)

        if clase_obj and instructor_obj:
            clase_obj.agregar_instructor(instructor_obj)
            messagebox.showinfo("Éxito", f"Instructor '{instructor_obj.nombre}' asignado a la clase '{clase_obj.tipo}'.")
            self.actualizar_vista_clases()
        else:
            messagebox.showerror("Error", "No se encontró la clase o el instructor.")

    def borrar_clase_seleccionada(self):
        """Borra la clase seleccionada en la tabla Treeview."""
        selected_item = self.tree_clases.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una clase para borrar.")
            return

        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar la clase seleccionada?"):
            return

        item_values = self.tree_clases.item(selected_item, 'values')
        id_a_borrar = int(item_values[0])

        clase_a_borrar = next((c for c in self.clases_creadas if c.id_clase == id_a_borrar), None)
        
        if clase_a_borrar:
            self.clases_creadas.remove(clase_a_borrar)
            messagebox.showinfo("Éxito", f"Clase '{clase_a_borrar.tipo}' borrada correctamente.")
            self.actualizar_vista_clases()
            self.actualizar_comboboxes_asignacion()

    def buscar_clases(self):
        """Filtra la tabla de clases según el término de búsqueda."""
        termino_busqueda = self.entry_buscar_clase.get().lower()

        for item in self.tree_clases.get_children():
            self.tree_clases.delete(item)

        if not termino_busqueda:
            self.actualizar_vista_clases()
            return

        for c in self.clases_creadas:
            instructor_nombre = c.instructor.nombre if hasattr(c, 'instructor') else ""
            if termino_busqueda in str(c.id_clase).lower() or \
               termino_busqueda in str(c.tipo).lower() or \
               termino_busqueda in str(c.capacidad).lower() or \
               termino_busqueda in instructor_nombre.lower():
                self.tree_clases.insert("", tk.END, values=(c.id_clase, c.tipo, c.capacidad, instructor_nombre))


#################################
