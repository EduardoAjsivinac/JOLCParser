from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from math import log

class FuncionTypeof(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        if (self.hijos[2].tipo==None):
            self.hijos[2].tipo=DataType.nothing
        self.valor = self.hijos[2].tipo.name
        self.tipo = self.hijos[2].tipo
    
    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass