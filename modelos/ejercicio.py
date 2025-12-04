class Ejercicio:    
    def __init__(self, id_ejercicio, nombre, descripcion, grupo_muscular, repeticiones, series, duracion_segundos):
        self.id_ejercicio = id_ejercicio
        self.nombre = nombre
        self.descripcion = descripcion
        self.grupo_muscular = grupo_muscular
        self.repeticiones = repeticiones
        self.series = series
        self.duracion_segundos = duracion_segundos

    def mostrar_info(self):
        """Muestra la información completa del ejercicio."""
        print(f"Ejercicio: {self.nombre} (ID: {self.id_ejercicio})")
        print(f"  Descripción: {self.descripcion}")
        print(f"  Grupo Muscular: {self.grupo_muscular}")
        print(f"  Series: {self.series}, Repeticiones: {self.repeticiones}")
        print(f"  Duración Estimada: {self.duracion_segundos} segundos")

    def modificar_ejercicio(self, nombre=None, descripcion=None, grupo_muscular=None, repeticiones=None, series=None, duracion_segundos=None):
        """Permite modificar los atributos del ejercicio."""
        if nombre:
            self.nombre = nombre
        if descripcion:
            self.descripcion = descripcion
        if grupo_muscular:
            self.grupo_muscular = grupo_muscular
        if repeticiones is not None:
            self.repeticiones = repeticiones
        if series is not None:
            self.series = series
        if duracion_segundos is not None:
            self.duracion_segundos = duracion_segundos
        print(f"Ejercicio {self.id_ejercicio} modificado.")
