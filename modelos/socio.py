import sqlite3

class Socio: 
    def __init__(self, id_socio, nombre_apellido, dni, direccion, fecha_nacimiento, email,
                telefono, talla, peso, objetivo):
        self.id_socio = id_socio
        self.nombre_apellido = nombre_apellido
        self.dni = dni 
        self.direccion = direccion
        self.fecha_nacimiento = fecha_nacimiento
        self.email= email
        self.telefono = telefono
        self.talla = talla
        self.peso = peso
        self.objetivo = objetivo
        self.rutina = []

    def registrar_rutina(self, rutina):
        self.rutina.append(rutina)

    def modificar_datos(self, nombre_apellido=None, direccion=None, telefono=None, email=None, talla=None, peso=None, objetivo=None):
        if nombre_apellido:
            self.nombre_apellido = nombre_apellido
        if direccion:
            self.direccion = direccion
        if telefono:
            self.telefono = telefono
        if email:
            self.email = email
        if talla:
            self.talla = talla
        if peso:
            self.peso = peso
        if objetivo:
            self.objetivo = objetivo

    def guardar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()
        
        if self.id_socio:
            sql = '''
            UPDATE socios 
            SET nombre_y_apellido = ?, dni = ?, direccion = ?, telefono = ?, fnac = ?, email = ?, talla = ?, peso = ?, objetivo = ?
            WHERE id_socio = ?
            '''
            parametros = (self.nombre_apellido, self.dni, self.direccion, self.telefono, self.fecha_nacimiento, self.email, self.talla, self.peso, self.objetivo, self.id_socio)
        else:
            sql = '''
            INSERT INTO socios (nombre_y_apellido, dni, direccion, telefono, fnac, email, talla, peso, objetivo) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            parametros = (self.nombre_apellido, self.dni, self.direccion, self.telefono, self.fecha_nacimiento, self.email, self.talla, self.peso, self.objetivo)
        
        cursor.execute(sql,parametros)
        conn.commit()
        conn.close()
    
    @classmethod
    def obtener_todos(cls):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        SELECT * FROM socios
        '''
        cursor.execute(sql)
        socios = []
        for row in cursor.fetchall():
            socio = cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            socios.append(socio)
        conn.close()

        return socios
    
    def eliminar(self):
        conn = sqlite3.connect('gimnasio.db')
        cursor = conn.cursor()

        sql = '''
        DELETE FROM socios
        WHERE id_socio = ?
        '''

        cursor.execute(sql, (self.id_socio,))
        conn.commit()
        conn.close()