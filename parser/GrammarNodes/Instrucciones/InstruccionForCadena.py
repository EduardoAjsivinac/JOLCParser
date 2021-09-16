from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

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
        enviroment.actualizarValoresEntorno(nuevoEntorno)

        

    def getC3D(self):
        pass