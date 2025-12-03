from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime
import gimnasio_modelo as gc

class VistaSocio(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Socio")
        self.socios_creados = []

        # --- Formulario de Registro de Socios ---
        # Se crea el frame del formulario pero no se muestra inicialmente (sin .pack())
        self.form_frame = ttk.LabelFrame(self, text="Registrar Nuevo Socio", padding=(20, 10))

        self.btn_alta_socio = ttk.Button(self, text="Alta Socio", command=self.mostrar_formulario_alta, style="Alta.TButton")
        self.btn_alta_socio.pack(pady=20)

        # Creación de etiquetas y campos de entrada
        labels = ["Nombre y Apellido:", "DNI:", "Dirección:", "Fecha Nacimiento (DD/MM/AAAA):", "Teléfono:", "Email:", "Talle:", "Peso (kg):", "Objetivo:"]
        entries = []

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.form_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries.append(entry)

        # Asignar variables a los campos de entrada para fácil acceso
        (self.entry_nombre, self.entry_dni, self.entry_direccion, self.entry_fecha_nac, 
        self.entry_telefono, self.entry_email, self.entry_talle, self.entry_peso, self.entry_objetivo) = entries

        # Configurar la columna de los campos de entrada para que se expanda
        self.form_frame.columnconfigure(1, weight=1)

        # --- Botones del formulario ---
        self.btn_registrar = ttk.Button(self.form_frame, text="Registrar Socio", command=self.registrar_nuevo_socio)
        self.btn_registrar.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.btn_cancelar = ttk.Button(self.form_frame, text="Cancelar", command=self.ocultar_formulario_alta)
        self.btn_cancelar.grid(row=len(labels) + 1, column=0, columnspan=2, pady=5)


        # --- Vista de Socios Registrados ---
        self.vista_socios_frame = ttk.LabelFrame(self, text="Socios Registrados", padding=(10, 5))
        self.vista_socios_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Widget de Búsqueda ---
        search_frame = ttk.Frame(self.vista_socios_frame)
        search_frame.pack(fill='x', padx=5, pady=5)

        self.entry_buscar_socio = ttk.Entry(search_frame)
        self.entry_buscar_socio.pack(side='left', fill='x', expand=True)

        btn_buscar_socio = ttk.Button(search_frame, text="Buscar 🔎", command=self.buscar_socios)
        btn_buscar_socio.pack(side='right', padx=(5, 0))

        columns_socios = ('id', 'nombre', 'dni', 'telefono')
        self.tree_socios = ttk.Treeview(self.vista_socios_frame, columns=columns_socios, show='headings')
        self.tree_socios.heading('id', text='ID')
        self.tree_socios.heading('nombre', text='Nombre y Apellido')
        self.tree_socios.heading('dni', text='DNI')
        self.tree_socios.heading('telefono', text='Teléfono')
        self.tree_socios.column('id', width=50, anchor=tk.CENTER)
        self.tree_socios.pack(fill="both", expand=True)

        btn_borrar_socio = ttk.Button(self.vista_socios_frame, text="Borrar Socio Seleccionado", command=self.borrar_socio_seleccionado, style="Baja.TButton")
        btn_borrar_socio.pack(pady=5)

        # --- Botones ---
        # Botones del formulario (se crean pero no se muestran)
        self.btn_registrar = ttk.Button(self, text="Registrar Socio", command=self.registrar_nuevo_socio)
        self.btn_cancelar = ttk.Button(self, text="Cancelar", command=self.ocultar_formulario_alta)

    def actualizar_vista_socios(self):
        """Limpia y actualiza la tabla de socios."""
        for item in self.tree_socios.get_children():
            self.tree_socios.delete(item)
        for socio in self.socios_creados:
            self.tree_socios.insert("", tk.END, values=(socio.id_socio, socio.nombre_apellido, socio.dni, socio.telefono))

    def mostrar_formulario_alta(self):
        """Muestra el formulario de registro y oculta el botón 'Alta'."""
        self.btn_alta_socio.pack_forget()
        self.vista_socios_frame.pack_forget()
        self.form_frame.pack(padx=10, pady=10, fill="x")
        self.btn_registrar.pack(pady=10)
        self.btn_cancelar.pack(pady=5)

    def ocultar_formulario_alta(self):
        """Oculta el formulario de registro y vuelve a mostrar el botón 'Alta'."""
        self.btn_alta_socio.pack(pady=20)
        self.form_frame.pack_forget()
        self.btn_registrar.pack_forget()
        self.btn_cancelar.pack_forget()
        self.vista_socios_frame.pack(padx=10, pady=10, fill="both", expand=True)


    def registrar_nuevo_socio(self):
        """Captura datos del formulario y crea un nuevo objeto Socio."""
        nombre = self.entry_nombre.get()
        dni = self.entry_dni.get()
        direccion = self.entry_direccion.get()
        fecha_nac = self.entry_fecha_nac.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()
        talle = self.entry_talle.get()
        peso = self.entry_peso.get()
        objetivo = self.entry_objetivo.get()

        # Validación simple
        if not all([nombre, dni, direccion, fecha_nac, telefono, email, talle, peso, objetivo]):
            messagebox.showerror("Error de validación", "Todos los campos son obligatorios.")
            return

        # Crear y guardar el nuevo socio
        id_socio = len(self.socios_creados) + 1
        fecha_registro = datetime.now().strftime("%d/%m/%Y")
        nuevo_socio = gc.Socio(id_socio, nombre, dni, direccion, fecha_nac, telefono, email, fecha_registro, talle, peso, objetivo)
        self.socios_creados.append(nuevo_socio)
        
        messagebox.showinfo("Registro Exitoso", f"Socio {nombre} registrado correctamente.")
        
        # Limpiar campos del formulario
        for entry in [self.entry_nombre, self.entry_dni, self.entry_direccion, self.entry_fecha_nac, self.entry_telefono, self.entry_email, self.entry_talle, self.entry_peso, self.entry_objetivo]:
            entry.delete(0, tk.END)
        
        self.ocultar_formulario_alta()
        self.actualizar_vista_socios()

    def borrar_socio_seleccionado(self):
        """Borra el socio seleccionado en la tabla Treeview."""
        selected_item = self.tree_socios.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un socio para borrar.")
            return

        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar el socio seleccionado?"):
            return

        item_values = self.tree_socios.item(selected_item, 'values')
        id_a_borrar = int(item_values[0])

        socio_a_borrar = next((s for s in self.socios_creados if s.id_socio == id_a_borrar), None)
        
        if socio_a_borrar:
            self.socios_creados.remove(socio_a_borrar)
            messagebox.showinfo("Éxito", f"Socio '{socio_a_borrar.nombre_apellido}' borrado correctamente.")
            self.actualizar_vista_socios()

    def buscar_socios(self):
        """Filtra la tabla de socios según el término de búsqueda."""
        termino_busqueda = self.entry_buscar_socio.get().lower()

        # Limpiar la tabla antes de mostrar los resultados
        for item in self.tree_socios.get_children():
            self.tree_socios.delete(item)

        # Si no hay término de búsqueda, mostrar todos y salir
        if not termino_busqueda:
            self.actualizar_vista_socios()
            return

        # Filtrar y mostrar resultados
        for socio in self.socios_creados:
            # Convertimos todos los valores a string y minúsculas para una búsqueda flexible
            if termino_busqueda in str(socio.id_socio).lower() or \
            termino_busqueda in str(socio.nombre_apellido).lower() or \
            termino_busqueda in str(socio.dni).lower() or \
            termino_busqueda in str(socio.telefono).lower():
                self.tree_socios.insert("", tk.END, values=(socio.id_socio, socio.nombre_apellido, socio.dni, socio.telefono))
