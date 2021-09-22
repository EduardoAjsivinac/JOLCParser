from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class FuncionTrunc(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        #trunc(tipo de dato, cadena)
        if len(self.hijos) == 6:
            self.hijos[2].execute(enviroment)
            self.hijos[4].execute(enviroment)
            if(self.hijos[2].tipo==DataType.int64):
                if (self.hijos[4].tipo==DataType.float64):
                    self.valor = int(float(self.hijos[4].valor))
                    self.tipo = DataType.int64
                    self.fila = self.hijos[0].fila
                    self.columna = self.hijos[0].columna
                else:
                    self.valor = None
                    self.tipo = DataType.error
                    descripcion = "El valor <b>"+self.hijos[4].valor+"</b> no se puede truncar"
                    enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
        else: #Sin tipo
            #trunc ( expresion )
            self.hijos[2].execute(enviroment)
            if (self.hijos[2].tipo==DataType.float64):
                self.valor = int(float(self.hijos[2].valor))
                self.tipo = DataType.int64
                self.fila = self.hijos[0].fila
                self.columna = self.hijos[0].columna
            else:
                self.valor = None
                self.tipo = DataType.error
                descripcion = "El valor <b>"+self.hijos[2].valor+"</b> no se puede truncar"
                enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)

    

    def getC3D(self):
        pass