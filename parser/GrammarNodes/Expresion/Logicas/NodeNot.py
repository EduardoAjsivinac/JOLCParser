from ...Node import Nodo
from ...Tipo import DataType
from ...Tipo import TypeChecker
from ...C3D import C3DAux

class NodeNot(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        # ! expresion
        self.hijos[1].execute(enviroment)
        if (self.hijos[1].tipo == DataType.bool):
            self.valor = not self.hijos[1].valor
        else:
            descripcion =""
            if(self.hijos[1].isIdentifier and not self.hijos[1].identifierDeclare):
                descripcion = "La variable <b>" + self.hijos[1].texto + "</b> no está declarada"
            else:
                descripcion = "El tipo de dato debe ser booleano"
            enviroment.addError(descripcion, self.hijos[1].fila, self.hijos[1].columna)
    
    def createTable(self, simbolTable):
        self.hijos[1].createTable(simbolTable)
        self.tipo = self.hijos[1].tipo


    def getC3D(self,symbolTable):
        self.hijos[1].getC3D(symbolTable)
        if self.hijos[1].tipo == DataType.bool:
            self.tipo = DataType.bool
            expresion1 = self.hijos[1].expresion
            if len(self.hijos[1].ev) == 0:
                # Primer hijo es un terminal True o False
                ev = C3DAux().getLabel()
                ef = C3DAux().getLabel()
                self.hijos[1].ev.append(ev)
                self.hijos[1].ef.append(ef)
                expresion1 += "if("+self.hijos[1].referencia+" == 1) {goto "+str(ev)+"}\n"
                expresion1 += "goto "+str(ef)+"\n"
            etv_tmp = self.hijos[1].ev
            self.ev = self.hijos[1].ef
            self.ef = etv_tmp
            self.expresion = expresion1 
        else:
            self.tipo = DataType.error
            self.fila = self.hijos[1].fila
            self.columna = self.hijos[1].columna
            symbolTable.agregarError("La operación <b>not</b> se trabaja con datos booleanos",self.fila, self.columna, "simbolo")