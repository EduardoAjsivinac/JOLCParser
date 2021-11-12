from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class ListaParametros(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        for x in self.hijos:
            x.execute(enviroment)

    def createTable(self, simbolTable):
        for x in self.hijos:
            x.createTable(simbolTable)

    def getC3D(self,symbolTable):
        print("Lista Parametros")
        self.expresion += ""
        for x in self.hijos[0]:
            x.getC3D(symbolTable)
            self.expresion += x.expresion
        
