from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class Parametro(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        # ID :: Tipo //Con tipo de dato
        # ID //Tipo de dato 
        if (self.hijos[0].tipo != DataType.generic):
            self.tipo = self.hijos[2].tipo
            self.valor = self.hijos[0].texto
            self.fila = self.hijos[0].fila
            self.columna = self.hijos[0].columna
        else:
            self.tipo = DataType.generic
            self.valor = self.hijos[0].texto
            self.fila = self.hijos[0].fila
            self.columna = self.hijos[0].columna

    
    def createTable(self, simbolTable):
        pass
        
    def getC3D(self,symbolTable):
        pass