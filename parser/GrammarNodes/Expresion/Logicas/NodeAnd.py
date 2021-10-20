from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class NodeAnd(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        # expresion != expresion
        self.hijos[0].execute(enviroment)
        if(self.hijos[0].valor):
            self.hijos[2].execute(enviroment)
            if(self.hijos[2].valor):
                self.tipo = DataType.bool
                self.valor =  True
                return
            if(self.hijos[0].tipo==DataType.bool):
                self.tipo = DataType.bool
                self.valor = False
                return
        if(self.hijos[0].tipo==DataType.bool):
            self.tipo = DataType.bool
            self.valor = False
            return
        self.tipo = DataType.error
        self.valor = False

    def createTable(self, simbolTable):
        pass


    def getC3D(self,symbolTable):
        pass