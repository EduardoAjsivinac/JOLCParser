from parser.Entorno.Entorno import Entorno, TipoEntorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from ..C3D import C3DAux
from copy import deepcopy

class InstruccionCrearFuncionParametros(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        newEnviroment = Entorno("funcion", TipoEntorno.funcion)
        dictParam = {}
        arrParam=[]
        hayError = False

        self.hijos[3].execute(newEnviroment) # Lista Parametros

        idFuncion = self.hijos[1].valor
        self.fila = self.hijos[1].fila
        self.columna = self.hijos[1].columna
        listaParametros = self.hijos[3].hijos
        nodoCuerpo = self.hijos[5]
        
        for x in range(0,len(listaParametros),2):

            if (dictParam.get(listaParametros[x].valor,None)==None):
                #busca que el nombre del parametro no sea agregado dos veces
                dictParam[listaParametros[x].valor] = {
                    "id" : listaParametros[x].valor,
                    "tipo" : listaParametros[x].tipo,
                    "valor" : None
                }
                arrParam.append({
                    "id" : listaParametros[x].valor,
                    "tipo" : listaParametros[x].tipo,
                    "valor" : None
                })
            else:
                hayError=True
                descripcion = "El parametro <b>" + str(listaParametros[x].valor) + "</b> en la funcion <b>"+idFuncion+"</b> ya esta declarado."
                enviroment.addError(descripcion, self.fila, self.columna)
        if(not hayError):
            enviroment.addFunction(idFuncion, nodoCuerpo, self.fila, self.columna, dictParam, arrParam)
    
    def createTable(self, simbolTable):
        nuevaTabla = deepcopy(simbolTable)
        nuevaTabla.agregarEntorno("funcion")
        nuevaTabla.setNextPosArray(0)
        params = nuevaTabla.getNoVar()
        
        self.hijos[3].createTable(nuevaTabla)
        #nuevaTabla.imprimir()
        params = nuevaTabla.getNoVar()-params
        self.hijos[5].createTable(nuevaTabla)
        simbolTable.insertFunctionEntity(self.hijos[1].texto, nuevaTabla.getNoVar() - simbolTable.getNoVar(), params + 1, nuevaTabla.listaSimbolos)

    def getC3D(self,symbolTable):
        C3DAux().changeArreglo()
        atr = symbolTable.findSymbol(self.hijos[1].texto)
        if atr != None:
            C3DAux().agregarATam(atr.tam+1)
        symbolTable.agregarEntorno("funcion")
        self.hijos[5].getC3D(symbolTable)
        symbolTable.eliminarEntorno()
        C3DAux().changeArreglo()
        txt = "func "+self.hijos[1].texto+"(){\n"
        txt += "t0 = sp;\n"
        txt += "t1 = sp;\n"
        txt += self.hijos[5].expresion
        for x in C3DAux().listaReturns:
            txt+=str(x)+":\n"
        txt += "}\n"
        C3DAux().listaReturns = []
        C3DAux().agregarExpresionFunciones(txt)
        if atr != None:
            C3DAux().eliminarTam()