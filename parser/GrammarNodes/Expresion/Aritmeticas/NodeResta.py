from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from ...Tipo import TypeCheckerC3DTable

class NodeResta(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        # expresion - expresion
        self.hijos[0].execute(enviroment)
        self.hijos[2].execute(enviroment)
        type = TypeChecker('-', enviroment, self.hijos[0], self.hijos[2])
        if (type != DataType.error and type != DataType.nothing):
            self.valor = self.hijos[0].valor - self.hijos[2].valor                
        self.tipo = type

    def createTable(self, simbolTable):
        self.hijos[0].createTable(simbolTable)
        self.hijos[2].createTable(simbolTable)
        self.tipo = TypeCheckerC3DTable('-',simbolTable, self.hijos[0], self.hijos[2])

    def getC3D(self,symbolTable):
        pass