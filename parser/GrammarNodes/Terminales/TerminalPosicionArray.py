from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

class TerminalPosicionArray(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        self.hijos[1].execute(enviroment)
        self.valor = self.hijos[1].valor
        self.fila = self.hijos[1].fila
        self.columna = self.hijos[1].columna
        self.tipo = self.hijos[1].tipo

    def getC3D(self):
        pass