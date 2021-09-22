from parser.Entorno.Entorno import Entorno
from parser.Entorno.Entorno import TipoEntorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from ..Struct import *

class InstruccionDeclaracionInmutable(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        # STRUCT IDENTIFICADOR instrucciones END
        self.hijos[1].execute(enviroment)
        if (self.hijos[1].tipo == DataType.nothing):
            nuevo_entorno = Entorno(self.hijos[1].texto,TipoEntorno.struct)
            nuevo_entorno.copiarStructs(enviroment)
            self.hijos[2].execute(nuevo_entorno)
            if(self.hijos[2].tipo == DataType.error):
                enviroment.delStruct(enviroment.nombreAmbito)
            else:                
                nuevo_entorno.limpiarAtributosStruct()
                nuevaStruct = Struct(False)
                for x in nuevo_entorno.diccionarioSimbolos[nuevo_entorno.nombreAmbito]:
                    nuevaStruct.agregarAtributo(x,nuevo_entorno.diccionarioSimbolos[nuevo_entorno.nombreAmbito][x],nuevo_entorno.diccionarioSimbolos[nuevo_entorno.nombreAmbito][x]['tipo'])
                enviroment.addStruct(nuevo_entorno.nombreAmbito, self.hijos[1].fila, self.hijos[1].columna, nuevaStruct, DataType.struct)
        else:
            descripcion = "El struct " + self.hijos[1].texto +" ya está declarado."
            enviroment.addError(descripcion, self.hijos[1].fila, self.hijos[1].columna)

    def getC3D(self):
        pass