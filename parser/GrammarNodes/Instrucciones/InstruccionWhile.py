from parser.Entorno.Entorno import TipoEntorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionWhile(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna = -1):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna)
    
    def execute(self, enviroment):
        #while expresion instrucciones end
        sigueCiclo = True
        tipoEntorno = enviroment.tipoEntorno
        enviroment.tipoEntorno = TipoEntorno.cicloWhile
        while(sigueCiclo):
            
            self.hijos[1].execute(enviroment)
            if(self.hijos[1].tipo == DataType.bool):
                if(self.hijos[1].valor):
                    self.hijos[2].execute(enviroment)
                    self.isReturn = self.hijos[2].isReturn
                    if(self.isReturn):
                        self.valor = self.hijos[2].valor
                        self.tipo = self.hijos[2].tipo
                        break
                    if(self.hijos[2].isBreak):
                        self.valor = self.hijos[2].valor
                        self.tipo = self.hijos[2].tipo
                        sigueCiclo=False
                        break
                else:
                    sigueCiclo=False
            else:
                sigueCiclo=False
        enviroment.tipoEntorno = tipoEntorno

        

    def getC3D(self):
        pass