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
                # las variables creadas acá son temporales
                self.hijos[6].execute(nuevoEntorno)
                # las variables se
                self.isReturn = self.hijos[6].isReturn
                if(self.isReturn):
                    self.valor = self.hijos[6].valor
                    self.tipo = self.hijos[6].tipo
                    break
                if(self.hijos[6].isBreak):
                    self.valor = self.hijos[6].tipo
                    self.tipo = self.hijos[6].tipo
                    break
        enviroment.actualizarValoresEntorno(nuevoEntorno)

        

    def getC3D(self):
        pass