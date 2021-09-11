from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

class InstruccionForRango(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        nuevoEntorno = deepcopy(enviroment)
        #FOR IDENTIFICADOR IN expresion : expresion instrucciones END
        self.hijos[1].execute(nuevoEntorno)
        self.hijos[3].execute(nuevoEntorno)
        self.hijos[5].execute(nuevoEntorno)
        if (self.hijos[3].tipo == DataType.int64 and self.hijos[5].tipo == DataType.int64):
            for i in range(self.hijos[3].valor, self.hijos[5].valor+1): #Se le suma 1 porque JULIA trabaja con [inicio final] y no como python [inicio final)
                nuevoEntorno.updateSymbol(self.hijos[1].texto, self.hijos[1].fila, self.hijos[1].columna, i, DataType.int64)
                self.hijos[6].execute(nuevoEntorno)
        enviroment.concatErrors(nuevoEntorno.pilaErrores)
        enviroment.agregarPila(nuevoEntorno.consolaSalida)
        enviroment.actualizarValoresEntorno(nuevoEntorno)

        

    def getC3D(self):
        pass