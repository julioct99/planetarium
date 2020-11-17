import os
import json
import utils
from constantes import *
from OpenGL.GL import *


class foco:
    def __init__(self):
        self.config_focos = []
        self.focos = [False] * 8
        self.cargar_focos()

    def mostrar_estado_focos(self):
        os.system("clear")
        print("\n-----FOCOS-----------------------------")
        for i, foco in enumerate(self.focos):
            print(f"  {i}: {'Encendido' if foco else ''}")
        print("---------------------------------------")

    def configurar_focos(self):
        print(f"Configurando focos desde {ARCHIVO_CONFIG} ({__name__}.py)")
        for i, foco in enumerate(self.config_focos):
            glLight(GL_LIGHT1 + i, GL_DIFFUSE, foco["luzdifusa"])
            glLight(GL_LIGHT1 + i, GL_AMBIENT, foco["luzambiente"])
            glLight(GL_LIGHT1 + i, GL_SPECULAR, foco["luzspecular"])
            glLight(GL_LIGHT1 + i, GL_POSITION, foco["posicion"])
        print("Pulsa [0] para empezar")

    def cargar_focos(self):
        with open(ARCHIVO_CONFIG) as archivo_json:
            self.config_focos = json.load(archivo_json)["focos"]

    def encender(self, foco):
        # Si está apagado, se enciende. Si no, se apaga
        glDisable(GL_LIGHT0 + foco) if self.focos[foco] else glEnable(GL_LIGHT0 + foco)
        self.focos[foco] = not self.focos[foco]
        self.mostrar_estado_focos()
        utils.mostrar_instrucciones()
