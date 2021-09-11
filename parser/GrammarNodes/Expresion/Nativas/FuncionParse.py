from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker

class FuncionParse(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        #oarse(tipo de dato, cadena)
        self.hijos[2].execute(enviroment)
        self.hijos[4].execute(enviroment)
        if(self.hijos[2].tipo==DataType.int64):
            try:
                self.valor = int(self.hijos[4].valor)
                self.tipo = DataType.int64
                self.fila = self.hijos[0].fila
                self.columna = self.hijos[0].columna
            except ValueError:
                self.valor = None
                self.tipo = DataType.error
                descripcion = "El valor <b>"+self.hijos[4].valor+"</b> no se puede convertir a entero"
                enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
        elif(self.hijos[2].tipo==DataType.float64):
            try:
                self.valor = float(self.hijos[4].valor)
                self.tipo = DataType.float64
                self.fila = self.hijos[0].fila
                self.columna = self.hijos[0].columna
            except ValueError:
                self.valor = None
                self.tipo = DataType.error
                descripcion = "El valor <b>"+self.hijos[4].valor+"</b> no se puede convertir a flotante"
                enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)

        
    

    def getC3D(self):
        pass