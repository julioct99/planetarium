import modelo as model
import foco
import camara
import material
import planeta
import time

from constantes import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import re
import json
import keyboard
import math as m


class Mundo:

    # Distintas opciones del menu.
    opcionesMenu = {
        "FONDO_1": 0,
        "FONDO_2": 1,
        "FONDO_3": 2,
        "DIBUJO_1": 3,
        "DIBUJO_2": 4,
        "DIBUJO_3": 5,
        "FORMA_1": 6,
        "FORMA_2": 7,
        "FORMA_3": 8,
        "FORMA_4": 9,
    }

    # Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
    # Negro, Verde oscuro, Azul oscuro, Blanco, Verde claro, Azul claro
    colores = [
        (0.00, 0.00, 0.00),
        (0.06, 0.25, 0.13),
        (0.10, 0.07, 0.33),
        (1.00, 1.00, 1.00),
        (0.12, 0.50, 0.26),
        (0.20, 0.14, 0.66),
    ]

    def __init__(self):
        # Inicializamos todo:

        # Variables de la clase
        self.width = 800
        self.height = 800
        self.aspect = self.width / self.height
        self.angulo = 0
        self.window = 0

        self.Sol = model.Modelo()
        self.camara = camara.camara()
        self.material = material.material()
        self.foco = foco.foco()
        self.planeta = planeta.planeta()

        self.focos_configurados = False
        self.mostrar_ejes = False
        self.mostrar_orbitas = True

        # Tamaño de los ejes y del alejamiento de Z.
        self.tamanio = 40
        self.z0 = 0

        # Factor para el tamaño del modelo.
        self.escalaGeneral = 0.001

        # Rotacion de los modelos.
        self.alpha = 0
        self.beta = 0

        # Variables para la gestion del ratón.
        self.xold = 0
        self.yold = 0
        self.zoom = 1.0

        # Vistas del Sistema Planetario.
        # modelo.tipoVista iForma
        self.iDibujo = 3
        self.iFondo = 0
        self.iForma = 6

    def configurar_focos(self):
        if not self.focos_configurados:
            self.foco.configurar_focos()
            self.focos_configurados = True

    def drawAxis(self):
        if self.mostrar_ejes:
            # Inicializamos
            glDisable(GL_LIGHTING)
            glBegin(GL_LINES)

            # Eje X Rojo
            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(self.tamanio, 0.0, 0.0)

            # Eje Y Verde
            glColor3f(0.0, 1.0, 0.0)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(0.0, self.tamanio, 0.0)

            # Eje Z Azul
            glColor3f(0.0, 0.0, 1.0)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(0.0, 0.0, self.tamanio)

            # Se vuelve a configurar el color de dibujo
            glColor3f(*self.colores[self.iDibujo])

            glEnd()
            glEnable(GL_LIGHTING)

    def drawOrbita(self, r):
        if self.mostrar_orbitas:
            glDisable(GL_LIGHTING)
            glBegin(GL_LINES)

            for i in range(360):
                glVertex3d(
                    ((r / 180) * m.cos(2 * i * 3.14 / 360)),
                    0,
                    ((r / 180) * m.sin(2 * i * 3.14 / 360)),
                )

            glEnd()
            glEnable(GL_LIGHTING)

    def drawPlaneta(self, planeta, i, t):
        glPushMatrix()

        tamanio = planeta["tamanio"] * 5
        r = planeta["radio"] * self.zoom
        omega = t * self.escalaGeneral * planeta["wRotAstro"]
        posicion = [r * m.cos(omega) / 180, 0, r * m.sin(omega) / 180]

        self.drawOrbita(r)

        glTranslate(*posicion)
        glRotatef(planeta["wRotProp"] * t, 0.0, 1.0, 0.0)
        # if i == 1:
        #     print(planeta["wRotProp"] * t)

        glScalef(tamanio, tamanio, tamanio)

        self.drawModel(self.Sol, self.escalaGeneral, self.material.materiales[i], planeta)
        glPopMatrix()

    def drawModel(self, forma, escala, material, planeta):
        forma.Draw_Model(self.iForma, escala, self.zoom, material, planeta)

    def display(self):
        glClearDepth(1.0)
        glClearColor(
            *self.colores[self.iFondo],
            1.0,
        )
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluPerspective(25.0, 1.0, 1.0, 10.0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Usamos la cámara activa
        gluLookAt(*self.camara.camara_actual())

        glRotatef(self.alpha, 1.0, 0.0, 0.0)
        glRotatef(self.beta, 0.0, 1.0, 0.0)

        # Establecemos el color del Modelo.
        glColor3f(*self.colores[self.iDibujo])

        self.configurar_focos()
        self.drawAxis()

        # Obtenemos el tiempo del sistema
        t = int(round(time.time() * 1000))

        # Pintamos los planetas.
        for i, planeta in enumerate(self.planeta.planetas):
            self.drawPlaneta(planeta, i, t)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glFlush()
        glutSwapBuffers()

    # Funcion para gestionar los movimientos del raton.
    def onMouse(self, button, state, x, y):
        if (button == 3) or (button == 4):
            if state == GLUT_UP:
                pass
            if (button == 3) and (self.zoom - 0.1 > 0.2):
                self.zoom = self.zoom - 0.1
            elif self.zoom + 0.1 <= 5:
                self.zoom = self.zoom + 0.1
        else:
            # Actualizamos los valores de x, y.
            self.xold = x
            self.yold = y

    # Funcion que actualiza la posicion de los modelos en la pantalla segun los movimientos del raton.
    def onMotion(self, x, y):
        self.alpha = self.alpha + (y - self.yold)
        self.beta = self.beta + (x - self.xold)
        self.xold = x
        self.yold = y
        glutPostRedisplay()

    # Funcion que gestiona las pulsaciones en el teclado.
    def keyPressed(self, *args):
        # Limpiamos toda la basura del input para quedarnos solo con el caracter que nos interesa
        key = str(args[0][0]).lower()
        keychar = key[-2]

        if key == "b'\\x1b'":  # ESC
            sys.exit()
        elif keychar == "e":
            self.mostrar_ejes = not self.mostrar_ejes
        elif keychar == "o":
            self.mostrar_orbitas = not self.mostrar_orbitas
        elif keychar == " ":
            self.camara_activa = self.camara.cambiar_camara_actual()
        else:
            # COMPROBAMOS SI ES UN NUMERO DEL 0 AL 7
            search = re.search("[0-7]", keychar)
            if search:
                self.foco.encender(int(search.string))

    # Funcion para activar las distintas opciones que permite el menu.
    def onMenu(self, opcion):
        if opcion == self.opcionesMenu["FONDO_1"]:
            self.iFondo = 0
        elif opcion == self.opcionesMenu["FONDO_2"]:
            self.iFondo = 1
        elif opcion == self.opcionesMenu["FONDO_3"]:
            self.iFondo = 2
        elif opcion == self.opcionesMenu["DIBUJO_1"]:
            self.iDibujo = 3
        elif opcion == self.opcionesMenu["DIBUJO_2"]:
            self.iDibujo = 4
        elif opcion == self.opcionesMenu["DIBUJO_3"]:
            self.iDibujo = 5
        elif opcion == self.opcionesMenu["FORMA_1"]:
            self.iForma = 6
        elif opcion == self.opcionesMenu["FORMA_2"]:
            self.iForma = 7
        elif opcion == self.opcionesMenu["FORMA_3"]:
            self.iForma = 8
        elif opcion == self.opcionesMenu["FORMA_4"]:
            self.iForma = 9
        glutPostRedisplay()
        return opcion

    def cargarModelo(self, nombre):
        _, vertices, caras = self.Sol.load(nombre)
        self.Sol.numVertices = len(vertices)
        self.Sol.numCaras = len(caras)
        self.Sol.ListaCaras = caras
        self.Sol.ListaPuntos3D = vertices
