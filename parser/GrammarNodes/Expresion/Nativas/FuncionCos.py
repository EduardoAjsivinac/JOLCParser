from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from math import cos

class FuncionCos(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        if(self.hijos[2].tipo == DataType.int64 or self.hijos[2].tipo == DataType.float64):
            self.valor = cos(self.hijos[2].valor)
            self.tipo = DataType.float64
        else:
            descripcion = "La función <b>sin</b> requiere una numero como parametro"
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)

    def getC3D(self):
        pass