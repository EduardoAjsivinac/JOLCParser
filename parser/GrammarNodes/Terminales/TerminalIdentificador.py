from parser.GrammarNodes.C3D.Etiquetas import C3DAux
from ..Node import Nodo
from ..Tipo import DataType
from ..Tipo import TypeChecker

class TerminalIdentificador(Nodo):
    def __init__(self, valor, id_nodo, texto, fila, columna, tipo):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
        

    def execute(self, enviroment):
        simbolo = enviroment.findSymbol(self.texto)
        if (simbolo != None):
            self.valor = simbolo["valor"]
            self.tipo = simbolo["tipo"]
            self.identifierDeclare = True
            self.isIdentifier = True
        else:
            self.isIdentifier = True
            self.valor = None
            self.tipo = DataType.nothing

    def createTable(self, simbolTable):
        nodo = simbolTable.findSymbol(self.texto)
        if nodo != None:
            self.tipo = nodo.tipo

    def getC3D(self,symbolTable):
        atributo = symbolTable.findSymbol(self.texto)
        if atributo != None:
            #if atributo.tipo != DataType.string:
            tmp = C3DAux().getTemp()
            self.referencia = C3DAux().getTemp()
            self.expresion += str(tmp) + " = " + str(atributo.posicion) + ";\n"
            self.expresion += str(self.referencia) + " = heap[int(" + str(tmp) + ")];\n"
            self.tipo = atributo.tipo
            #else:
            #    symbolTable.imprimir()
            #    print("Cadena")
                
        else:
            descrpicion = "No existe la variable <b>"+self.texto+"</b>"
            self.tipo = DataType.error
            symbolTable.agregarError(descrpicion, self.fila, self.columna, "simbolo")