from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionPrintSinParametros(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        texto = "\n"
        enviroment.consolaSalida += texto

    def getC3D(self):
        pass