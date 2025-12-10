import sqlite3

class Clases:
    def __init__(self, id_clase, tipo, capacidad, nombre):
        self.id_clase = id_clase
        self.tipo = tipo
        self.capacidad = capacidad
        self.nombre = nombre
    
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

    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()
        
        sql = '''
        INSERT INTO clases (tipo, capacidad, nombre) 
        VALUES (?, ?, ?)
        '''
        parametros = (self.tipo, self.capacidad, self.nombre)
        
        cursor.execute(sql,parametros)
        conn.commit()
        conn.close()
                  
    @classmethod
    def obtener_todos(cls):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        SELECT * FROM clases
        '''
        cursor.execute(sql)
        clases = []
        # La tabla clases tiene 4 columnas: id_clase, nombre, tipo, capacidad
        for row in cursor.fetchall():
            # Asumiendo que el constructor es (id, tipo, capacidad, nombre)
            clase_obj = cls(row[0], row[2], row[3], row[1]) 
            clases.append(clase_obj)
        conn.close()

        return clases