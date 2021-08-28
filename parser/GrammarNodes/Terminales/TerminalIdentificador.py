from ..Node import Nodo
from ..Tipo import DataType
from ..Tipo import TypeChecker

class TerminalIdentificador(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
        

    def execute(self, enviroment):
        simbolo = enviroment.getTable().simbolos.get(self.valor)
        print(simbolo)
        if (simbolo != None):
            self.valor = simbolo.value
            self.tipo = simbolo.type
        else:
            self.valor = None
            self.tipo = DataType.nothing

    def getC3D(self):
        pass