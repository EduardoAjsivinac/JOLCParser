from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from parser.Entorno.Entorno import Entorno, TipoEntorno
from copy import deepcopy
from ..C3D import C3DAux

class InstruccionLlamadaFuncion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        nombre_funcion = self.hijos[0].texto
        dato = enviroment.findSymbol(nombre_funcion)
        if dato!= None:
            if (dato['clase']=="funcion"):
                nuevo_entorno = Entorno(nombre_funcion,TipoEntorno.funcion)
                nuevo_entorno.copiarFunciones(enviroment)
                tmpFuncion = nuevo_entorno.findSymbol(nombre_funcion)
                
                if (tmpFuncion != None):
                    parametros_solicitados =  tmpFuncion['parametros_arr']
                    nodo_instrucciones = deepcopy(tmpFuncion['instrucciones'])
                    if (len(parametros_solicitados)==0):
                        # Se verificó la cantidad de parametros enviados y solicitados.
                        nodo_instrucciones.execute(nuevo_entorno)
                        self.tipo = nodo_instrucciones.tipo
                        self.valor = nodo_instrucciones.valor
                        enviroment.concatErrors(nuevo_entorno.pilaErrores)
                        enviroment.consolaSalida +=nuevo_entorno.consolaSalida
                        enviroment.copiarValores(nuevo_entorno)
                    else:
                        descripcion = "La funcion <b>"+nombre_funcion+"</b> requiere parametros"
                        enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
                        return
                else:
                    descripcion = "La función <b>"+nombre_funcion+"</b> no existe."
                    enviroment.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)
        
    def createTable(self, simbolTable):
        pass
    
    def getC3D(self,symbolTable):


        self.tipo = DataType.generic
        self.hijos[0].getC3D(symbolTable)
        func = symbolTable.findSymbol(self.hijos[0].texto)
        if func != None:
            if(self.hijos[0].size == 1):# Posicion se utilizó como numero de parametros
                
                tmpEtq = C3DAux().getTemp()
                self.expresion += "sp = sp + "+str(C3DAux().obtenerUltima())+"\n"
                self.expresion += str(tmpEtq)+" = sp;\n"
                
                self.expresion += str(self.hijos[0].texto) + "();\n"
                self.referencia = C3DAux().getTemp()
                self.expresion += str(self.referencia) + " = stack[int(sp)];\n"
                self.expresion += "sp = sp - "+str(C3DAux().obtenerUltima())+"\n"
