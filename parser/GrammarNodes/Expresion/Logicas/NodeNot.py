from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class NodeNot(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        # ! expresion
        self.hijos[1].execute(enviroment)
        if (self.hijos[1].tipo == DataType.bool):
            self.valor = not self.hijos[1].valor
        else:
            descripcion =""
            if(self.hijos[1].isIdentifier and not self.hijos[1].identifierDeclare):
                descripcion = "La variable <b>" + self.hijos[1].texto + "</b> no está declarada"
            else:
                descripcion = "El tipo de dato debe ser booleano"
            enviroment.addError(descripcion, self.hijos[1].fila, self.hijos[1].columna)
    
    def createTable(self, simbolTable):
        pass


    def getC3D(self,symbolTable):
        pass