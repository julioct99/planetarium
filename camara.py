import json
from constantes import *


class camara:
    def __init__(self):
        self.camaras = []
        self.camara_activa = 0
        self.cargar_camaras()

    def cargar_camaras(self):
        with open(ARCHIVO_CONFIG) as archivo_json:
            print(f"Configurando camaras desde {ARCHIVO_CONFIG} ({__name__}.py)")
            self.camaras = json.load(archivo_json)["camaras"]

    def cambiar_camara_actual(self):
        self.camara_activa = (self.camara_activa + 1) % len(self.camaras)

    def camara_actual(self):
        return self.camaras[self.camara_activa].values()
