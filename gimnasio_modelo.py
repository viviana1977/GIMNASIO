class Socio: 
    def __init__(self, id_socio, nombre_apellido, dni, direccion, fecha_nacimiento, telefono, email, fecha_registro,
                talle, peso, objetivo):
        self.id_socio = id_socio
        self.nombre_apellido = nombre_apellido
        self.dni = dni 
        self.direccion = direccion
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.email= email
        self.fecha_registro= fecha_registro
        self.talle = talle
        self.peso = peso
        self.objetivo = objetivo

        if rutina( self, rutina):
            self.rutina = []
            self.clases = []

    def registrar_rutina(self, rutina):
        self.rutina.append(rutina)
        if rutina( self, rutina):
            self.rutina = []
            self.rutina.append(rutina)

    def registrar_clase(self, clases):
        self.clases.append(clases)
        if clases( self, clases):
            self.clases = []
            self.clases.append(clases)

    def modificar_datos(self, nombre_apellido=None, direccion=None, telefono=None, email=None, talle=None, peso=None, objetivo=None):
        if nombre_apellido:
            self.nombre_apellido = nombre_apellido
        if direccion:
            self.direccion = direccion
        if telefono:
            self.telefono = telefono
        if email:
            self.email = email
        if talle:
            self.talle = talle
        if peso:
            self.peso = peso
        if objetivo:
            self.objetivo = objetivo
            self.rutina = []
            self.clases = []

    def cancelar_membresia(self):
        self.rutina = []
        self.clases = []
        print(f"La membresía del socio {self.nombre_apellido} ha sido cancelada.")

    def ingresar_cuota_abonada(self, monto):
        self.cuota_abonada = monto
        print(f"El socio {self.nombre_apellido} ha abonado la cuota de {monto}.")
        print(f"El socio {self.nombre_apellido} está inscripto en la clase {self.clases}.")

class rutina:
    def __init__(self, id_rutina, tipo, ejercicio, duracion):
        self.id_rutina = id_rutina
        self.tipo = tipo
        self.ejercicio = ejercicio
        self.duracion = duracion

    def asignar_ejercicio(self, ejercicio):
        self.ejercicio.append(ejercicio)
        print(f"Ejercicio {ejercicio} asignado a la rutina {self.id_rutina}.")
        print(f"Ejercicios en la rutina {self.id_rutina}: {self.ejercicio}")
        

class equipamiento:
    def __init__(self, id_equipamiento, capacidad, tipo_maquina, musculos,estado):
        self.id_equipamiento = id_equipamiento
        self.capacidad = capacidad
        self.tipo_maquina = tipo_maquina
        self.musculos = musculos
        self.estado = estado
    def habilitar_deshabilitar(self, estado):
        self.estado = estado
        print(f"El equipamiento {self.tipo_maquina} ha sido {estado}.")
    def agregar_peso(self, peso):
        self.peso = peso
        print(f"Se ha agregado {peso} al equipamiento {self.tipo_maquina}.")
    def quitar_peso(self, peso):
        self.peso = peso
        print(f"Se ha quitado {peso} del equipamiento {self.tipo_maquina}.")
            
class clases:
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
    

class horarios:
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


class instructor:
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