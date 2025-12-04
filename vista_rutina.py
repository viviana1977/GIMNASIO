# --- Pestaña Rutina ---

from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime
import gimnasio_modelo as gc


class VistaRutina(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Rutinas")
        self.rutinas_creadas = []

        # --- Formulario para Crear Rutina (inicialmente oculto) ---
        self.form_crear_rutina_frame = ttk.LabelFrame(self, text="Crear una nueva rutina", padding=(20, 10))

        # --- Botón principal para crear rutina ---
        self.btn_crear_rutina = ttk.Button(self, text="Crear Rutina", command=self.mostrar_form_crear_rutina, style="Alta.TButton")
        self.btn_crear_rutina.pack(pady=10)

        ttk.Label(self.form_crear_rutina_frame, text="Tipo de Rutina:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_rutina_tipo = ttk.Entry(self.form_crear_rutina_frame)
        self.entry_rutina_tipo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_crear_rutina_frame, text="Duración:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_rutina_duracion = ttk.Entry(self.form_crear_rutina_frame)

        self.form_crear_rutina_frame.columnconfigure(1, weight=1)

        self.btn_guardar_rutina = ttk.Button(self.form_crear_rutina_frame, text="Guardar Rutina", command=self.guardar_nueva_rutina)
        self.btn_guardar_rutina.grid(row=3, column=0, columnspan=2, pady=10)

        self.btn_cancelar_rutina = ttk.Button(self.form_crear_rutina_frame, text="Cancelar", command=self.ocultar_form_crear_rutina)
        self.btn_cancelar_rutina.grid(row=4, column=0, columnspan=2, pady=5)

        # --- Vista de Rutinas Creadas ---
        self.vista_rutinas_frame = ttk.LabelFrame(self, text="Rutinas Creadas", padding=(10, 5))
        self.vista_rutinas_frame.pack(padx=10, pady=10, fill="both", expand=True)

        search_frame_rutinas = ttk.Frame(self.vista_rutinas_frame)
        search_frame_rutinas.pack(fill='x', padx=5, pady=5)

        self.entry_buscar_rutina = ttk.Entry(search_frame_rutinas)
        self.entry_buscar_rutina.pack(side='left', fill='x', expand=True)

        self.btn_buscar_rutina = ttk.Button(search_frame_rutinas, text="Buscar 🔎", command=self.buscar_rutinas)
        self.btn_buscar_rutina.pack(side='right', padx=(5, 0))

        columns_rutinas = ('id', 'tipo', 'duracion', 'num_ejercicios')
        self.tree_rutinas = ttk.Treeview(self.vista_rutinas_frame, columns=columns_rutinas, show='headings')
        self.tree_rutinas.heading('id', text='ID')
        self.tree_rutinas.heading('tipo', text='Tipo')
        self.tree_rutinas.heading('duracion', text='Duración')
        self.tree_rutinas.heading('num_ejercicios', text='N° Ejercicios')
        self.tree_rutinas.column('id', width=50, anchor=tk.CENTER)
        self.tree_rutinas.pack(fill="both", expand=True)

        self.btn_borrar_rutina = ttk.Button(self.vista_rutinas_frame, text="Borrar Rutina Seleccionada", command=self.borrar_rutina_seleccionada, style="Baja.TButton")
        self.btn_borrar_rutina.pack(pady=5)

    def actualizar_vista_rutinas(self):
        """Limpia y actualiza la tabla de rutinas."""
        for item in self.tree_rutinas.get_children():
            self.tree_rutinas.delete(item)
        for r in self.rutinas_creadas:
            # Contar ejercicios para mostrar en la tabla
            num_ejercicios = len(r.ejercicios)
            self.tree_rutinas.insert("", tk.END, values=(r.id_rutina, r.tipo, r.duracion, num_ejercicios))


    def mostrar_form_crear_rutina(self):
        """Muestra el formulario para crear una nueva rutina."""
        self.btn_crear_rutina.pack_forget()
        self.vista_rutinas_frame.pack_forget()
        self.form_crear_rutina_frame.pack(padx=10, pady=10, fill="x")
        # form_asignar_ejercicio_frame.pack_forget() # Ocultar el otro form

    def ocultar_form_crear_rutina(self):
        """Oculta el formulario de creación de rutinas."""
        self.form_crear_rutina_frame.pack_forget()
        self.btn_crear_rutina.pack(pady=10)
        self.vista_rutinas_frame.pack(padx=10, pady=10, fill="both", expand=True)
        # form_asignar_ejercicio_frame.pack(padx=10, pady=10, fill="x", expand=True) # Volver a mostrar

    def guardar_nueva_rutina(self):
        """Crea un nuevo objeto rutina y lo guarda."""
        tipo = self.entry_rutina_tipo.get()
        duracion = self.entry_rutina_duracion.get()
        ejercicio_inicial = self.entry_rutina_ejercicio.get()

        if not all([tipo, duracion, ejercicio_inicial]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        # Simular un ID único para la rutina
        id_rutina = len(self.rutinas_creadas) + 1
        nueva_rutina = gc.rutina(id_rutina, tipo, duracion)
        
        # Asignar el ejercicio inicial
        nueva_rutina.asignar_ejercicio(ejercicio_inicial)
        
        self.rutinas_creadas.append(nueva_rutina)

        print(f"Nueva rutina creada: ID={nueva_rutina.id_rutina}, Tipo={nueva_rutina.tipo}, Ejercicios: {nueva_rutina.ejercicios}")
        messagebox.showinfo("Éxito", f"Rutina '{tipo}' creada correctamente.")

        # Limpiar campos y ocultar formulario
        self.entry_rutina_tipo.delete(0, tk.END)
        self.entry_rutina_duracion.delete(0, tk.END)
        self.entry_rutina_ejercicio.delete(0, tk.END)
        self.ocultar_form_crear_rutina()
        self.actualizar_vista_rutinas()

    def asignar_ejercicio_a_rutina(self):
        """Asigna un nuevo ejercicio a la rutina seleccionada en el Combobox."""
        seleccion = self.combo_rutinas.get()
        nuevo_ejercicio = self.entry_nuevo_ejercicio.get()

        if not seleccion or not nuevo_ejercicio:
            messagebox.showerror("Error", "Debe seleccionar una rutina y escribir un ejercicio.")
            return

        # Encontrar la rutina seleccionada en la lista rutinas_creadas
        id_rutina_seleccionada = int(seleccion.split(":")[0].replace("ID ", ""))
        rutina_encontrada = None
        for r in self.rutinas_creadas:
            if r.id_rutina == id_rutina_seleccionada:
                rutina_encontrada = r
                break
        
        if rutina_encontrada:
            rutina_encontrada.asignar_ejercicio(nuevo_ejercicio)
            messagebox.showinfo("Éxito", f"Ejercicio '{nuevo_ejercicio}' asignado a la rutina '{rutina_encontrada.tipo}'.")
            self.entry_nuevo_ejercicio.delete(0, tk.END)
            print(f"Rutina ID {rutina_encontrada.id_rutina} actualizada. Ejercicios: {rutina_encontrada.ejercicios}")
        else:
            messagebox.showerror("Error", "No se encontró la rutina seleccionada.")

    def borrar_rutina_seleccionada(self):
        """Borra la rutina seleccionada en la tabla Treeview."""
        selected_item = self.tree_rutinas.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una rutina para borrar.")
            return

        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar la rutina seleccionada?"):
            return

        item_values = self.tree_rutinas.item(selected_item, 'values')
        id_a_borrar = int(item_values[0])

        rutina_a_borrar = next((r for r in self.rutinas_creadas if r.id_rutina == id_a_borrar), None)
        
        if rutina_a_borrar:
            self.rutinas_creadas.remove(rutina_a_borrar)
            messagebox.showinfo("Éxito", f"Rutina '{rutina_a_borrar.tipo}' borrada correctamente.")
            self.actualizar_vista_rutinas()


    def buscar_rutinas(self):
        """Filtra la tabla de rutinas según el término de búsqueda."""
        termino_busqueda = self.entry_buscar_rutina.get().lower()

        for item in self.tree_rutinas.get_children():
            self.tree_rutinas.delete(item)

        if not termino_busqueda:
            self.actualizar_vista_rutinas()
            return

        for r in self.rutinas_creadas:
            if termino_busqueda in str(r.id_rutina).lower() or \
            termino_busqueda in str(r.tipo).lower() or \
            termino_busqueda in str(r.duracion).lower():
                self.tree_rutinas.insert("", tk.END, values=(r.id_rutina, r.tipo, r.duracion, len(r.ejercicios)))

