from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime
from modelos import Socio

class VistaSocio(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text="Socio")
        self.socios_creados = []
        self.id_socio_a_editar = None

        # --- Formulario de Registro de Socios ---
        # Se crea el frame del formulario pero no se muestra inicialmente (sin .pack())
        self.form_frame = ttk.LabelFrame(self, text="Registrar Nuevo Socio", padding=(20, 10))

        # Creación de etiquetas y campos de entrada
        labels = ["Nombre y Apellido:", "DNI:", "Dirección:", "Fecha Nacimiento (DD/MM/AAAA):", "Email:", "Teléfono:", "Talla:", "Peso (kg):", "Objetivo:"]
        entries = []

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.form_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries.append(entry)

        # Asignar variables a los campos de entrada para fácil acceso
        (self.entry_nombre, self.entry_dni, self.entry_direccion, self.entry_fecha_nac, 
        self.entry_email,self.entry_telefono, self.entry_talla, self.entry_peso, self.entry_objetivo) = entries

        # Configurar la columna de los campos de entrada para que se expanda
        self.form_frame.columnconfigure(1, weight=1)

        # --- Botones del formulario ---
        self.btn_registrar = ttk.Button(self.form_frame, text="Registrar Socio", command=self.guardar_socio)
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

        columns_socios = ('nombre', 'dni', 'telefono', 'email')
        self.tree_socios = ttk.Treeview(self.vista_socios_frame, columns=columns_socios, show='headings')
        self.tree_socios.heading('nombre', text='Nombre y Apellido')
        self.tree_socios.heading('dni', text='DNI')
        self.tree_socios.heading('telefono', text='Teléfono')
        self.tree_socios.heading('email', text='Email')
        self.tree_socios.pack(fill="both", expand=True)

        self.btn_crear_socio = ttk.Button(self.vista_socios_frame, text="Crear Socio", command=self.mostrar_formulario_crear_socio)
        self.btn_crear_socio.pack(pady=10, side=tk.LEFT)

        self.btn_modificar_socio = ttk.Button(self.vista_socios_frame, text="Modificar Socio", command=self.mostrar_formulario_modificar_socio)
        self.btn_modificar_socio.pack(pady=10, side=tk.LEFT, padx=5)

        self.btn_borrar_socio = ttk.Button(self.vista_socios_frame, text="Borrar Socio", command=self.borrar_socio)
        self.btn_borrar_socio.pack(pady=10, side=tk.LEFT)

        self.actualizar_vista_socios()

        
    def actualizar_vista_socios(self):
        """Limpia y actualiza la tabla de socios."""
        for item in self.tree_socios.get_children():
            self.tree_socios.delete(item)

        self.socios_creados = Socio.obtener_todos()
        
        for socio in self.socios_creados:
            self.tree_socios.insert("", tk.END, text=socio.id_socio ,values=(socio.nombre_apellido, socio.dni, socio.telefono, socio.email))

    def mostrar_formulario_crear_socio(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_dni.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_fecha_nac.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_talla.delete(0, tk.END)
        self.entry_peso.delete(0, tk.END)
        self.entry_objetivo.delete(0, tk.END)

        self.form_frame.config(text="Crear Socio")
        self.btn_registrar.config(text="Guardar Socio", command=self.guardar_socio)
        self.id_socio_a_editar = None

        self.form_frame.pack(padx=10, pady=10, fill="x")
        self.vista_socios_frame.pack_forget()

    def mostrar_formulario_modificar_socio(self):
        selected_item = self.tree_socios.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un socio para modificar.")
            return

        id_socio = self.tree_socios.item(selected_item, 'text')
        socio_a_modificar = next((s for s in self.socios_creados if s.id_socio == id_socio), None)

        if not socio_a_modificar:
            messagebox.showerror("Error", "No se encontró el socio seleccionado.")
            return
        
        self.entry_direccion.delete(0, tk.END)
        self.entry_dni.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_fecha_nac.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_objetivo.delete(0, tk.END)
        self.entry_peso.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_talla.delete(0, tk.END)
        
        self.entry_direccion.insert(0, socio_a_modificar.direccion)
        self.entry_dni.insert(0, socio_a_modificar.dni)
        self.entry_email.insert(0, socio_a_modificar.email)
        self.entry_fecha_nac.insert(0, socio_a_modificar.fecha_nacimiento)
        self.entry_nombre.insert(0, socio_a_modificar.nombre_apellido)
        self.entry_objetivo.insert(0, socio_a_modificar.objetivo)
        self.entry_peso.insert(0, socio_a_modificar.peso)
        self.entry_telefono.insert(0, socio_a_modificar.telefono)
        self.entry_talla.insert(0, socio_a_modificar.talla)

        self.id_socio_a_editar = id_socio

        self.form_frame.config(text="Modificar Socio")
        self.btn_registrar.config(text="Actualizar Socio", command=self.actualizar_socio)

        self.form_frame.pack(padx=10, pady=10, fill="x")
        self.vista_socios_frame.pack_forget()

    def ocultar_formulario_alta(self):
        self.id_socio_a_editar = None
        self.form_frame.pack_forget()
        self.vista_socios_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def guardar_socio(self):
        nombre = self.entry_nombre.get()
        dni = self.entry_dni.get()
        direccion = self.entry_direccion.get()
        fecha_nac = self.entry_fecha_nac.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()
        talla = self.entry_talla.get()
        peso = self.entry_peso.get()
        objetivo = self.entry_objetivo.get()

        if not all([nombre, dni, direccion, telefono, fecha_nac, email, talla, peso, objetivo]):
            messagebox.showerror("Error de validación", "Todos los campos son obligatorios.")
            return

        # fecha_registro = datetime.now().strftime("%d/%m/%Y")
        nuevo_socio = Socio(self.id_socio_a_editar, nombre, dni, direccion, fecha_nac, email, telefono, talla, peso, objetivo)
        nuevo_socio.guardar()
        
        messagebox.showinfo("Registro Exitoso", f"Socio {nombre} registrado correctamente.")
        
        # Limpiar campos del formulario
        for entry in [self.entry_nombre, self.entry_dni, self.entry_direccion, self.entry_telefono, self.entry_fecha_nac, self.entry_email, self.entry_talla, self.entry_peso, self.entry_objetivo]:
            entry.delete(0, tk.END)
        
        self.ocultar_formulario_alta()
        self.actualizar_vista_socios()

    def actualizar_socio(self):
        nombre = self.entry_nombre.get()
        dni = self.entry_dni.get()
        direccion = self.entry_direccion.get()
        fecha_nac = self.entry_fecha_nac.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()
        talla = self.entry_talla.get()
        peso = self.entry_peso.get()
        objetivo = self.entry_objetivo.get()

        if not all([nombre, dni, direccion, telefono, fecha_nac, email, talla, peso, objetivo, self.id_socio_a_editar]):
            messagebox.showerror("Error", "Todos los campos son obligatorios y debe haber un socio seleccionado.")
            return

        self.guardar_socio()

    def borrar_socio(self):
        selected_item = self.tree_socios.focus()

        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un socio para borrar.")
            return

        if not messagebox.askyesno("Confirmar Borrado", "¿Está seguro de que desea borrar el socio seleccionado?"):
            return

        id_a_borrar = self.tree_socios.item(selected_item, 'text')

        socio_a_borrar = next((s for s in self.socios_creados if s.id_socio == id_a_borrar), None)
        
        if socio_a_borrar:
            socio_a_borrar.eliminar()
            messagebox.showinfo("Éxito", f"Socio '{socio_a_borrar.nombre_apellido}' borrado correctamente.")
            self.actualizar_vista_socios()

    def buscar_socios(self):
        termino_busqueda = self.entry_buscar_socio.get().lower()

        for item in self.tree_socios.get_children():
            self.tree_socios.delete(item)

        if not termino_busqueda:
            self.actualizar_vista_socios()
            return

        for socio in self.socios_creados:
            if termino_busqueda in str(socio.id_socio).lower() or \
            termino_busqueda in str(socio.nombre_apellido).lower() or \
            termino_busqueda in str(socio.dni).lower() or \
            termino_busqueda in str(socio.telefono).lower():
                self.tree_socios.insert("", tk.END, values=(socio.id_socio, socio.nombre_apellido, socio.dni, socio.telefono))
