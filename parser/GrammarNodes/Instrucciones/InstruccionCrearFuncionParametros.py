from parser.Entorno.Entorno import Entorno, TipoEntorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

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
        pass

    def getC3D(self,symbolTable):
        pass