import re
import json
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL import *
import math as m

from point_face import Point3D, Face


class Modelo:
    alpha = None
    beta = None

    ListaPuntos3D = []
    ListaCaras = []

    numCaras = None
    numVertices = None

    def __init__(self, ncaras=None, nvertices=None):
        self.NumCaras = ncaras
        self.NumVertices = nvertices
        self.inicializarParametros()

    def setVector4(self, v, v0, v1, v2, v3):
        v[0] = v0
        v[1] = v1
        v[2] = v2
        v[3] = v3

    def inicializarParametros(self):
        self.alpha = 0
        self.beta = 0

    @staticmethod
    def load(path: str):
        """Loads a asc file as a 3D model

        Args:
            path (str): The path where the asc file can be found

        Returns:
            str: Name of the imported model
            list: List of vertices (Point3D)
            list: List of faces (Face)
        """

        num_vertices, num_faces = 0, 0
        vertices, faces = list(), list()
        name = ""

        def regex(types, regex, string):
            return [t(s) for t, s in zip(types, re.search(regex, string).groups())]

        with open(path) as file:
            for line in file:
                line = line.strip()
                if line[:5] == "Named":
                    name = re.search('"(.*)"', line).groups()[0]
                    line = next(file)
                    _, num_vertices, _, _, num_faces = regex(
                        (str, int, str, str, int),
                        "Tri-mesh, Vertices:(\s+)(\d+)(\s+)Faces:(\s+)(\d+)",
                        line,
                    )

                if line == "Vertex list:":
                    for n in range(0, num_vertices):
                        line = next(file)

                        _, x = regex((str, float), "X:(\s*)(-?\d*\.?\d*)", line)
                        _, y = regex((str, float), "Y:(\s*)(-?\d*\.?\d*)", line)
                        _, z = regex((str, float), "Z:(\s*)(-?\d*\.?\d*)", line)

                        vertices.append(Point3D(x, y, z))

                if line == "Face list:":
                    for n in range(0, num_faces):
                        line = next(file)
                        if line.strip() == "" or "Page" in line or "Smoothing:" in line:
                            continue

                        _, a = regex((str, int), "A:(\s*)(\d+)", line)
                        _, b = regex((str, int), "B:(\s*)(\d+)", line)
                        _, c = regex((str, int), "C:(\s*)(\d+)", line)

                        ax = vertices[a].x - vertices[b].x  # X[A] - X[B]
                        ay = vertices[a].y - vertices[b].y  # Y[A] - Y[B]
                        az = vertices[a].z - vertices[b].z  # Z[A] - Z[B]
                        bx = vertices[b].x - vertices[c].x  # X[B] - X[C]
                        by = vertices[b].y - vertices[c].y  # Y[B] - Y[C]
                        bz = vertices[b].z - vertices[c].z  # Z[B] - Z[C]

                        normal = Point3D(
                            (ay * bz) - (az * by),
                            (az * bx) - (ax * bz),
                            (ax * by) - (ay * bx),
                        )

                        l = ((normal.x ** 2) + (normal.y ** 2) + (normal.z ** 2)) ** (1 / 2)

                        normal.x /= l
                        normal.y /= l
                        normal.z /= l

                        faces.append(Face(a, b, c, normal))

        return name, vertices, faces

    def Draw_Model(self, iForma, scale_from_editor, zoom, material, planeta):

        # zoom *= planeta["tamanio"]
        # r = planeta["radio"]
        # # posicion = (m.cos(r), 0, m.sin(r))

        # # Pintar la órbita
        # # ----------------------------------------------------------------------------------------
        # glPushMatrix()
        # glBegin(GL_LINES)
        # radio = r * 1000 * scale_from_editor * zoom

        # # glVertex3d ((p.radio/100.0)*cos(2*i*3.14/360), 0 , (p.radio/180)*sen(2*i*3.14/360))
        # for i in range(360):
        #     glVertex3d(
        #         ((radio / 180) * m.cos(2 * i * 3.14 / 360)),
        #         0,
        #         ((radio / 180) * m.sin(2 * i * 3.14 / 360)),
        #     )

        # glEnd()
        # # ----------------------------------------------------------------------------------------

        # glTranslate(m.cos(r), 0, m.sin(r))
        # glPopMatrix()

        if iForma == 6:  # Wired
            glDisable(GL_LIGHTING)
            for face in self.ListaCaras:
                glBegin(GL_LINES)
                glVertex3f(
                    self.ListaPuntos3D[face.a].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].z * scale_from_editor * zoom,
                )
                glVertex3f(
                    self.ListaPuntos3D[face.b].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].z * scale_from_editor * zoom,
                )
                glVertex3f(
                    self.ListaPuntos3D[face.c].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].z * scale_from_editor * zoom,
                )
                glEnd()
            glEnable(GL_LIGHTING)

        elif iForma == 7:  # Solid
            for face in self.ListaCaras:
                glBegin(GL_POLYGON)
                glVertex3f(
                    self.ListaPuntos3D[face.a].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].z * scale_from_editor * zoom,
                )
                glVertex3f(
                    self.ListaPuntos3D[face.b].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].z * scale_from_editor * zoom,
                )
                glVertex3f(
                    self.ListaPuntos3D[face.c].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].z * scale_from_editor * zoom,
                )
                glEnd()

        elif iForma == 8:  # Flat
            glShadeModel(GL_FLAT)
            glMaterialfv(GL_FRONT, GL_DIFFUSE, material["luzdifusa"])
            glMaterialfv(GL_FRONT, GL_SPECULAR, material["luzspecular"])
            glMaterialfv(GL_FRONT, GL_AMBIENT, material["luzambiente"])
            glMaterialf(GL_FRONT, GL_SHININESS, material["brillo"])
            for face in self.ListaCaras:
                glBegin(GL_POLYGON)
                glNormal3f(
                    face.normal.x * scale_from_editor * zoom,
                    face.normal.y * scale_from_editor * zoom,
                    face.normal.z * scale_from_editor * zoom,
                )

                glVertex3f(
                    self.ListaPuntos3D[face.a].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].z * scale_from_editor * zoom,
                )
                glVertex3f(
                    self.ListaPuntos3D[face.b].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].z * scale_from_editor * zoom,
                )
                glVertex3f(
                    self.ListaPuntos3D[face.c].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].z * scale_from_editor * zoom,
                )
                glEnd()

        elif iForma == 9:  # Smooth
            glShadeModel(GL_SMOOTH)
            glMaterialfv(GL_FRONT, GL_DIFFUSE, material["luzdifusa"])
            glMaterialfv(GL_FRONT, GL_SPECULAR, material["luzspecular"])
            glMaterialfv(GL_FRONT, GL_AMBIENT, material["luzambiente"])
            glMaterialf(GL_FRONT, GL_SHININESS, material["brillo"])
            for face in self.ListaCaras:
                glBegin(GL_POLYGON)

                glNormal3f(
                    self.ListaPuntos3D[face.a].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].z * scale_from_editor * zoom,
                )
                glVertex3f(
                    self.ListaPuntos3D[face.a].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.a].z * scale_from_editor * zoom,
                )

                glNormal3f(
                    self.ListaPuntos3D[face.b].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].z * scale_from_editor * zoom,
                )
                glVertex3f(
                    self.ListaPuntos3D[face.b].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.b].z * scale_from_editor * zoom,
                )

                glNormal3f(
                    self.ListaPuntos3D[face.c].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].z * scale_from_editor * zoom,
                )
                glVertex3f(
                    self.ListaPuntos3D[face.c].x * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].y * scale_from_editor * zoom,
                    self.ListaPuntos3D[face.c].z * scale_from_editor * zoom,
                )

                glEnd()

        glVertex3f(
            self.ListaPuntos3D[face.a].x * scale_from_editor * zoom,
            self.ListaPuntos3D[face.a].y * scale_from_editor * zoom,
            self.ListaPuntos3D[face.a].z * scale_from_editor * zoom,
        )

        # glEnd()
