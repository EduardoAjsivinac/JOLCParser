from parser.GrammarNodes.Tipo.DataType import DataType
from ..Node import Nodo

class GenericoExpresion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.tipo = DataType.nothing
        self.valor = None

    def getC3D(self):
        pass