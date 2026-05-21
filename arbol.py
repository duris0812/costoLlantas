class Nodo:
    def __init__(self, datos, hijos=None):
        self.datos = datos
        self.hijos = []
        self.padre = None
        self.costo = 0
        self.heuristica = 0
        self.f = 0

        if hijos is not None:
            self.set_hijos(hijos)

    def set_hijos(self, hijos):
        self.hijos = hijos

        for h in self.hijos:
            h.padre = self

    def get_hijos(self):
        return self.hijos

    def get_padre(self):
        return self.padre

    def set_padre(self, padre):
        self.padre = padre

    def get_datos(self):
        return self.datos

    def set_datos(self, datos):
        self.datos = datos

    def set_costo(self, costo):
        self.costo = costo

    def get_costo(self):
        return self.costo

    def set_heuristica(self, h):
        self.heuristica = h

    def get_heuristica(self):
        return self.heuristica

    def set_f(self, f):
        self.f = f

    def get_f(self):
        return self.f

    def igual(self, nodo):
        return self.datos == nodo.datos

    def en_lista(self, lista_nodos):
        for n in lista_nodos:
            if self.igual(n):
                return True
        return False

    def __str__(self):
        return str(self.datos)