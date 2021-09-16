from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from parser.Entorno.Entorno import Entorno, TipoEntorno
from copy import deepcopy

class InstruccionLlamadaFuncion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        
        id = self.hijos[0].texto
        nuevoEntorno = Entorno(id, TipoEntorno.funcion)
        nuevoEntorno.copiarAFuncion(enviroment)
        funcion2 = nuevoEntorno.findSymbol(id)
        self.tipo = DataType.nothing
        self.valor = None
        if funcion2 != None:
            funcion = deepcopy(funcion2)
            arregloFuncion = funcion['parametros_arr']
            if (funcion['clase']=='funcion'):
                if (len(arregloFuncion) == 0):
                    nuevoEntorno.tipoEntorno=TipoEntorno.funcion
                    nuevoEntorno.addEnviroments(nuevoEntorno)
                    funcion['instrucciones'].execute(nuevoEntorno)
                    self.tipo = funcion['instrucciones'].tipo
                    self.valor = funcion['instrucciones'].valor
                else:
                    descripcion = "El numero de parametros enviados <b>0</b> no coincide con el numero solicitado por la funcion <b>" +str(len(funcion['parametros_arr']))+"</b>" 
                    nuevoEntorno.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
            else:
                descripcion = "<b>"+str(id)+"</b> no es una funcion"
                nuevoEntorno.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
        else:
            descripcion = "La función <b>"+str(id)+"</b> no está definida"
            nuevoEntorno.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
        enviroment.concatErrors(nuevoEntorno.pilaErrores)
        enviroment.consolaSalida +=nuevoEntorno.consolaSalida
        
        
    def getC3D(self):
        pass