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
        enviroment.concatErrors(nuevoEntorno.pilaErrores)
        enviroment.agregarPila(nuevoEntorno.consolaSalida)
        enviroment.actualizarValoresEntorno(nuevoEntorno)

        

    def getC3D(self):
        pass