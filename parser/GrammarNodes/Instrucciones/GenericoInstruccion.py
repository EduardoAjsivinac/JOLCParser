from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class GenericoInstruccion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        for x in self.hijos:
            x.execute(enviroment)

    def getC3D(self):
        pass