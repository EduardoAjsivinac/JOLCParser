from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionAsignacion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        #Identificador =  expresion
        self.hijos[2].execute(enviroment)
        self.hijos[0].execute(enviroment)
        self.fila = self.hijos[0].fila
        self.columna = self.hijos[0].columna
        self.tipo = self.hijos[2].tipo
        ident = self.hijos[0].texto
        if(self.tipo != DataType.error):
            if self.tipo == DataType.struct:
                enviroment.updateSymbol(ident, self.fila, self.columna, self.hijos[2].valor, self.tipo)
            else:
                enviroment.updateSymbol(ident, self.fila, self.columna, self.hijos[2].valor, self.tipo)


    def getC3D(self):
        pass