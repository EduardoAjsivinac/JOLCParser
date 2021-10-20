from ..Node import Nodo
from ..Tipo import DataType
from ..Tipo import TypeChecker

class TerminalIdentificador(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
        

    def execute(self, enviroment):
        simbolo = enviroment.findSymbol(self.texto)
        if (simbolo != None):
            self.valor = simbolo["valor"]
            self.tipo = simbolo["tipo"]
            self.identifierDeclare = True
            self.isIdentifier = True
        else:
            self.isIdentifier = True
            self.valor = None
            self.tipo = DataType.nothing

    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass