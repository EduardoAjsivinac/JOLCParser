from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from ..C3D import C3DAux

class InstruccionReturnValor(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        #return expresion
        self.hijos[1].execute(enviroment)
        self.tipo = self.hijos[1].tipo
        self.valor = self.hijos[1].valor
        self.fila = self.hijos[0].fila
        self.columna = self.hijos[0].columna
        self.isReturn = True
    
    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        self.isReturn = True
        self.tipo = DataType.nothing
        self.hijos[1].getC3D(symbolTable)
        self.etReturn = C3DAux().getLabel()
        self.expresion += "stack[0] = " + str( self.hijos[1].referencia) + "\n"
        self.expresion += "goto "+str(self.etReturn) + "\n"