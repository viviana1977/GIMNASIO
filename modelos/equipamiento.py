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
