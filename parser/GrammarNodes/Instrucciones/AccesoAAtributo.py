from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

class AccesoAAtributo(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        pass

    def getC3D(self):
        pass