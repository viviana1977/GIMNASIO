import sqlite3

class Equipamiento:
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

    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()
        
        sql = '''
        INSERT INTO equipamiento(capacidad, tipo_maquina, musculos, estado) 
        VALUES (?, ?, ?, ?)
        '''
        parametros = (self.capacidad, self.tipo_maquina, self.musculos, self.estado)
        
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