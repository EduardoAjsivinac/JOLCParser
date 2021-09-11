from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionDeclaracion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        #Identificador =  expresion :: tipo
        self.hijos[2].execute(enviroment)
        fila = self.hijos[4].fila
        columna = self.hijos[4].columna
        tipo1 = self.hijos[2].tipo
        tipo2 = self.hijos[4].tipo
        ident = self.hijos[0].texto
        if(tipo1 == tipo2):
            enviroment.addSymbol(ident, fila, columna, self.hijos[2].valor, tipo1) 
        else:
            if (tipo1 != DataType.error and tipo2 != DataType.error):
                descripcion = "El tipo " + str(tipo1.name) + " no coincide con " + str(tipo2.name)
                enviroment.addError(descripcion, fila, columna)

    def getC3D(self):
        pass