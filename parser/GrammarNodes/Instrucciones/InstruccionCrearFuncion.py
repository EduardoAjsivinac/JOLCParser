from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo



class InstruccionCrearFuncion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        # function ID ( ) instrucciones end

        idFuncion = self.hijos[1].valor
        self.fila = self.hijos[1].fila
        self.columna = self.hijos[1].columna
        nodoCuerpo = self.hijos[4]
        
        enviroment.addFunction(idFuncion, nodoCuerpo, self.fila, self.columna)

    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass