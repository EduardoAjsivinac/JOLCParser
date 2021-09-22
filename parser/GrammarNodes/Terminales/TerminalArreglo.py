from ..Node import Nodo
from ..Tipo import DataType
from ..Tipo import TypeChecker

class TerminalArreglo(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)

    def execute(self, enviroment):
        self.hijos[1].execute(enviroment)
        self.valor = []
        for x in range(0,len(self.hijos[1].hijos),2):
            self.valor.append(self.hijos[1].hijos[x])
        self.arraySize = len(self.valor)

    def getC3D(self):
        pass