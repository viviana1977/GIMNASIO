from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime
from modelos import Ejercicio

class VistaEjercicio(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Ejercicio")
        self.ejercicios_creados = []

        # --- Widgets de la Pestaña Ejercicios ---
        self.btn_crear_ejercicio = ttk.Button(self, text="Crear Nuevo Ejercicio", command=self.mostrar_form_crear_ejercicio, style="Alta.TButton")
        self.btn_crear_ejercicio.pack(pady=10)

        self.form_crear_ejercicio_frame = ttk.LabelFrame(self, text="Crear Ejercicio", padding=(20, 10))
        labels_ejercicio = ["Nombre:", "Descripción:", "Grupo Muscular:", "Repeticiones:", "Series:", "Duración (seg):"]
        entries_ejercicio = [ttk.Entry(self.form_crear_ejercicio_frame) for _ in labels_ejercicio]
        (self.entry_ejercicio_nombre, self.entry_ejercicio_desc, self.entry_ejercicio_musculo, self.entry_ejercicio_rep, self.entry_ejercicio_series, self.entry_ejercicio_duracion) = entries_ejercicio

        for i, (text, widget) in enumerate(zip(labels_ejercicio, entries_ejercicio)):
            ttk.Label(self.form_crear_ejercicio_frame, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

        self.form_crear_ejercicio_frame.columnconfigure(1, weight=1)
        ttk.Button(self.form_crear_ejercicio_frame, text="Guardar Ejercicio", command=self.guardar_nuevo_ejercicio).grid(row=len(labels_ejercicio), column=0, columnspan=2, pady=10)
        ttk.Button(self.form_crear_ejercicio_frame, text="Cancelar", command=self.ocultar_form_crear_ejercicio).grid(row=len(labels_ejercicio) + 1, column=0, columnspan=2, pady=5)

        self.vista_ejercicios_frame = ttk.LabelFrame(self, text="Ejercicios Creados", padding=(10, 5))
        self.vista_ejercicios_frame.pack(padx=10, pady=10, fill="both", expand=True)

        search_frame_ejercicios = ttk.Frame(self.vista_ejercicios_frame)
        search_frame_ejercicios.pack(fill='x', padx=5, pady=5)

        entry_buscar_ejercicio = ttk.Entry(search_frame_ejercicios)
        entry_buscar_ejercicio.pack(side='left', fill='x', expand=True)

        btn_buscar_ejercicio = ttk.Button(search_frame_ejercicios, text="Buscar 🔎", command=self.buscar_ejercicios)
        btn_buscar_ejercicio.pack(side='right', padx=(5, 0))

        columns_ejercicios = ('id', 'nombre', 'grupo_muscular', 'series_reps', 'duracion')
        self.tree_ejercicios = ttk.Treeview(self.vista_ejercicios_frame, columns=columns_ejercicios, show='headings')
        self.tree_ejercicios.heading('id', text='ID')
        self.tree_ejercicios.heading('nombre', text='Nombre')
        self.tree_ejercicios.heading('grupo_muscular', text='Grupo Muscular')
        self.tree_ejercicios.heading('series_reps', text='Series x Reps')
        self.tree_ejercicios.heading('duracion', text='Duración')
        self.tree_ejercicios.column('id', width=50, anchor=tk.CENTER)
        self.tree_ejercicios.column('series_reps', width=50, anchor=tk.CENTER)
        self.tree_ejercicios.column('duracion', width=50, anchor=tk.CENTER)
        self.tree_ejercicios.pack(fill="both", expand=True)

        btn_borrar_ejercicio = ttk.Button(self.vista_ejercicios_frame, text="Borrar Ejercicio Seleccionado", command=self.borrar_ejercicio_seleccionado, style="Baja.TButton")
        btn_borrar_ejercicio.pack(pady=5)

    def actualizar_vista_ejercicios(self):
        """Limpia y actualiza la tabla de ejercicios."""
        for item in self.tree_ejercicios.get_children():
            self.tree_ejercicios.delete(item)
        for ej in self.ejercicios_creados:
            self.tree_ejercicios.insert("", tk.END, values=(ej.id_ejercicio, ej.nombre, ej.grupo_muscular, f"{ej.series}x{ej.repeticiones}", f"{ej.duracion_segundos} seg"))

    def mostrar_form_crear_ejercicio(self):
        self.btn_crear_ejercicio.pack_forget()
        self.vista_ejercicios_frame.pack_forget()
        self.form_crear_ejercicio_frame.pack(padx=10, pady=10, fill="x")

    def ocultar_form_crear_ejercicio(self):
        self.form_crear_ejercicio_frame.pack_forget()
        self.btn_crear_ejercicio.pack(pady=10)
        self.vista_ejercicios_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def guardar_nuevo_ejercicio(self):
        nombre = self.entry_ejercicio_nombre.get()
        descripcion = self.entry_ejercicio_desc.get()
        grupo_muscular = self.entry_ejercicio_musculo.get()
        repeticiones = self.entry_ejercicio_rep.get()
        series = self.entry_ejercicio_series.get()
        duracion = self.entry_ejercicio_duracion.get()

        if not all([nombre, grupo_muscular, repeticiones, series, duracion]):
            messagebox.showerror("Error", "Los campos Nombre, Grupo Muscular, Repeticiones, Series y Duración son obligatorios.")
            return

        id_ejercicio = len(self.ejercicios_creados) + 1
        nuevo_ejercicio = Ejercicio(id_ejercicio, nombre, descripcion, grupo_muscular, repeticiones, series, duracion)
        self.ejercicios_creados.append(nuevo_ejercicio)

        messagebox.showinfo("Éxito", f"Ejercicio '{nombre}' creado correctamente.")
        for entry in [self.entry_ejercicio_nombre, self.entry_ejercicio_desc, self.entry_ejercicio_musculo, self.entry_ejercicio_rep, self.entry_ejercicio_series, self.entry_ejercicio_duracion]:
            entry.delete(0, tk.END)
        self.ocultar_form_crear_ejercicio()
        self.actualizar_vista_ejercicios()

    def borrar_ejercicio_seleccionado(self):
        """Borra el ejercicio seleccionado en la tabla Treeview."""
        selected_item = self.tree_ejercicios.focus()  # Obtiene el item seleccionado
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un ejercicio para borrar.")
            return

        # Pedir confirmación al usuario
        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar el ejercicio seleccionado?"):
            return

        item_values = self.tree_ejercicios.item(selected_item, 'values')
        id_ejercicio_a_borrar = int(item_values[0])

        # Encontrar y eliminar el ejercicio de la lista de datos
        ejercicio_a_borrar = next((ej for ej in self.ejercicios_creados if ej.id_ejercicio == id_ejercicio_a_borrar), None)
        
        if ejercicio_a_borrar:
            self.ejercicios_creados.remove(ejercicio_a_borrar)
            messagebox.showinfo("Éxito", f"Ejercicio '{ejercicio_a_borrar.nombre}' borrado correctamente.")
            self.actualizar_vista_ejercicios()  # Actualiza la tabla para reflejar el cambio

    def buscar_ejercicios(self):
        """Filtra la tabla de ejercicios según el término de búsqueda."""
        termino_busqueda = self.entry_buscar_ejercicio.get().lower()

        for item in self.tree_ejercicios.get_children():
            self.tree_ejercicios.delete(item)

        if not termino_busqueda:
            self.actualizar_vista_ejercicios()
            return

        for ej in self.ejercicios_creados:
            if termino_busqueda in str(ej.id_ejercicio).lower() or \
            termino_busqueda in str(ej.nombre).lower() or \
            termino_busqueda in str(ej.grupo_muscular).lower():
                self.tree_ejercicios.insert("", tk.END, values=(ej.id_ejercicio, ej.nombre, ej.grupo_muscular, f"{ej.series}x{ej.repeticiones}", f"{ej.duracion_segundos} seg"))
    