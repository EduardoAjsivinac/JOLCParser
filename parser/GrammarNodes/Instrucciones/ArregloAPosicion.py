from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

class ArregloAPosicion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        self.valor = []
        for x in self.hijos:
            x.execute(enviroment)
            if(x.tipo==DataType.int64):
                self.valor.append(x.valor)
            else:
                self.tipo = DataType.error
        

    def getC3D(self):
        pass