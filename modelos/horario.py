import sqlite3

class Horario:
    def __init__(self, id_horario, dia_semana, hora_inicio, hora_final, id_instructor=None, id_clase=None):   
        self.id_horario = id_horario
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.id_instructor = id_instructor
        self.id_clase = id_clase


    @classmethod
    def obtener_todos_con_relaciones(cls):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        SELECT h.id_horario, h.dia_semana, h.hora_inicio, h.hora_final, h.id_instructor, h.id_clase, i.nombre AS nombre_instructor, c.nombre AS nombre_clase
        FROM horarios h
        LEFT JOIN instructores i ON h.id_instructor = i.id_instructor
        LEFT JOIN clases c ON h.id_clase = c.id_clase
        '''
        cursor.execute(sql)
        horarios = []
        for row in cursor.fetchall():
            horario_obj = cls(row[0], row[1], row[2], row[3], row[4], row[5])
            horario_obj.nombre_instructor = row[6]
            horario_obj.nombre_clase = row[7]
            horarios.append(horario_obj)
        conn.close()

        return horarios

    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()
        
        if self.id_horario:
            sql = '''
            UPDATE horarios SET dia_semana = ?, hora_inicio = ?, hora_final = ?, id_instructor = ?, id_clase = ?
            WHERE id_horario = ?
            '''

            parametros = (self.dia_semana, self.hora_inicio, self.hora_final, self.id_horario, self.id_instructor, self.id_clase)
        else:
            sql = '''
            INSERT INTO horarios (dia_semana, hora_inicio, hora_final, id_instructor, id_clase) 
            VALUES (?, ?, ?, ?, ?)
            '''
            parametros = (self.dia_semana, self.hora_inicio, self.hora_final, self.id_instructor, self.id_clase)
        
        cursor.execute(sql,parametros)
        conn.commit()
        conn.close() 
                    
    @classmethod
    def obtener_todos(cls):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        SELECT * FROM horarios
        '''
        cursor.execute(sql)
        horarios = []
        # La tabla horarios tiene 4 columnas: id_horarios, dia_semana, hora_inicio, hora_final
        for row in cursor.fetchall():
            # El constructor es (id, dia, inicio, fin)
            horario_obj = cls(row[0], row[1], row[2], row[3])
            horarios.append(horario_obj)
        conn.close()

        return horarios
    
    def eliminar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        DELETE FROM horarios 
        WHERE id_horario = ?
        '''
        cursor.execute(sql, (self.id_horario,))
        conn.commit()
        conn.close()