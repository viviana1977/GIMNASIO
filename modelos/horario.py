class Horario:
    def __init__(self, id_dias, dia_semana, hora_inicio, hora_final):   
        self.id_dias = id_dias
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
    def agregar_clase(self, clase, dia_semana, hora_inicio, hora_final):
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        print(f"clase agregado: {dia_semana} de {hora_inicio} a {hora_final}.")
    def eliminar_clase(self, clases, dia_semana, hora_inicio, hora_final):
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        print(f"clase eliminado: {dia_semana} de {hora_inicio} a {hora_final}.")

    def agregar_socio(self, socio):
        self.socio = socio
        print(f"El socio {socio.nombre_apellido} ha sido agregado al horario.")
    def eliminar_socio(self, socio):
        self.socio = socio
        print(f"El socio {socio.nombre_apellido} ha sido eliminado del horario.")
    def agregar_instructor(self, instructor):
        self.instructor = instructor
        print(f"El instructor {instructor.nombre} ha sido agregado al horario.")    
