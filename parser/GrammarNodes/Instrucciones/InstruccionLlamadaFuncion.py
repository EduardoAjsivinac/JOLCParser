from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from parser.Entorno.Entorno import Entorno

class InstruccionLlamadaFuncion(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):

        # IDENTIFICADOR ( )
        id = self.hijos[0].texto
        funcion = enviroment.findSymbol(id)
        
        nuevoEntorno = Entorno(id)
        #nuevoEntorno.diccionarioSimbolos = enviroment.getDiccionarioSimbolos()
        if funcion != None:
            arregloFuncion = funcion['parametros_arr']
            if (funcion['clase']=='funcion'):
                if (len(arregloFuncion) == 0):
                    nuevoEntorno.addEnviroments(enviroment)
                    funcion['instrucciones'].execute(nuevoEntorno)
                    enviroment.concatErrors(nuevoEntorno.pilaErrores)
                    enviroment.agregarPila(nuevoEntorno.consolaSalida)
                else:
                    descripcion = "El numero de parametros enviados <b>0</b> no coincide con el numero solicitado por la funcion <b>" +str(len(funcion['parametros_arr']))+"</b>" 
                    enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
            else:
                descripcion = "<b>"+str(id)+"</b> no es una funcion"
                enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
        else:
            descripcion = "La función <b>"+str(id)+"</b> no está definida"
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)

    def getC3D(self):
        pass