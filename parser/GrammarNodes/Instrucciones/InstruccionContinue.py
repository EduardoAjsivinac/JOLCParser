from parser.Entorno.Entorno import TipoEntorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from ..C3D import C3DAux

class InstruccionContinue(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        self.isContinue = True
        self.tipo = DataType.nothing

    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        self.isContinue = True
        self.tipo = DataType.nothing
        self.etContinue = C3DAux().getLabel()
        self.expresion += "goto "+str(self.etContinue) + "\n"