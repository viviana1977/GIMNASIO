class Socio: 
    def __init__(self, id_socio, nombre_apellido, direccion, fecha_nacimiento, telefono, email, fecha_registro,
                talle, peso, objetivo):
        self.id_socio = id_socio
        self.nombre_apellido = nombre_apellido
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

        if equipamiento == "en uso":
            



class clases:
    def __init__(self, id_clase, tipo, capacidad, nombres):
        self.id_clase = id_clase
        self.tipo = tipo
        self.capacidad = capacidad
        self.nombres = nombres


class horarios:
    def __init__(self, id_dias, dia_semana, hora_inicio, hora_final):   
        self.id_dias = id_dias
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final


class instructor:
    def __init__(self, id_instructor, nombre, direccion, telefono, sueldo):
        self.id_instructor = id_instructor
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.sueldo = sueldo    