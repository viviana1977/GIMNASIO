from tkinter import ttk, messagebox
import tkinter as tk
from modelos import Clases

# --- Pestaña Clases ---
class VistaClases(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Clases") # Changed text to "Clases" for consistency
        self.clases_creadas = []
        self.id_clase_a_editar = None
 
        #-- Formulario de Creación de Clases (initially hidden) ---
        self.form_crear_clase_frame = ttk.LabelFrame(self, text="Crear Clase", padding=(20, 10))

        labels_clases_text = ["Tipo:", "Nombre:"]
        self.entries_clases = []

        for i, label_text in enumerate(labels_clases_text):
            ttk.Label(self.form_crear_clase_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.form_crear_clase_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries_clases.append(entry)

        # Assign variables to entry fields for easy access
        (self.entry_clase_tipo, 
        self.entry_clase_nombre) = self.entries_clases
        
        # Configure the column for entry fields to expand
        self.form_crear_clase_frame.columnconfigure(1, weight=1)

        # Buttons for the form
        self.btn_guardar_clase = ttk.Button(self.form_crear_clase_frame, 
                                            text="Guardar Clase", 
                                            command=self.guardar_clase)
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

        columns_clases = ('tipo', 'nombre')
        self.tree_clases = ttk.Treeview(self.vista_clases_frame, columns=columns_clases, show='headings')
        self.tree_clases.heading('tipo', text='Tipo')
        self.tree_clases.heading('nombre', text='Nombre')
        self.tree_clases.pack(fill="both", expand=True)

        #---button to show the registration form---
        self.btn_crear_clase = ttk.Button(self.vista_clases_frame, text="Crear Clase", command=self.mostrar_form_crear_clase)
        self.btn_crear_clase.pack(pady=10, side=tk.LEFT)

        self.btn_modificar_clase = ttk.Button(self.vista_clases_frame, text="Modificar Clase", command=self.mostrar_form_modificar_clase)
        self.btn_modificar_clase.pack(pady=10, side=tk.LEFT, padx=5)

        self.btn_borrar_clase = ttk.Button(self.vista_clases_frame, text="Borrar Clase", command=self.borrar_clase) #
        self.btn_borrar_clase.pack(pady=10, side=tk.LEFT)

        self.actualizar_vista_clases()

         
    def actualizar_vista_clases(self):
            """Limpia y actualiza la tabla de clases."""    
            for item in self.tree_clases.get_children():
                self.tree_clases.delete(item)

            self.clases_creadas: list[Clases] = Clases.obtener_todos()

            for c in self.clases_creadas:
                self.tree_clases.insert("", tk.END, text=c.id_clase, values=(c.tipo, c.nombre))

    def mostrar_form_crear_clase(self):
        self.entry_clase_tipo.delete(0, tk.END)
        self.entry_clase_nombre.delete(0, tk.END)

        self.form_crear_clase_frame.config(text="Crear Clase")
        self.btn_guardar_clase.config(text="Guardar Clase", command=self.guardar_clase)
        self.id_clase_a_editar = None

        self.form_crear_clase_frame.pack(padx=10, pady=10, fill="x")
        self.vista_clases_frame.pack_forget()

    def mostrar_form_modificar_clase(self):
        selected_item = self.tree_clases.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una clase para modificar.")
            return

        id_clase = self.tree_clases.item(selected_item, 'text')
        clase_a_modificar = next((c for c in self.clases_creadas if c.id_clase == id_clase), None)

        if not clase_a_modificar:
            messagebox.showerror("Error", "No se encontró la clase seleccionada.")
            return

        self.entry_clase_tipo.delete(0, tk.END)
        self.entry_clase_nombre.delete(0, tk.END)

        self.entry_clase_tipo.insert(0, clase_a_modificar.tipo)
        self.entry_clase_nombre.insert(0, clase_a_modificar.nombre)

        self.id_clase_a_editar = id_clase
        self.form_crear_clase_frame.config(text="Modificar Clase")
        self.btn_guardar_clase.config(text="Actualizar Clase", command=self.actualizar_clase)

        self.form_crear_clase_frame.pack(padx=10, pady=10, fill="x")
        self.vista_clases_frame.pack_forget()

    def ocultar_form_crear_clase(self):
        self.id_clase_a_editar = None
        self.form_crear_clase_frame.pack_forget()
        self.vista_clases_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def guardar_clase(self):
        tipo = self.entry_clase_tipo.get()
        nombre = self.entry_clase_nombre.get()

        if not all([tipo, nombre]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        clase = Clases(self.id_clase_a_editar, tipo, nombre)
        clase.guardar()
        
        messagebox.showinfo("Éxito", f"Clase '{nombre}' guardada correctamente.")
        
        self.ocultar_form_crear_clase()
        self.actualizar_vista_clases()

    def actualizar_clase(self):
        tipo = self.entry_clase_tipo.get()
        nombre = self.entry_clase_nombre.get()

        if not all([tipo, nombre, self.id_clase_a_editar]):
            messagebox.showerror("Error", "Todos los campos son obligatorios y debe haber una clase seleccionada.")
            return

        self.guardar_clase()

    def borrar_clase(self):
        selected_item = self.tree_clases.focus()

        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una clase para borrar.")
            return

        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar la clase seleccionada?"):
            return
 
        id_a_borrar = self.tree_clases.item(selected_item, 'text')

        clase_a_borrar = next((c for c in self.clases_creadas if c.id_clase == id_a_borrar), None)
        
        if clase_a_borrar:
            clase_a_borrar.eliminar()
            messagebox.showinfo("Éxito", f"Clase '{clase_a_borrar.nombre}' borrada correctamente.")
            self.actualizar_vista_clases()

    def buscar_clases(self):
        termino_busqueda = self.entry_buscar_clase.get().lower()

        for item in self.tree_clases.get_children():
            self.tree_clases.delete(item)

        if not termino_busqueda:
            self.actualizar_vista_clases()
            return

        for c in self.clases_creadas:
            if termino_busqueda in str(c.tipo).lower() or \
               termino_busqueda in str(c.nombre).lower():
                self.tree_clases.insert("", tk.END, values=(c.tipo, c.nombre))
