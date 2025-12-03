import sqlite3
mi_conexion = sqlite3.connect('gimnasio.db')
cursor = mi_conexion.cursor()
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS "telefonos" (
        "id_telefono" INTEGER NOT NULL UNIQUE,
        "nro_telefono" TEXT,
        PRIMARY KEY("id_telefono")
    );

    CREATE TABLE IF NOT EXISTS "socios" (
        "id_socio" INTEGER NOT NULL UNIQUE,
        "nombre_y_apellido" TEXT,
        "dni" TEXT,
        "direccion" TEXT,
        "fnac" TEXT,
        "id_telefono" INTEGER NOT NULL UNIQUE,
        "email" TEXT,
        "talla" TEXT,
        "peso" TEXT,
        "objetivo" TEXT,
        "id_rutina" INTEGER NOT NULL,
        PRIMARY KEY("id_socio"),
        FOREIGN KEY ("id_telefono") REFERENCES "telefonos"("id_telefono")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("id_rutina") REFERENCES "rutinas"("id-rutina")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "rutinas" (
        "id-rutina" INTEGER NOT NULL UNIQUE,
        "tipo" TEXT,
        "duracion" TEXT,
        PRIMARY KEY("id-rutina"),
        FOREIGN KEY ("id-rutina") REFERENCES "rutina_clase"("id_rutina")
        ON UPDATE NO ACTION ON DELETE NO ACTION
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
        "nombre" TEXT,
        "tipo" TEXT,
        "capacidad" TEXT,
        PRIMARY KEY("id_clase")
    );

    CREATE TABLE IF NOT EXISTS "clases_horarios" (
        "id_clase_horario" INTEGER NOT NULL UNIQUE,
        "id_clase" INTEGER,
        "id_horario" INTEGER,
        PRIMARY KEY("id_clase_horario"),
        FOREIGN KEY ("id_clase") REFERENCES "clases"("id_clase")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("id_horario") REFERENCES "horarios"("id_horarios")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "horarios" (
        "id_horarios" INTEGER NOT NULL UNIQUE,
        "dias" TEXT,
        "horario_inicio" TEXT,
        "Horario_final" TEXT,
        PRIMARY KEY("id_horarios")
    );

    CREATE TABLE IF NOT EXISTS "instructor_horario" (
        "id_instructor_horario" INTEGER NOT NULL UNIQUE,
        "id_instructor" INTEGER,
        "id_horario" INTEGER,
        PRIMARY KEY("id_instructor_horario"),
        FOREIGN KEY ("id_instructor") REFERENCES "instructor"("id_instructor")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("id_horario") REFERENCES "horarios"("id_horarios")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "horarios" (
        "id_horario" INTEGER NOT NULL UNIQUE,
        PRIMARY KEY("id_horario")
    );

    CREATE TABLE IF NOT EXISTS "instructor" (
        "id_instructor" INTEGER NOT NULL UNIQUE,
        "nombre" TEXT,
        "direccion" TEXT,
        "telefono" TEXT,
        "sueldo" INTEGER,
        PRIMARY KEY("id_instructor")
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