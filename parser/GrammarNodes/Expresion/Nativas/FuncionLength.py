from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from math import log

class FuncionLength(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        #length( expresion )
        self.hijos[2].execute(enviroment)
        if (self.hijos[2].tipo == DataType.array):
            self.tipo = DataType.int64
            self.valor = len(self.hijos[2].valor)
            self.fila = self.hijos[2].fila
            self.columna = self.hijos[2].columna
        else:
            self.tipo = DataType.error
            self.valor = None
            self.fila = self.hijos[2].fila
            self.columna = self.hijos[2].columna
            descripcion = "La funcion length se aplica unicamente a un arreglo"
            enviroment.addError(descripcion,self.fila,self.columna)

    def getC3D(self):
        pass