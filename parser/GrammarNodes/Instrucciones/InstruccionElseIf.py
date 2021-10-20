from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionElseIf(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        self.hijos[1].execute(enviroment)
        if(self.hijos[1].tipo==DataType.bool):
            if(self.hijos[1].valor): #Elseif se cumple
                self.hijos[2].execute(enviroment)
                self.valor = self.hijos[2].valor
                self.tipo = self.hijos[2].tipo
                self.isReturn = self.hijos[2].isReturn
                self.isContinue = self.hijos[2].isContinue
                self.isBreak = self.hijos[2].isBreak
            else:
                if len(self.hijos) == 4:
                    self.hijos[3].execute(enviroment)
                    self.valor = self.hijos[3].valor
                    self.tipo = self.hijos[3].tipo
                    self.isReturn = self.hijos[3].isReturn
                    self.isContinue = self.hijos[3].isContinue
                    self.isBreak = self.hijos[3].isBreak
        else:
            descripcion = "La instrucción IF requiere una expresión booleana"
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
    
    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass