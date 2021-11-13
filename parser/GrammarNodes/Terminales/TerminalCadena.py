from parser.GrammarNodes import C3D
from ..Node import Nodo
from ..Tipo import DataType
from ..Tipo import TypeChecker
from ..C3D import C3DAux

class TerminalCadena(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)

    def execute(self, enviroment):
        pass
    
    def createTable(self, simbolTable):
        self.size = len(self.valor)

    def getC3D(self,symbolTable):
        C3DAux().traducirCadena(self,symbolTable)