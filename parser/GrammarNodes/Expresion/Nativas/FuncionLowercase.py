from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class FuncionLowercase(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        if(self.hijos[2].tipo == DataType.string):
            self.valor = str(self.hijos[2].valor).lower()
            self.tipo = DataType.string
        else:
            descripcion = "La función <b>lowercase</b> requiere una cadena como parametro"
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
    
    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass