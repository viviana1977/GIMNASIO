from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime
from modelos import Equipamiento

class VistaEquipamiento(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Equipamiento")
        self.equipos_creados = []

        self.form_agregar_equipo_frame = ttk.LabelFrame(self,text="Agregar Nuevo Equipamiento", padding=(20, 10))
        labels_equipo = {"Tipo de Máquina:": 0, "Capacidad:": 1, "Músculos que trabaja:": 2, "Estado Inicial:": 3}
        entry_equipo_tipo = ttk.Entry(self.form_agregar_equipo_frame)
        entry_equipo_capacidad = ttk.Entry(self.form_agregar_equipo_frame)
        entry_equipo_musculos = ttk.Entry(self.form_agregar_equipo_frame)
        combo_equipo_estado = ttk.Combobox(self.form_agregar_equipo_frame, values=["Habilitado", "Deshabilitado"], state="readonly")

        for i, (text, widget) in enumerate(zip(labels_equipo.keys(), [entry_equipo_tipo, entry_equipo_capacidad, entry_equipo_musculos, combo_equipo_estado])):
            ttk.Label(self.form_agregar_equipo_frame, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

        self.form_agregar_equipo_frame.columnconfigure(1, weight=1)
        btn_guardar_equipo = ttk.Button(self.form_agregar_equipo_frame, text="Guardar Equipo", command=self.guardar_nuevo_equipo)
        btn_guardar_equipo.grid(row=4, column=0, columnspan=2, pady=10)
        btn_cancelar_equipo = ttk.Button(self.form_agregar_equipo_frame, text="Cancelar", command=self.ocultar_form_agregar_equipo)
        btn_cancelar_equipo.grid(row=5, column=0, columnspan=2, pady=5)

        # --- Vista de Equipos Registrados ---
        self.vista_equipos_frame = ttk.LabelFrame(self, text="Equipos Registrados", padding=(10, 5))
        self.vista_equipos_frame.pack(padx=10, pady=10, fill="both", expand=True)

        search_frame_equipos = ttk.Frame(self.vista_equipos_frame)
        search_frame_equipos.pack(fill='x', padx=5, pady=5)

        entry_buscar_equipo = ttk.Entry(search_frame_equipos)
        entry_buscar_equipo.pack(side='left', fill='x', expand=True)

        btn_buscar_equipo = ttk.Button(search_frame_equipos, text="Buscar 🔎", command=self.buscar_equipos)
        btn_buscar_equipo.pack(side='right', padx=(5, 0))

        columns_equipos = ('id', 'tipo', 'musculos', 'estado')
        tree_equipos = ttk.Treeview(self.vista_equipos_frame, columns=columns_equipos, show='headings')
        tree_equipos.heading('id', text='ID')
        tree_equipos.heading('tipo', text='Tipo de Máquina')
        tree_equipos.heading('musculos', text='Músculos')
        tree_equipos.heading('estado', text='Estado')
        tree_equipos.column('id', width=50, anchor=tk.CENTER)
        tree_equipos.pack(fill="both", expand=True)

        self.btn_agregar_equipo = ttk.Button(self.vista_equipos_frame, text="Crear Equipamiento", command=self.mostrar_form_crear_equipo)
        self.btn_agregar_equipo.pack(pady=10, side=tk.LEFT)

        self.btn_modificar_equipo = ttk.Button(self.vista_equipos_frame, text="Modificar Equipamiento", command=self.mostrar_form_crear_equipo)
        self.btn_modificar_equipo.pack(pady=10, side=tk.LEFT, padx=5)

        btn_borrar_equipo = ttk.Button(self.vista_equipos_frame, text="Borrar Equipamiento", command=self.borrar_equipo)
        btn_borrar_equipo.pack(pady=10, side=tk.LEFT)
    
    def actualizar_vista_equipos(self):
        """Limpia y actualiza la tabla de equipos."""
        for item in self.tree_equipos.get_children():
            self.tree_equipos.delete(item)
        for eq in self.equipos_creados:
            self.tree_equipos.insert("", tk.END, values=(eq.id_equipamiento, eq.tipo_maquina, eq.musculos, eq.estado))
    
        # También actualiza el combo de la pestaña rutina si es necesario
        # (Aunque no se usa directamente, es buena práctica mantenerlo)
        nombres_equipos = [f"ID {e.id_equipamiento}: {e.tipo_maquina}" for e in self.equipos_creados]
        # combo_equipos_gestion['values'] = nombres_equipos


    def mostrar_form_crear_equipo(self):
        """Muestra el formulario para agregar un nuevo equipo."""
        self.btn_agregar_equipo.pack_forget()
        self.form_agregar_equipo_frame.pack(padx=10, pady=10, fill="x")
        self.vista_equipos_frame.pack_forget()

    def ocultar_form_agregar_equipo(self):
        """Oculta el formulario de agregación y muestra los otros widgets."""
        self.form_agregar_equipo_frame.pack_forget()
        self.pack(pady=10)
        self.vista_equipos_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def guardar_nuevo_equipo(self):
        """Crea un nuevo objeto equipamiento y lo guarda."""
        tipo_maquina = self.entry_equipo_tipo.get()
        capacidad = self.entry_equipo_capacidad.get()
        musculos = self.entry_equipo_musculos.get()
        estado = self.combo_equipo_estado.get()

        if not all([tipo_maquina, capacidad, musculos, estado]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        id_equipo = len(self.equipos_creados) + 1
        nuevo_equipo = Equipamiento(id_equipo, capacidad, tipo_maquina, musculos, estado)
        self.equipos_creados.append(nuevo_equipo)

        messagebox.showinfo("Éxito", f"Equipo '{tipo_maquina}' agregado correctamente.")
        print(f"Nuevo equipo agregado: ID={nuevo_equipo.id_equipamiento}, Tipo={nuevo_equipo.tipo_maquina}, Estado={nuevo_equipo.estado}")

        for entry in [self.entry_equipo_tipo, self.entry_equipo_capacidad, self.entry_equipo_musculos]:
            entry.delete(0, tk.END)
        self.ocultar_form_agregar_equipo()
        self.actualizar_vista_equipos()

    def actualizar_estado_equipo(self):
        """Actualiza el estado (habilita/deshabilita) de un equipo seleccionado."""
        seleccion = self.combo_equipos_gestion.get()
        nuevo_estado = self.combo_estado_gestion.get()

        if not seleccion or not nuevo_estado:
            messagebox.showerror("Error", "Debe seleccionar un equipo y un nuevo estado.")
            return

        id_equipo_sel = int(seleccion.split(":")[0].replace("ID ", ""))
        equipo_encontrado = next((e for e in self.equipos_creados if e.id_equipamiento == id_equipo_sel), None)

        if equipo_encontrado:
            equipo_encontrado.habilitar_deshabilitar(nuevo_estado)
            messagebox.showinfo("Éxito", f"El estado de '{equipo_encontrado.tipo_maquina}' ha sido actualizado a '{nuevo_estado}'.")
            print(f"Equipo ID {equipo_encontrado.id_equipamiento} actualizado. Nuevo estado: {equipo_encontrado.estado}")
        else:
            messagebox.showerror("Error", "No se encontró el equipo seleccionado.")

    def borrar_equipo(self):
        """Borra el equipo seleccionado en la tabla Treeview."""
        selected_item = self.tree_equipos.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un equipo para borrar.")
            return

        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar el equipo seleccionado?"):
            return

        item_values = self.tree_equipos.item(selected_item, 'values')
        id_a_borrar = int(item_values[0])

        equipo_a_borrar = next((eq for eq in self.equipos_creados if eq.id_equipamiento == id_a_borrar), None)
        
        if equipo_a_borrar:
            self.equipos_creados.remove(equipo_a_borrar)
            messagebox.showinfo("Éxito", f"Equipo '{equipo_a_borrar.tipo_maquina}' borrado correctamente.")
            self.actualizar_vista_equipos()

    def buscar_equipos(self):
        """Filtra la tabla de equipos según el término de búsqueda."""
        termino_busqueda = self.entry_buscar_equipo.get().lower()

        for item in self.tree_equipos.get_children():
            self.tree_equipos.delete(item)

        if not termino_busqueda:
            self.actualizar_vista_equipos()
            return

        for eq in self.equipos_creados:
            if termino_busqueda in str(eq.id_equipamiento).lower() or \
            termino_busqueda in str(eq.tipo_maquina).lower() or \
            termino_busqueda in str(eq.musculos).lower() or \
            termino_busqueda in str(eq.estado).lower():
                self.tree_equipos.insert("", tk.END, values=(eq.id_equipamiento, eq.tipo_maquina, eq.musculos, eq.estado))
