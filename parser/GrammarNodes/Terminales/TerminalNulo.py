from ..Node import Nodo
from ..Tipo import DataType
from ..Tipo import TypeChecker

class TerminalNulo(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)

    def execute(self, enviroment):
        self.tipo = DataType.nothing
        self.valor = None

    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass