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
