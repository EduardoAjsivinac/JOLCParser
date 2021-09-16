from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

class AccesoAArreglo(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        listaPosiciones =[]
        for x in self.hijos:
            x.execute(enviroment)
            
            if (x.tipo == DataType.error):
                self.tipo = DataType.error
                self.valor = None
                return
            else:
                listaPosiciones.append(x.valor)
                self.tipo = DataType.generic
                self.valor = listaPosiciones
            

    def getC3D(self):
        pass