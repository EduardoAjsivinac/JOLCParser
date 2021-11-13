from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker


class FuncionPop(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        self.hijos[2].execute(enviroment)
        self.hijos[3].execute(enviroment)
        if(self.hijos[2].tipo == DataType.array):
            if(self.hijos[3].tipo==None): #Sin dimensiones
                valorPop = self.hijos[2].valor.pop()
                self.valor = valorPop.valor
                self.tipo = valorPop.tipo
                enviroment.updateSymbol(self.hijos[2].texto, self.hijos[2].fila, self.hijos[2].columna, self.hijos[2].valor, self.hijos[2].tipo)
            elif(self.hijos[3].tipo != DataType.error):
                temp = self.hijos[2]
                for x in self.hijos[3].valor:
                    if (temp.tipo == DataType.array):
                        if((x-1)<len(temp.valor)):
                            temp = temp.valor[x-1]
                        else:
                            self.tipo = DataType.error
                            descripcion ="Fuera deñ rango"
                            enviroment.addError(descripcion,self.hijos[2].fila, self.hijos[2].columna)
                            break
                    else:
                        self.tipo = DataType.error
                        descripcion = "No es un arreglo, no se puede hacer POP"
                        enviroment.addError(descripcion,self.hijos[2].fila, self.hijos[2].columna)
                        break
                if (self.tipo != DataType.error):
                    valorPop = temp.valor.pop()
                    self.valor = valorPop.valor
                    self.tipo = valorPop.tipo
                    enviroment.updateSymbol(self.hijos[2].texto, self.hijos[2].fila, self.hijos[2].columna, self.hijos[2].valor, self.hijos[2].tipo)
    
    def createTable(self, simbolTable):
        pass
        
    def getC3D(self,symbolTable):
        pass