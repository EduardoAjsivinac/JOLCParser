from parser.GrammarNodes.Tipo.DataType import DataType
from ..Node import Nodo

class NodeListaExpresiones(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        # expresion, expresion, expresion, expresion
        self.tipo = DataType.nothing
        self.valor = None
        for x in self.hijos:
            x.execute(enviroment)
            if (x.tipo == DataType.error):
                self.tipo = DataType.error
    
    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        for x in self.hijos:
            x.getC3D(symbolTable);