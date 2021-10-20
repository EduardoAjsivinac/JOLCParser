from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionPrintln(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        texto = ""
        if (self.hijos[2].tipo != DataType.error):
            for x in self.hijos[2].hijos:
                if(x.valor != None and x.tipo != DataType.array):
                    texto +=str(x.valor)
                elif(x.tipo == DataType.array):
                    listaMatriz= self.generarTextoMatriz(x)
                    texto+=str(listaMatriz)
                else:
                    if(x.tipo == DataType.nothing and x.isIdentifier):
                        descripcion = "La variable <b>" + x.texto+"</b> no está definida"
                        enviroment.addError(descripcion, x.fila, x.columna)
                        self.tipo = DataType.error
                        break
                    else:
                        texto +=" "
            texto +="\n"
            if self.tipo != DataType.error:
                enviroment.consolaSalida += texto

    def generarTextoMatriz(self, arrayNode):
        listaMatriz = []
        for x in arrayNode.valor:
            if(x.tipo == DataType.array):
                listaMatriz.append(self.generarTextoMatriz(x))
            else:
                listaMatriz.append(x.valor)
        return listaMatriz

    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass