from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionPrint(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        texto = ""
        if (self.hijos[2].tipo != DataType.error):
            for x in self.hijos[2].hijos:
                if(x.valor != None):
                    texto +=str(x.valor)
                else:
                    texto +=" "
            enviroment.agregarPila(texto)

    def getC3D(self):
        pass