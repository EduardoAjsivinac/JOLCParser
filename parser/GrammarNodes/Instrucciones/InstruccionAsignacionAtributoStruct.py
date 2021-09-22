from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

class InstruccionAsignacionAtributoStruct(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        
        self.hijos[0].valor = self.hijos[2].valor
        self.hijos[0].tipo = self.hijos[2].tipo
        self.hijos[0].execute(enviroment)
        self.valor = self.hijos[0].valor
        self.tipo = self.hijos[0].tipo

    def getC3D(self):
        pass
