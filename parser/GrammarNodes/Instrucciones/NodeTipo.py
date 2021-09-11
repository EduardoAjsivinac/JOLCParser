from ..Node import Nodo

class NodeTipo(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo = tipo)
    
    def execute(self, enviroment):
        pass

    def getC3D(self):
        pass