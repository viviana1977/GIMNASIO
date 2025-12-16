import sqlite3
mi_conexion = sqlite3.connect('gimnasio.db')
cursor = mi_conexion.cursor()
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS "socios" (
        "id_socio" INTEGER NOT NULL UNIQUE,
        "nombre_y_apellido" TEXT,
        "dni" TEXT,
        "direccion" TEXT,
        "fnac" TEXT,
        "email" TEXT,
        "telefono" TEXT,
        "talla" TEXT,
        "peso" TEXT,
        "objetivo" TEXT,
        "id_rutina" INTEGER,
        PRIMARY KEY("id_socio"),
        FOREIGN KEY ("id_rutina") REFERENCES "rutinas"("id-rutina")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "rutinas" (
        "id-rutina" INTEGER NOT NULL UNIQUE,
        "tipo" TEXT,
        "duracion" TEXT,
        PRIMARY KEY("id-rutina")
    );

    CREATE TABLE IF NOT EXISTS "rutina_clase" (
        "id_rutina_clase" INTEGER NOT NULL UNIQUE,
        "id_rutina" INTEGER NOT NULL UNIQUE,
        "id_clase" INTEGER NOT NULL UNIQUE,
        PRIMARY KEY("id_rutina_clase", "id_rutina", "id_clase"),
        FOREIGN KEY ("id_clase") REFERENCES "clases"("id_clase")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "clases" (
        "id_clase" INTEGER NOT NULL UNIQUE,
        "tipo" TEXT,
        "nombre" TEXT,
        PRIMARY KEY("id_clase")
    );

    CREATE TABLE IF NOT EXISTS "horarios" (
        "id_horario" INTEGER NOT NULL UNIQUE,
        "dia_semana" TEXT,
        "hora_inicio" TEXT,
        "hora_final" TEXT,
        "id_instructor" INTEGER,
        "id_clase" INTEGER,
        PRIMARY KEY("id_horario"),
        FOREIGN KEY ("id_instructor") REFERENCES "instructores"("id_instructor")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY("id_clase") REFERENCES "clases"("id_clase")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "instructores" (
        "id_instructor" INTEGER NOT NULL UNIQUE,
        "nombre" TEXT,
        "direccion" TEXT,
        "telefono" TEXT,
        "sueldo" INTEGER,
        PRIMARY KEY("id_instructor")
    );
                     
    CREATE TABLE IF NOT EXISTS "equipamientos" (
        "id_equipamiento" INTEGER NOT NULL UNIQUE,
        "capacidad" TEXT,
        "musculo" TEXT,
        "estado" TEXT,
        PRIMARY KEY("id_equipamiento")
    );

    CREATE TABLE IF NOT EXISTS "usuarios" (
        "id_usuario" INTEGER PRIMARY KEY AUTOINCREMENT,
        "nombre_usuario" TEXT NOT NULL UNIQUE,
        "contraseña" TEXT NOT NULL,
        "rol" TEXT NOT NULL
    );
''')

cursor.execute("INSERT OR IGNORE INTO usuarios (nombre_usuario, contraseña, rol) VALUES ('dueño', 'dueño123', 'propietario')")
cursor.execute("INSERT OR IGNORE INTO usuarios (nombre_usuario, contraseña, rol) VALUES ('instructor', 'instructor123', 'instructor')")
mi_conexion.commit()
mi_conexion.close()