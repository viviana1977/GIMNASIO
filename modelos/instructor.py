import sqlite3

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

    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()
        
        if self.id_instructor:
            sql = '''
            UPDATE instructores 
            SET nombre = ?, direccion = ?, telefono = ?, sueldo = ?
            WHERE id_instructor = ?
            '''
            parametros = (self.nombre, self.direccion, self.telefono, self.sueldo, self.id_instructor)
        else:
            sql = '''
            INSERT INTO instructores (nombre, direccion, telefono, sueldo)
            VALUES (?, ?, ?, ?)
            '''
            parametros = (self.nombre, self.direccion, self.telefono, self.sueldo)
        
        cursor.execute(sql,parametros)
        conn.commit()
        conn.close()
    
    @classmethod
    def obtener_todos(cls):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        SELECT * FROM instructores
        '''
        cursor.execute(sql)
        instructores = []
        for row in cursor.fetchall():
            instructor = cls(row[0], row[1], row[2], row[3], row[4])
            instructores.append(instructor)
        conn.close()

        return instructores
    
    def eliminar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        DELETE FROM instructores
        WHERE id_instructor = ?
        '''

        cursor.execute(sql, (self.id_instructor,))
        conn.commit()
        conn.close()