from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from ...C3D import C3DAux

class NodeOr(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        # expresion != expresion
        self.hijos[0].execute(enviroment)
        if(not self.hijos[0].valor):
            self.hijos[2].execute(enviroment)
            if(not self.hijos[2].valor):
                self.tipo = DataType.bool
                self.valor =  False
                return
            if(self.hijos[0].tipo==DataType.bool):
                self.tipo = DataType.bool
                self.valor = True
                return
        if(self.hijos[0].tipo==DataType.bool):
            self.tipo = DataType.bool
            self.valor = True
            return
        self.tipo = DataType.error
        self.valor = False

    def createTable(self, simbolTable):
        pass


    def getC3D(self,symbolTable):
        self.hijos[0].getC3D(symbolTable)
        self.hijos[2].getC3D(symbolTable)
        if self.hijos[0].tipo == DataType.bool and self.hijos[2].tipo == DataType.bool:
            self.tipo = DataType.bool
            expresion1 = self.hijos[0].expresion
            expresion2 = self.hijos[2].expresion
            if len(self.hijos[0].ev) == 0:
                # Primer hijo es un terminal True o False
                ev = C3DAux().getLabel()
                ef = C3DAux().getLabel()
                self.hijos[0].ev.append(ev)
                self.hijos[0].ef.append(ef)
                expresion1 += "if("+self.hijos[0].referencia+" == 1) {goto "+ev+"}\n"
                expresion1 += "goto "+ef+"\n"
            if len(self.hijos[2].ev) == 0:
                # Segundo hijo es un terminal True o False
                ev = C3DAux().getLabel()
                ef = C3DAux().getLabel()
                self.hijos[2].ev.append(ev)
                self.hijos[2].ef.append(ef)
                expresion2 += "if("+self.hijos[2].referencia+" == 1) {goto "+ev+"}\n"
                expresion2 += "goto "+ef+"\n"
            self.ev = self.hijos[0].ev + self.hijos[2].ev
            self.ef = self.hijos[2].ef
            self.expresion = expresion1 
            for x in self.hijos[0].ef:
                self.expresion += str(x)+":\n"
            self.expresion += expresion2
        else:
            self.tipo = DataType.error
            self.fila = self.hijos[0].fila
            self.columna = self.hijos[0].columna
            symbolTable.agregarError("La operación <b>and</b> se trabaja con datos booleanos",self.fila, self.columna, "simbolo")