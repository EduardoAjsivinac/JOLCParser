from parser.GrammarNodes.C3D.Etiquetas import C3DAux
from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class FuncionUppercase(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        if(self.hijos[2].tipo == DataType.string):
            self.valor = str(self.hijos[2].valor).upper()
            self.tipo = DataType.string
        else:
            descripcion = "La función <b>uppercase</b> requiere una cadena como parametro"
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)

    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        self.hijos[2].getC3D(symbolTable)
        C3DAux().traducirCase(self,self.hijos[2],symbolTable, True)
        