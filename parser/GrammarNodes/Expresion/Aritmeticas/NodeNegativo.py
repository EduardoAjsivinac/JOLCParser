from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from ...Tipo import TypeCheckerC3DTable
from ...C3D import C3DAux

class NodeNegativo(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[1].execute(enviroment)
        self.valor = self.hijos[1].valor
        self.fila = self.hijos[1].fila
        self.columna = self.hijos[1].columna
        self.tipo = self.hijos[1].tipo
        self.isIdentifier = self.hijos[1].isIdentifier
        self.identifierDeclare = self.hijos[1].identifierDeclare
        self.isContinue = self.hijos[1].isContinue
        self.isBreak = self.hijos[1].isBreak
        self.isReturn = self.hijos[1].isReturn
        self.isContinue = self.hijos[1].isContinue

        if(self.tipo == DataType.int64 or self.tipo == DataType.float64):
            self.valor=self.valor*-1
        else:
            descripcion = "La operación negativa solo se aplica a tipos de datos numericos"
            enviroment.addError(descripcion,self.fila, self.columna)
            self.tipo = DataType.error

    def createTable(self, simbolTable):
        self.tipo = self.hijos[1].tipo

    def getC3D(self,symbolTable):
        self.hijos[1].getC3D(symbolTable)

        self.expresion = self.hijos[1].expresion
        self.tipo = self.hijos[1].tipo
        if self.tipo == DataType.int64 or self.tipo == DataType.float64:
            if len(self.hijos[1].ev) >0 or len(self.hijos[1].ef) >0:
                # Valida si es una operación (como true o false)
                tmp = C3DAux().getTemp()
                etq = C3DAux().getLabel()
                self.hijos[1].referencia = tmp
                for x in self.hijos[1].ev:
                    self.hijos[1].expresion += x + ":\n"
                self.hijos[1].expresion+= str(tmp) + " = 1;\n"
                self.hijos[1].expresion += "goto " + str(etq) + "\n"
                for x in self.hijos[1].ef:
                    self.hijos[1].expresion += x + ":\n"
                self.hijos[1].expresion+= str(tmp) + " = 0;\n"
                self.hijos[1].expresion += str(etq) + ":\n"
            neg = C3DAux().getTemp()
            self.referencia = C3DAux().getTemp()
            self.expresion += str(neg)+ " = 0 - 1;\n"
            self.expresion +=str(self.referencia) + " = " + str(self.hijos[1].referencia) + " * " +str(neg) + "; \n"
        else:
            self.tipo = DataType.error

        
        self.isReturn = self.hijos[1].isReturn
        self.isContinue = self.hijos[1].isContinue
        self.isBreak = self.hijos[1].isBreak
        self.etBreak = self.hijos[1].etBreak
        self.etContinue = self.hijos[1].etContinue
        self.etReturn = self.hijos[1].etReturn