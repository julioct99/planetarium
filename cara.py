class TNormal:
    x = 0
    y = 0
    z = 0

class Cara:

    a = 0
    b = 0
    c = 0
    normal = TNormal.TNormal()

    # normal=None es que este parámetro es opcional
    def __init__(self, vA, vB, vC, normal=None):
        self.a = vA
        self.b = vB
        self.c = vC
        self.normal = normal
