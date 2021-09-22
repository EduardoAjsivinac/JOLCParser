from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionElse(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        self.hijos[1].execute(enviroment)
        self.valor = self.hijos[1].valor
        self.tipo = self.hijos[1].tipo
        self.isReturn = self.hijos[1].isReturn
        self.isContinue = self.hijos[1].isContinue
        self.isBreak = self.hijos[1].isBreak
        

    def getC3D(self):
        pass