from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionWhile(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        #while expresion instrucciones end
        sigueCiclo = True
        while(sigueCiclo):
            self.hijos[1].execute(enviroment)
            if(self.hijos[1].tipo == DataType.bool):
                if(self.hijos[1].valor):
                    self.hijos[2].execute(enviroment)
                else:
                    sigueCiclo=False
            else:
                sigueCiclo=False

        

    def getC3D(self):
        pass