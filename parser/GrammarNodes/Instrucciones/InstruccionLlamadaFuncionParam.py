from parser.Entorno.Entorno import Entorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo

class InstruccionLlamadaFuncionParam(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        # Ejecuta line de parámetros
        self.hijos[2].execute(enviroment)
        # IDENTIFICADOR ( lista_parametros )
        # buscar la funcion en Identificador
        id = self.hijos[0].texto
        funcion = enviroment.findSymbol(id)
        
        nuevoEntorno = Entorno(id)
        #nuevoEntorno.diccionarioSimbolos = enviroment.getDiccionarioSimbolos()
        if funcion != None:
            arregloFuncion = funcion['parametros_arr']
            if (funcion['clase']=='funcion'):
                noHijos = int((len(self.hijos[2].hijos)+1)/2)
                if (len(arregloFuncion) == noHijos):
                    listaParametros = self.hijos[2].hijos
                    for x in range(0,len(listaParametros),2):
                        if(listaParametros[x].isIdentifier and not listaParametros[x].identifierDeclare):
                            descripcion = "La variable <b>"+listaParametros[x].texto+"</b> no está declarada" 
                            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
                            return 
                        else:
                            if(listaParametros[x].tipo != DataType.error): 
                                # Si no hay error, si hay error ya está asignado anteriormente
                                if(arregloFuncion[int(x/2)]['tipo'] == DataType.generic or arregloFuncion[int(x/2)]['tipo'] == listaParametros[x].tipo):
                                    #Tipo de dato generico.
                                    nuevoEntorno.addSymbol(arregloFuncion[int(x/2)]['id'],-1,-1,listaParametros[x].valor,listaParametros[x].tipo)
                                else:
                                    descripcion = "El tipo de datos solicitado <b>"+arregloFuncion[int(x/2)]['tipo'].name+"</b> no coincide con el enviado <b>" +listaParametros[x].tipo.name+"</b>"
                                    enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
                    nuevoEntorno.addEnviroments(enviroment)
                    funcion['instrucciones'].execute(nuevoEntorno)
                    enviroment.concatErrors(nuevoEntorno.pilaErrores)
                    enviroment.agregarPila(nuevoEntorno.consolaSalida)
                else:
                    descripcion = "El numero de parametros enviados <b>"+str(noHijos)+"</b> no coincide con el numero solicitado por la funcion <b>" +str(len(funcion['parametros_arr']))+"</b>" 
                    enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
            else:
                descripcion = "<b>"+str(id)+"</b> no es una funcion"
                enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
        else:
            descripcion = "La función <b>"+str(id)+"</b> no está definida"
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
        

    def getC3D(self):
        pass