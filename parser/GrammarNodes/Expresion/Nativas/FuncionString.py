from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from math import cos

class FuncionString(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        if(self.hijos[2].tipo == DataType.float64 or self.hijos[2].tipo == DataType.array or self.hijos[2].tipo == DataType.int64):
            self.valor = str(self.hijos[2].valor)
            self.tipo = DataType.string
        else:
            descripcion = "La función <b>float</b> requiere una numero o un arreglo"
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)

    def getC3D(self):
        pass