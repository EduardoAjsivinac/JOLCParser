from parser.GrammarNodes.Struct import Struct
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from parser.Entorno import *

class InstruccionDeclaracionMutable(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        # MUTABLE STRUCT IDENTIFICADOR instrucciones END
        self.hijos[2].execute(enviroment)
        if (self.hijos[2].tipo == DataType.nothing):
            nuevo_entorno = Entorno(self.hijos[2].texto,TipoEntorno.struct)
            nuevo_entorno.copiarStructs(enviroment)
            self.hijos[3].execute(nuevo_entorno)
            if(self.hijos[3].tipo == DataType.error):
                enviroment.delStruct(enviroment.nombreAmbito)
            else:                
                nuevo_entorno.limpiarAtributosStruct()
                nuevaStruct = Struct(True)
                for x in nuevo_entorno.diccionarioSimbolos[nuevo_entorno.nombreAmbito]:
                    nuevaStruct.agregarAtributo(x,nuevo_entorno.diccionarioSimbolos[nuevo_entorno.nombreAmbito][x],nuevo_entorno.diccionarioSimbolos[nuevo_entorno.nombreAmbito][x]['tipo'])
                enviroment.addStruct(nuevo_entorno.nombreAmbito, self.hijos[2].fila, self.hijos[2].columna, nuevaStruct, DataType.struct)
        else:
            descripcion = "El struct " + self.hijos[2].texto +" ya está declarado."
            enviroment.addError(descripcion, self.hijos[2].fila, self.hijos[2].columna)

    def getC3D(self):
        pass