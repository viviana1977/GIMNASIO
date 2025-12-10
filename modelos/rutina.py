import sqlite3

class Rutina:
    def __init__(self, id_rutina, tipo, duracion):
        self.id_rutina = id_rutina
        self.tipo = tipo
        self.ejercicios = []
        self.duracion = duracion

    def asignar_ejercicio(self, ejercicio):
        self.ejercicios.append(ejercicio)
        print(f"Ejercicio {ejercicio} asignado a la rutina {self.id_rutina}.")
        print(f"Ejercicios en la rutina {self.id_rutina}: {self.ejercicios}")
    
    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()
        
        sql = '''
        INSERT INTO Rutina (tipo, ejercicios, duracion) 
        VALUES (?, ?, ?)
        '''
        parametros = (self.tipo, self.ejercicios,self.duracion)
        
        cursor.execute(sql,parametros)
        conn.commit()
        conn.close() 
             
    @classmethod
    def obtener_todos(cls):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        SELECT * FROM rutina
        '''
        cursor.execute(sql)
        rutinas = []
        for row in cursor.fetchall():
            Rutina= cls(row[0], row[1], row[2])
            Rutina.append(Rutina)
        conn.close()

        return Rutina