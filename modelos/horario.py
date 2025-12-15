import sqlite3

class Horario:
    def __init__(self, id_horario, dia_semana, hora_inicio, hora_final):   
        self.id_horario = id_horario
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final

    def agregar_clase(self, clase, dia_semana, hora_inicio, hora_final):
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        print(f"clase agregado: {dia_semana} de {hora_inicio} a {hora_final}.")
    
    def eliminar_clase(self, clases, dia_semana, hora_inicio, hora_final):
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        print(f"clase eliminado: {dia_semana} de {hora_inicio} a {hora_final}.")

    def agregar_socio(self, socio):
        self.socio = socio
        print(f"El socio {socio.nombre_apellido} ha sido agregado al horario.")
    
    def eliminar_socio(self, socio):
        self.socio = socio
        print(f"El socio {socio.nombre_apellido} ha sido eliminado del horario.")
    
    def agregar_instructor(self, instructor):
        self.instructor = instructor
        print(f"El instructor {instructor.nombre} ha sido agregado al horario.")    

    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()
        
        if self.id_horario:
            sql = '''
            UPDATE horarios SET dia_semana = ?, hora_inicio = ?, hora_final = ?
            WHERE id_horario = ?
            '''

            parametros = (self.dia_semana, self.hora_inicio, self.hora_final, self.id_horario)
        else:
            sql = '''
            INSERT INTO horarios (dia_semana, hora_inicio, hora_final) 
            VALUES (?, ?, ?)
            '''
            parametros = (self.dia_semana, self.hora_inicio, self.hora_final)
        
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