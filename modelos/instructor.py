class Instructor:
    def __init__(self, id_instructor, nombre, direccion, telefono, sueldo):
        self.id_instructor = id_instructor
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.sueldo = sueldo
    def agregar_clase(self, clases):
        self.clases = clases
        print(f"El instructor {self.nombre} ha sido asignado a la clase {clases.tipo}.")
    def modificar_clase(self, clases):
        self.clases = clases
        print(f"El instructor {self.nombre} ha modificado la clase a {clases.tipo}.")
    def eliminar_clase(self, clases):
        self.clases = clases
        print(f"El instructor {self.nombre} ha eliminado la clase {clases.tipo}.")