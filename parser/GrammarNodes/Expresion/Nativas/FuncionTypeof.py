from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from math import log

class FuncionTypeof(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        #ypeof(expresion)
        self.hijos[2].execute(enviroment)
        self.valor = self.hijos[2].tipo.name
        self.tipo = self.hijos[2].tipo

    def getC3D(self):
        pass