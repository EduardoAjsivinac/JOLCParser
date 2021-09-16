from parser.Entorno.Entorno import TipoEntorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class GenericoInstruccion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        for x in self.hijos:
            x.execute(enviroment)
            if(x.isReturn):
                if (enviroment.tipoEntorno != TipoEntorno.eglobal):
                    self.isReturn = True
                    self.tipo = x.tipo
                    self.valor = x.valor
                    break
                else:
                    descripcion = "La instruccion retorno se debe definir dentro de una funcion"
                    enviroment.addError(descripcion,x.hijos[0].fila,x.hijos[0].columna)

    def getC3D(self):
        pass