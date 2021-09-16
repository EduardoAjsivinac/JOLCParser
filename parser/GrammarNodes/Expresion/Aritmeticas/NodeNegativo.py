from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class NodeNegativo(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[1].execute(enviroment)
        self.valor = self.hijos[1].valor
        self.fila = self.hijos[1].fila
        self.columna = self.hijos[1].columna
        self.tipo = self.hijos[1].tipo
        self.isIdentifier = self.hijos[1].isIdentifier
        self.identifierDeclare = self.hijos[1].identifierDeclare
        self.isContinue = self.hijos[1].isContinue
        self.isBreak = self.hijos[1].isBreak
        self.isReturn = self.hijos[1].isReturn
        if(self.tipo == DataType.int64 or self.tipo == DataType.float64):
            self.valor=self.valor*-1
        else:
            descripcion = "La operación negativa solo se aplica a tipos de datos numericos"
            enviroment.addError(descripcion,self.fila, self.columna)
            self.tipo = DataType.error

    def getC3D(self):
        pass