from parser.GrammarNodes.Tipo.DataType import DataType
from ..Node import Nodo
from copy import deepcopy

class NodeTipo(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo = tipo)
    
    def execute(self, enviroment):
        if(self.tipo == DataType.struct):
            sim =  enviroment.findSymbol(self.texto)
            if(sim!= None):
                self.valor = sim
            else:
                self.tipo = DataType.error
                self.valor = None
    
    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass