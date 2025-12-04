class Clases:
    def __init__(self, id_clase, tipo, capacidad, nombres):
        self.id_clase = id_clase
        self.tipo = tipo
        self.capacidad = capacidad
        self.nombres = nombres
    
    def iniciar_clase(self):
        print(f"La clase {self.tipo} ha comenzado.")

    def finalizar_clase(self):
        print(f"La clase {self.tipo} ha finalizado.")

    def agregar_eliminar_clase(self, clases):
        self.clases.append(clases)

    def tipo_clase(self, tipo):
        self.tipo = tipo
        print(f"El tipo de clase ha sido cambiado a {tipo}.")
    def agregar_instructor(self, instructor):
        self.instructor = instructor
        print(f"El instructor {instructor.nombre} ha sido asignado a la clase {self.tipo}.")
    def agregar_socio(self, socio):
        self.socio = socio
        print(f"El socio {socio.nombre_apellido} ha sido inscrito en la clase {self.tipo}.")
