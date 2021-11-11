from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from ..C3D import C3DAux

class InstruccionElse(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        self.hijos[1].execute(enviroment)
        self.valor = self.hijos[1].valor
        self.tipo = self.hijos[1].tipo
        self.isReturn = self.hijos[1].isReturn
        self.isContinue = self.hijos[1].isContinue
        self.isBreak = self.hijos[1].isBreak
    
    def createTable(self, simbolTable):
        simbolTable.agregarEntorno("else")
        self.hijos[1].createTable(simbolTable)
        simbolTable.eliminarEntorno()
        

    def getC3D(self,symbolTable):
        symbolTable.agregarEntorno("else")
        self.hijos[1].getC3D(symbolTable)
        C3DAux().traducirIfs(None, self.hijos[1], self)
        symbolTable.eliminarEntorno()
        self.isReturn = self.hijos[1].isReturn
        self.isContinue = self.hijos[1].isContinue
        self.isBreak = self.hijos[1].isBreak
        self.etBreak = self.hijos[1].etBreak
        self.etReturn = self.hijos[1].etReturn
        self.etContinue = self.hijos[1].etContinue