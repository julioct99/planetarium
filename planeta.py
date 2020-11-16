import json
from constantes import *


class planeta:
    def __init__(self):
        self.planetas = []
        self.cargar_planetas()

    # Carga todos los astros del json
    def cargar_planetas(self):
        with open(ARCHIVO_CONFIG) as archivo_json:
            print(f"Configurando planetas desde {ARCHIVO_CONFIG} ({__name__}.py)")
            self.planetas = json.load(archivo_json)["planetas"]