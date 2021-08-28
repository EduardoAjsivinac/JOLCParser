from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class NodeAgrupacion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        # ( Expresion ) 
        self.hijos[1].execute(enviroment)
        self.valor = self.hijos[1].valor
        self.tipo = self.hijos[1].tipo

    def getC3D(self):
        pass