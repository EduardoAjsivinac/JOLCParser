from ..Node import Nodo
from ..Tipo import DataType
from ..Tipo import TypeChecker

class TerminalDecimal(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)

    def execute(self, enviroment):
        pass
    
    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        self.expresion=""
        self.referencia = self.texto