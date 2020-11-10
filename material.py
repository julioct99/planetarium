import json
from constantes import *


class material:
    def __init__(self):
        self.materiales = []
        self.cargar_materiales()

    def cargar_materiales(self):
        with open(ARCHIVO_CONFIG) as archivo_json:
            print(f"Configurando materiales desde {ARCHIVO_CONFIG} ({__name__}.py)")
            self.materiales = json.load(archivo_json)["materiales"]
