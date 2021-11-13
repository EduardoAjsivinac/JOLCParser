from parser.GrammarNodes.C3D.Etiquetas import C3DAux
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy



class InstruccionCrearFuncion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        # function ID ( ) instrucciones end

        idFuncion = self.hijos[1].valor
        self.fila = self.hijos[1].fila
        self.columna = self.hijos[1].columna
        nodoCuerpo = self.hijos[4]
        
        enviroment.addFunction(idFuncion, nodoCuerpo, self.fila, self.columna)

    def createTable(self, simbolTable):
        nuevaTabla = deepcopy(simbolTable)
        nuevaTabla.agregarEntorno("funcion")
        nuevaTabla.setNextPosArray(0)
        self.hijos[4].createTable(nuevaTabla)
        # El return se toma como parametro
        simbolTable.insertFunctionEntity(self.hijos[1].texto, nuevaTabla.getNoVar() - simbolTable.getNoVar(), 1, nuevaTabla.listaSimbolos)

    def getC3D(self,symbolTable):
        C3DAux().changeArreglo()
        symbolTable.agregarEntorno("funcion")
        self.hijos[4].getC3D(symbolTable)
        symbolTable.eliminarEntorno()
        C3DAux().changeArreglo()
        txt = "func "+self.hijos[1].texto+"(){\n"
        txt += "t0 = sp;\n"
        txt += self.hijos[4].expresion
        if (self.hijos[4].isReturn):
            for x in C3DAux().listaReturns:
                txt+=str(x)+":\n"
        C3DAux().listaReturns = []
        txt += "}\n"
        C3DAux().agregarExpresionFunciones(txt)