from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.C3D.Etiquetas import C3DAux
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

class InstruccionIf(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        self.hijos[1].execute(enviroment)
        if(self.hijos[1].tipo==DataType.bool):
            if(self.hijos[1].valor):
                self.hijos[2].execute(enviroment)
                self.valor = self.hijos[2].valor
                self.tipo = self.hijos[2].tipo
                self.isReturn = self.hijos[2].isReturn
                self.isContinue = self.hijos[2].isContinue
                self.isBreak = self.hijos[2].isBreak
            else:
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
        simbolTable.agregarEntorno("if")
        self.hijos[2].createTable(simbolTable)
        simbolTable.eliminarEntorno()
        if (len(self.hijos)==5):
            self.hijos[3].createTable(simbolTable)
        


    def getC3D(self,symbolTable):
        self.hijos[1].getC3D(symbolTable) # expresion
        symbolTable.agregarEntorno("if")
        self.hijos[2].getC3D(symbolTable)
        C3DAux().traducirIfs(self.hijos[1], self.hijos[2], self)
        if len(self.hijos)==5 : #existe un else o un else if
            symbolTable.eliminarEntorno()
            self.hijos[3].getC3D(symbolTable)
            self.expresion += self.hijos[3].expresion
        for x in self.ev:
            self.expresion += str(x) + ":\n" # Si se cumple la condición del primer if

        self.isReturn = self.hijos[2].isReturn
        self.isContinue = self.hijos[2].isContinue
        self.isBreak = self.hijos[2].isBreak
        self.etBreak = self.hijos[2].etBreak
        self.etReturn = self.hijos[2].etReturn
        self.etContinue = self.hijos[2].etContinue

        