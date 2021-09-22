from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class AtributoNoGenerico(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        # IDENTIFICADOR :: TIPO ;
        self.hijos[0].execute(enviroment)
        if(self.hijos[0].tipo == DataType.nothing):
            self.hijos[2].execute(enviroment)
            if(self.hijos[2].tipo!= DataType.error):
                enviroment.addAttrib(self.hijos[0].texto, self.hijos[0].fila, self.hijos[0].columna, self.hijos[2].valor, self.hijos[2].tipo)
            else:
                descripcion = "La estructura <b>" + self.hijos[2].texto + "</b> no está declarada"
                enviroment.addError(descripcion,self.hijos[2].fila, self.hijos[2].columna)
        else:
            descripcion = "El atributo <b>" + self.hijos[0].texto +"</b> ya está declarado en esta estructura"
            enviroment.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)

    def getC3D(self):
        pass