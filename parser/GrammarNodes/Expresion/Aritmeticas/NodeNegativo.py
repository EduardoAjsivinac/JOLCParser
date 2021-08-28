from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class NodeNegativo(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        pass

    def getC3D(self):
        pass