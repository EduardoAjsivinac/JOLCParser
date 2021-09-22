from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from math import log

class FuncionLog(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        #log(expresion,expresion)
        self.hijos[2].execute(enviroment)
        self.hijos[4].execute(enviroment)
        if((self.hijos[2].tipo == DataType.int64 or self.hijos[2].tipo == DataType.float64) and (self.hijos[4].tipo == DataType.int64 or self.hijos[4].tipo == DataType.float64)):
            self.valor = log(self.hijos[2].valor,self.hijos[4].valor)
            self.tipo = DataType.float64
        else:
            descripcion = "La función <b>log</b> requiere una numeros como parametros"
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)

    def getC3D(self):
        pass