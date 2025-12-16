import sqlite3

class Clases:
    def __init__(self, id_clase, tipo, nombre):
        self.id_clase = id_clase
        self.tipo = tipo
        self.nombre = nombre

    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        if self.id_clase:
            sql = '''
            UPDATE clases
            SET tipo = ?, nombre = ?
            WHERE id_clase = ?
            '''
            parametros = (self.tipo, self.nombre, self.id_clase)
        else:
            sql = '''
            INSERT INTO clases (tipo, nombre) 
            VALUES (?, ?)
            '''
            parametros = (self.tipo, self.nombre)
        
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

        for row in cursor.fetchall():
            clase_obj = cls(row[0], row[1], row[2]) 
            clases.append(clase_obj)
        conn.close()

        return clases
    
    def eliminar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        DELETE FROM clases
        WHERE id_clase = ?
        '''

        cursor.execute(sql, (self.id_clase,))
        conn.commit()
        conn.close()

    @classmethod
    def obtener_por_id(cls, id_clase):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        SELECT * FROM clases
        WHERE id_clase = ?
        '''

        cursor.execute(sql, (id_clase,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(row[0], row[1], row[2])
        else:
            return None