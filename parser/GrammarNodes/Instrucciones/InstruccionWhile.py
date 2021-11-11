from parser.Entorno.Entorno import TipoEntorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from ..C3D import C3DAux

class InstruccionWhile(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        #while expresion instrucciones end
        sigueCiclo = True
        tipoEntorno = enviroment.tipoEntorno
        enviroment.tipoEntorno = TipoEntorno.cicloWhile
        while(sigueCiclo):
            
            self.hijos[1].execute(enviroment)
            if(self.hijos[1].tipo == DataType.bool):
                if(self.hijos[1].valor):
                    self.hijos[2].execute(enviroment)
                    self.isReturn = self.hijos[2].isReturn
                    if(self.isReturn):
                        self.valor = self.hijos[2].valor
                        self.tipo = self.hijos[2].tipo
                        break
                    if(self.hijos[2].isBreak):
                        self.valor = self.hijos[2].valor
                        self.tipo = self.hijos[2].tipo
                        sigueCiclo=False
                        break
                else:
                    sigueCiclo=False
            else:
                sigueCiclo=False
        enviroment.tipoEntorno = tipoEntorno

    def createTable(self, simbolTable):
        simbolTable.agregarEntorno("while")
        self.hijos[2].createTable(simbolTable)
        simbolTable.eliminarEntorno()

    def getC3D(self,symbolTable):
        self.hijos[1].getC3D(symbolTable) # expresion
        symbolTable.agregarEntorno("while")
        self.hijos[2].getC3D(symbolTable)
        self.isReturn = self.hijos[2].isReturn
        self.isContinue = self.hijos[2].isContinue
        self.isBreak = self.hijos[2].isBreak
        self.etBreak = self.hijos[2].etBreak
        self.etReturn = self.hijos[2].etReturn
        self.etContinue = self.hijos[2].etContinue
        C3DAux().traducirWhile(self.hijos[1], self.hijos[2], self)
        if(self.isBreak):
            self.expresion += str(self.etBreak)+":\n"
        symbolTable.eliminarEntorno()
        