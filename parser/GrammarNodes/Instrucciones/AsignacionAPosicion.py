from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy

class AsignacionAPosicion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        for x in self.hijos:
            x.execute(enviroment)
        if(self.hijos[0].tipo == DataType.array):
            if(self.hijos[1].tipo != DataType.error):
                if(self.hijos[3].tipo != DataType.error):
                    temp = self.hijos[0]
                    for x in self.hijos[1].valor:
                        if temp.tipo == DataType.array:
                            if((x-1)<len(temp.valor) and (x-1)>=0):
                                temp=temp.valor[x-1]
                            else:
                                descripcion = "Posicion fuera de rango"
                                enviroment.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)
                                self.tipo = DataType.error
                        else:
                            descripcion = "Posicion fuera de rango"
                            enviroment.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)
                            self.tipo = DataType.error
                    if(self.tipo!=DataType.error):
                        temp.valor = self.hijos[3].valor
                        temp.tipo = self.hijos[3].tipo
                        self.tipo = temp.tipo
                        self.valor = self.valor
                        enviroment.updateSymbol(self.hijos[0].texto, self.fila, self.columna, self.hijos[0].valor, self.hijos[0].tipo)
                        
            else:
                descripcion = "Las posiciones tienen que ser enteros mayores a 0"
                enviroment.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)
        else:
            descripcion = "El tipo de variable no es un arreglo o la variable no está definida"
            enviroment.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)
    
    def createTable(self, simbolTable):
        pass

    def getC3D(self,symbolTable):
        pass