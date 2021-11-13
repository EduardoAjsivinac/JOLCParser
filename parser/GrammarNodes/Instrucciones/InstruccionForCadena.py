from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy
from ..C3D import C3DAux

class InstruccionForCadena(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        nuevoEntorno = deepcopy(enviroment)
        #FOR IDENTIFICADOR IN expresion instrucciones END
        self.hijos[1].execute(nuevoEntorno)
        self.hijos[3].execute(nuevoEntorno)
        if (self.hijos[3].tipo == DataType.string):
            arreglo_recorrer = list(self.hijos[3].valor)
            for x in arreglo_recorrer:
                nuevoEntorno.updateSymbol(self.hijos[1].texto, self.hijos[1].fila, self.hijos[1].columna, x, DataType.int64)
                self.hijos[4].execute(nuevoEntorno)
                self.isReturn = self.hijos[4].isReturn
                if (self.isReturn):
                    self.valor = self.hijos[4].valor
                    self.tipo = self.hijos[4].tipo
                    break
                if (self.hijos[4].isBreak):
                    self.valor = self.hijos[4].valor
                    self.tipo = self.hijos[4].tipo
                    break

        elif (self.hijos[3].tipo==DataType.array):
            arreglo_recorrer = []
            tipos = []
            for x in self.hijos[3].valor:
                arreglo_recorrer.append(x.valor)
                tipos.append(x.tipo)

            for x in range(0,len(arreglo_recorrer)):
                nuevoEntorno.updateSymbol(self.hijos[1].texto, self.hijos[1].fila, self.hijos[1].columna, arreglo_recorrer[x], tipos[x])
                self.hijos[4].execute(nuevoEntorno)
                self.isReturn = self.hijos[4].isReturn
                if (self.isReturn):
                    self.valor = self.hijos[4].valor
                    self.tipo = self.hijos[4].tipo
                    break
                if(self.hijos[4].isBreak):
                    self.valor = self.hijos[4].isBreak
                    self.tipo = self.hijos[4].isBreak
                    break
        enviroment.actualizarValoresEntorno(nuevoEntorno)

    def createTable(self, simbolTable):
        simbolTable.agregarEntorno("for")
        self.hijos[1].createTable(simbolTable)
        simbolTable.insertSymbolEntity(self.hijos[1].texto, DataType.char, 1)
        self.hijos[4].createTable(simbolTable)
        simbolTable.eliminarEntorno()

    def getC3D(self,symbolTable):
        symbolTable.agregarEntorno("for")
        self.hijos[1].getC3D(symbolTable) # expresion
        self.hijos[3].getC3D(symbolTable)
        self.hijos[4].getC3D(symbolTable)
        C3DAux().traducirFor(self.hijos[1], self.hijos[3],self.hijos[4], symbolTable, self)
        if(self.isBreak):
            for x in C3DAux().listaBreak:
                self.expresion += str(x)+":\n"
        C3DAux().listaBreak = []
        symbolTable.eliminarEntorno()