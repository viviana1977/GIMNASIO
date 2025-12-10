import sqlite3

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

    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()
        
        sql = '''
        INSERT INTO ejercicios (nombre, descripcion, grupo_muscular, repeticiones, series, duracion_segundos) 
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        parametros = (self.nombre, self.descripcion, self.grupo_muscular, self.repeticiones, self.series, self.duracion_segundos)
        
        cursor.execute(sql,parametros)
        conn.commit()
        conn.close()
    
    @classmethod
    def obtener_todos(cls):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        SELECT * FROM ejercicios
        '''
        cursor.execute(sql)
        ejercicios = []
        for row in cursor.fetchall():
            ejercicios = cls(row[0], row[1], row[2], row[3], row[4], row[5])
            ejercicios.append(ejercicios)
        conn.close()

        return ejercicios