from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class NodeMayor(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[0].execute(enviroment)
        self.hijos[2].execute(enviroment)
        type = TypeChecker('>',enviroment, self.hijos[0], self.hijos[2])
        if (type != DataType.error and type != DataType.nothing):
            self.valor = self.hijos[0].valor > self.hijos[2].valor
        self.tipo = type

    def getC3D(self):
        pass