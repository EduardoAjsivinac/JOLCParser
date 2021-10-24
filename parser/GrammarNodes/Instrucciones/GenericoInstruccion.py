from parser.Entorno.Entorno import TipoEntorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class GenericoInstruccion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        for x in self.hijos:
            x.execute(enviroment)
            if(x.isReturn):
                if (enviroment.tipoEntorno != TipoEntorno.eglobal):
                    self.isReturn = True
                    self.tipo = x.tipo
                    self.valor = x.valor
                    break
                else:
                    descripcion = "La instruccion retorno se debe definir dentro de una funcion"
                    enviroment.addError(descripcion,x.hijos[0].fila,x.hijos[0].columna)
            if(x.isBreak):
                if (enviroment.tipoEntorno != TipoEntorno.eglobal):
                    self.isBreak = True
                    self.tipo = x.tipo
                    self.valor = x.valor
                    break
                else:
                    descripcion = "La instruccion break se debe definir dentro de una funcion"
                    enviroment.addError(descripcion,x.hijos[0].fila,x.hijos[0].columna)
            if(x.isContinue):
                if (enviroment.tipoEntorno != TipoEntorno.eglobal):
                    self.isContinue = True
                    self.tipo = x.tipo
                    self.valor = x.valor
                    break
                else:
                    descripcion = "La instruccion continue se debe definir dentro de una funcion"
                    enviroment.addError(descripcion,x.hijos[0].fila,x.hijos[0].columna)
    
    def createTable(self, simbolTable):
        for x in self.hijos:
            x.createTable(simbolTable)

    def getC3D(self,symbolTable):
        for x in self.hijos:
            x.getC3D(symbolTable)
            if x.texto == "Instruccion":
                if x.texto == "Function":
                    self.expresion = x.expresion + self.expresion
                else: 
                    self.expresion += x.expresion
            else:
                self.expresion += x.expresion 