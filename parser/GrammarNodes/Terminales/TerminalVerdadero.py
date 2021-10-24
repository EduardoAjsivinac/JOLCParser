from ..Node import Nodo
from ..Tipo import DataType
from ..Tipo import TypeChecker
from ..C3D import C3DAux

class TerminalVerdadero(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)

    def execute(self, enviroment):
        pass

    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        self.referencia = C3DAux().getTemp()
        self.expresion = str(self.referencia) + " = 1;\n"