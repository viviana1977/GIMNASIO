import sqlite3

class Equipamiento:
    def __init__(self, id_equipamiento, capacidad, musculos,estado):
        self.id_equipamiento = id_equipamiento
        self.capacidad = capacidad
        self.musculos = musculos
        self.estado = estado

    def habilitar_deshabilitar(self, estado):
        self.estado = estado

    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()
        
        sql = '''
        INSERT INTO equipamiento(capacidad, musculos, estado) 
        VALUES (?, ?, ?)
        '''
        parametros = (self.capacidad, self.musculos, self.estado)
        
        cursor.execute(sql,parametros)
        conn.commit()
        conn.close()
    
    @classmethod
    def obtener_todos(cls):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        SELECT * FROM Equipamiento
        '''
        cursor.execute(sql)
        Equipamiento = []
        for row in cursor.fetchall():
            Equipamiento = cls(row[0], row[1], row[2], row[3])
            Equipamiento.append(Equipamiento)
        conn.close()

        return Equipamiento