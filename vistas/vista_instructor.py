from tkinter import ttk, messagebox
import tkinter as tk
from modelos import Instructor

# --- Pestaña instructor ---
class VistaInstructor(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Instructor") # Changed text to "Instructor" for consistency
        self.instructores_creados = []
        self.id_instructor_a_editar = None
        
        # --- Formulario de Registro de Instructores (initially hidden) ---
        self.form_alta_instructor_frame = ttk.LabelFrame(self, text="Registrar Nuevo Instructor", padding=(20, 10))

        labels_instructor_text = ["Nombre:", "Dirección:", "Teléfono:", "Sueldo:"]
        self.entries_instructor = []

        for i, label_text in enumerate(labels_instructor_text):
            ttk.Label(self.form_alta_instructor_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.form_alta_instructor_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries_instructor.append(entry)

        # Assign variables to entry fields for easy access
        (self.entry_instructor_nombre, self.entry_instructor_direccion, 
         self.entry_instructor_telefono, self.entry_instructor_sueldo) = self.entries_instructor

        # Configure the column for entry fields to expand
        self.form_alta_instructor_frame.columnconfigure(1, weight=1)

        # Buttons for the form
        self.btn_guardar_instructor = ttk.Button(self.form_alta_instructor_frame, 
                                                 text="Guardar Instructor", 
                                                 command=self.guardar_instructor)
        self.btn_guardar_instructor.grid(row=len(labels_instructor_text), column=0, 
                                         columnspan=2, pady=10)
        self.btn_cancelar_instructor_form = ttk.Button(self.form_alta_instructor_frame, 
                                                       text="Cancelar", 
                                                       command=self.ocultar_form_alta_instructor)
        self.btn_cancelar_instructor_form.grid(row=len(labels_instructor_text) + 1, 
                                               column=0, columnspan=2, pady=5)

        # --- View of Registered Instructors ---
        self.vista_instructores_frame = ttk.LabelFrame(self, text="Instructores Registrados", padding=(10, 5))
        self.vista_instructores_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Search Widget ---
        search_frame_inst = ttk.Frame(self.vista_instructores_frame)
        search_frame_inst.pack(fill='x', padx=5, pady=5)

        self.entry_buscar_instructor = ttk.Entry(search_frame_inst)
        self.entry_buscar_instructor.pack(side='left', fill='x', expand=True)       

        self.btn_buscar_instructor = ttk.Button(search_frame_inst, text="Buscar 🔎", 
                                                command=self.buscar_instructores)
        self.btn_buscar_instructor.pack(side='right', padx=(5, 0))

        columns_inst = ('nombre', 'telefono', 'sueldo')
        self.tree_instructores = ttk.Treeview(self.vista_instructores_frame, columns=columns_inst, show='headings')
        self.tree_instructores.heading('nombre', text='Nombre')
        self.tree_instructores.heading('telefono', text='Teléfono')
        self.tree_instructores.heading('sueldo', text='Sueldo')
        self.tree_instructores.pack(fill="both", expand=True)

       
       # --- Button to show the registration form ---
        self.btn_alta_instructor = ttk.Button(self.vista_instructores_frame, text="Crear Instructor", command=self.mostrar_form_crear_instructor)
        self.btn_alta_instructor.pack(pady=10, side=tk.LEFT)

        self.btn_modificar_instructor = ttk.Button(self.vista_instructores_frame, text="Modificar Instructor", command=self.mostrar_form_modificar_instructor)
        self.btn_modificar_instructor.pack(pady=10, side=tk.LEFT, padx=5)
       
        self.btn_borrar_instructor = ttk.Button(self.vista_instructores_frame, text="Borrar Instructor", command=self.borrar_instructor)
        self.btn_borrar_instructor.pack(pady=10, side=tk.LEFT)

        # Initial update of the view
        self.actualizar_vista_instructores()

    def actualizar_vista_instructores(self):
        """Limpia y actualiza la tabla de instructores."""
        for item in self.tree_instructores.get_children():
            self.tree_instructores.delete(item)

        self.instructores_creados: list[Instructor] = Instructor.obtener_todos()

        for inst in self.instructores_creados:
            self.tree_instructores.insert("", tk.END, text=inst.id_instructor, values=(inst.id_instructor, 
                                                             inst.nombre, inst.telefono, inst.sueldo))

    def mostrar_form_crear_instructor(self):
        self.entry_instructor_direccion.delete(0, tk.END)
        self.entry_instructor_nombre.delete(0, tk.END)
        self.entry_instructor_sueldo.delete(0, tk.END)
        self.entry_instructor_telefono.delete(0, tk.END)

        self.form_alta_instructor_frame.config(text="Crear Instructor")
        self.btn_guardar_instructor.config(text="Guardar Instructor", command=self.guardar_instructor)
        self.id_instructor_a_editar = None

        self.form_alta_instructor_frame.pack(padx=10, pady=10, fill="x")
        self.vista_instructores_frame.pack_forget()

    def mostrar_form_modificar_instructor(self):
        selected_item = self.tree_instructores.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un instructor para modificar.")
            return

        id_instructor = self.tree_instructores.item(selected_item, 'text')
        instructor_a_editar = next((i for i in self.instructores_creados if i.id_instructor == id_instructor), None)

        if not instructor_a_editar:
            messagebox.showerror("Error", "No se encontró el instructor seleccionado.")
            return
        
        self.entry_instructor_direccion.delete(0, tk.END)
        self.entry_instructor_nombre.delete(0, tk.END)
        self.entry_instructor_sueldo.delete(0, tk.END)
        self.entry_instructor_telefono.delete(0, tk.END)

        self.entry_instructor_direccion.insert(0, instructor_a_editar.direccion)
        self.entry_instructor_nombre.insert(0, instructor_a_editar.nombre)
        self.entry_instructor_sueldo.insert(0, instructor_a_editar.sueldo)
        self.entry_instructor_telefono.insert(0, instructor_a_editar.telefono)

        self.id_instructor_a_editar = id_instructor

        self.form_alta_instructor_frame.config(text="Modificar Instructor")
        self.btn_guardar_instructor.config(text="Actualizar Clase", command=self.actualizar_instructor)

        self.form_alta_instructor_frame.pack(padx=10, pady=10, fill="x")
        self.vista_instructores_frame.pack_forget()

    def ocultar_form_alta_instructor(self):
        self.id_instructor_a_editar = None
        self.form_alta_instructor_frame.pack_forget()
        self.vista_instructores_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def guardar_instructor(self):
        nombre = self.entry_instructor_nombre.get()
        direccion = self.entry_instructor_direccion.get()
        telefono = self.entry_instructor_telefono.get()
        sueldo = self.entry_instructor_sueldo.get()

        if not all([nombre, direccion, telefono, sueldo]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        nuevo_instructor = Instructor(self.id_instructor_a_editar, nombre, direccion, telefono, sueldo)
        nuevo_instructor.guardar()

        messagebox.showinfo("Éxito", f"Instructor {nombre} registrado correctamente.")

        self.ocultar_form_alta_instructor()
        self.actualizar_vista_instructores()

    def actualizar_instructor(self):
        nombre = self.entry_instructor_nombre.get()
        direccion = self.entry_instructor_direccion.get()
        telefono = self.entry_instructor_telefono.get()
        sueldo = self.entry_instructor_sueldo.get()

        if not all([nombre, direccion, telefono, sueldo]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        self.guardar_instructor()

    def borrar_instructor(self):
        selected_item = self.tree_instructores.focus()

        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un instructor para borrar.")
            return

        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar el instructor seleccionado?"):
            return

        id_a_borrar = self.tree_instructores.item(selected_item, 'text')

        instructor_a_borrar = next((inst for inst in self.instructores_creados if inst.id_instructor == id_a_borrar), None)
        
        if instructor_a_borrar:
            instructor_a_borrar.eliminar()
            messagebox.showinfo("Éxito", f"Instructor '{instructor_a_borrar.nombre}' borrado correctamente.")
            self.actualizar_vista_instructores()

    def buscar_instructores(self):
        """Filtra la tabla de instructores según el término de búsqueda."""
        termino_busqueda = self.entry_buscar_instructor.get().lower()

        for item in self.tree_instructores.get_children():
            self.tree_instructores.delete(item)

        if not termino_busqueda:
            self.actualizar_vista_instructores()
            return

        for inst in self.instructores_creados:
            if  termino_busqueda in str(inst.id_instructor).lower() or \
                termino_busqueda in str(inst.nombre).lower() or \
                termino_busqueda in str(inst.telefono).lower() or \
                termino_busqueda in str(inst.sueldo).lower():
                self.tree_instructores.insert("", tk.END, values=(inst.id_instructor, inst.nombre, inst.telefono, inst.sueldo))
