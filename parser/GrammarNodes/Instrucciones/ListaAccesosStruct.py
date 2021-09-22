from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy
import json
import sys

class ListaAccesosStruct(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        #a.b.c.d.e.f
        # Se busca el simbolo
        simbolo = enviroment.findSymbol(self.hijos[0].texto)
        if self.valor == None:
            self.recorrerStruct(simbolo,2, True)
        else:
            self.recorrerStruct(simbolo,2, False)
        if self.tipo == DataType.error:
            enviroment.addError(self.valor,self.hijos[0].fila, self.hijos[0].columna)
        

    def recorrerStruct(self,dictBusqueda, indiceAtributo, isAsignacion):
        #Valida que haya llegado al fin de los atributos

        if(indiceAtributo<len(self.hijos)):
            #Valida que sea una estructura
            if dictBusqueda['tipo'] == DataType.struct or dictBusqueda['tipo'] == DataType.generic:
                atributo = dictBusqueda['valor'].listaAtributos.get(self.hijos[indiceAtributo].texto,None)
                if atributo != None:
                    self.recorrerStruct(dictBusqueda['valor'].listaAtributos[self.hijos[indiceAtributo].texto],indiceAtributo+2,isAsignacion)
                else:
                    self.tipo = DataType.error
                    self.valor = "No se encuentra el atributo <b>"+ self.hijos[indiceAtributo].texto +"</b>"
            else:
                self.tipo = DataType.error
                self.valor = "Atributo invalido"
        else:
            if isAsignacion :
                # self.valor = nodoBusqueda.valor
                self.valor = dictBusqueda['valor']
                self.tipo = dictBusqueda['tipo']
            else:
                dictBusqueda['valor'] = self.valor
                dictBusqueda['tipo'] = self.tipo




    def getC3D(self):
        pass