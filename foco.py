import os
import json
from constantes import *
from OpenGL.GL import *


class foco:
    def __init__(self):
        self.config_focos = []
        self.focos = [
            {"encendido": False, "nombre": GL_LIGHT0},
            {"encendido": False, "nombre": GL_LIGHT1},
            {"encendido": False, "nombre": GL_LIGHT2},
            {"encendido": False, "nombre": GL_LIGHT3},
            {"encendido": False, "nombre": GL_LIGHT4},
            {"encendido": False, "nombre": GL_LIGHT5},
            {"encendido": False, "nombre": GL_LIGHT6},
            {"encendido": False, "nombre": GL_LIGHT7},
        ]
        self.cargar_focos()

    def mostrar_estado_focos(self):
        os.system("clear")
        print("\n-----FOCOS-----------------------------")
        for i in range(len(self.focos)):
            print(f"{i}: {'Encendido' if self.focos[i]['encendido'] else ''}")
        print("---------------------------------------\n")
        print("  Usa el raton para girar la figura")
        print("  Usa el scroll del raton para hacer zoom")
        print("  Pulsa [X] para activar/desactivar el foco numero X ")
        print("  Pulsa [E] para activar/desactivar los ejes")
        print("  Pulsa [O] para activar/desactivar las orbitas")
        print("  Pulsa [ESPACIO] para cambiar de camara")
        print("  Pulsa [ESC] para salir\n")
        print("---------------------------------------\n")

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
        if self.focos[foco]["encendido"]:
            glDisable(self.focos[foco]["nombre"])
        else:
            glEnable(self.focos[foco]["nombre"])

        self.focos[foco]["encendido"] = not self.focos[foco]["encendido"]
        self.mostrar_estado_focos()
