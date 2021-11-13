from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

class AccesoAPosicion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        if(len(self.hijos)>0):
            for x in self.hijos:
                x.execute(enviroment)
            self.fila = self.hijos[0].fila
            self.columna = self.hijos[0].columna
            nodoArreglo = self.findValue(self.hijos[0],1,enviroment)
            if nodoArreglo!= None:
                self.valor = nodoArreglo.valor
                self.tipo = nodoArreglo.tipo
                self.columna = nodoArreglo.columna
                self.fila = nodoArreglo.fila
            else:
                self.tipo = DataType.error
        
    
    def findValue(self, nodeArray, ind, enviroment):
        
        if (self.hijos[ind].tipo == DataType.int64):
            indice = self.hijos[ind].valor
            #verificar que sea un arreglo
            #verificar que el indice esté entre 1 y arraySize
            if(nodeArray.tipo == DataType.array):
                if (indice > 0 and indice<=len(nodeArray.valor)):
                    # Verificar si hay mas dimensiones o no
                    if ((len(self.hijos)-1)>ind):# hijos -1 por el identificador
                        return self.findValue(nodeArray.valor[indice-1],ind+1,enviroment)
                    else:
                        return nodeArray.valor[indice-1]
                else:
                    descripcion = "Indice fuera de rango " + str(indice)+" "+str(len(nodeArray.valor))
                    enviroment.addError(descripcion,self.fila, self.columna)
            else:
                descripcion = "El valor no es un arreglo <b>" + str(nodeArray.tipo)+ "</b>"
                enviroment.addError(descripcion,self.fila, self.columna)
        else:
            descripcion = "Los indices deben ser enteros positivos mayores a 0"
            enviroment.addError(descripcion,self.fila, self.columna)
            self.tipo = DataType.error
        return None

    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass