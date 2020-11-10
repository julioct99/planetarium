import json
from itertools import filterfalse, tee
from constantes import *

# Separa un iterable en dos listas dependiendo de si cumplen o no un filtro (pred)
def partition(pred, iterable):
    t1, t2 = tee(iterable)
    return list(filterfalse(pred, t1)), list(filter(pred, t2))


class planeta:
    def __init__(self):
        self.planetas = []
        self.cargar_planetas()

    # Carga las lunas dentro de sus respectivos planetas
    def cargar_lunas(self, astros):
        # Separamos los astros del json en planetas y lunas
        lunas, planetas = partition(lambda astro: astro["l"] == "n", astros)

        # Recorre los planetas y guarda dentro de ellos sus lunas correspondientes
        for planeta in planetas:
            planeta["lunas"] = []
            for luna in lunas:
                planeta_orbitado = luna["nombre"].lower().split(" ")[1]
                if planeta["nombre"].lower() == planeta_orbitado:
                    planeta["lunas"].append(luna)
                    lunas.remove(luna)

        self.planetas = planetas

    # Carga todos los astros del json
    def cargar_planetas(self):
        with open(ARCHIVO_CONFIG) as archivo_json:
            print(f"Configurando planetas desde {ARCHIVO_CONFIG} ({__name__}.py)")
            self.cargar_lunas(json.load(archivo_json)["planetas"])
            print("  Astros cargados: ")
            for planeta in self.planetas:
                l = len(planeta["lunas"])  # Numero de lunas del planeta
                print(f"    * {planeta['nombre']}: {l} {'luna' if l == 1 else 'lunas'} ")