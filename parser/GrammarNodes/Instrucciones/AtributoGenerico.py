from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class AtributoGenerico(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        # Identificador
        self.hijos[0].execute(enviroment)
        if(self.hijos[0].tipo == DataType.nothing):
            enviroment.addAttrib(self.hijos[0].texto, self.hijos[0].fila, self.hijos[0].columna, None, DataType.generic)
        else:
            descripcion = "El atributo ya está declarado en esta estructura " + self.hijos[0].texto
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columa)
            
    def getC3D(self):
        pass