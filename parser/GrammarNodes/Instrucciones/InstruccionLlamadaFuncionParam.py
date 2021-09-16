from parser.Entorno.Entorno import Entorno, TipoEntorno
from parser.GrammarNodes.Tipo.DataType import DataType, TypeChecker
from ..Node import Nodo
from copy import deepcopy
import sys
sys.setrecursionlimit(10000)

class InstruccionLlamadaFuncionParam(Nodo):
    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo= None):
        super().__init__(valor, id_nodo, texto, fila=fila, columna=columna, tipo=tipo)
    
    def execute(self, enviroment):
        # IDENTIFICADOR ( lista_parametros )
        self.hijos[2].execute(enviroment) # Se ejecutan los parámentro
        nombre_funcion = self.hijos[0].texto
        nuevo_entorno = Entorno(nombre_funcion,TipoEntorno.funcion)
        nuevo_entorno.copiarFunciones(enviroment)
        tmpFuncion = nuevo_entorno.findSymbol(nombre_funcion)

        if (tmpFuncion != None):
            parametros_solicitados =  tmpFuncion['parametros_arr']
            parametros_recibidos = self.hijos[2].hijos
            nodo_instrucciones = deepcopy(tmpFuncion['instrucciones'])
            if (len(parametros_solicitados)==int((len(parametros_recibidos)+1)/2)):
                # Se verificó la cantidad de parametros enviados y solicitados.
                for i in range(0,len(parametros_recibidos),2):
                    if (parametros_recibidos[i].isIdentifier and not parametros_recibidos[i].identifierDeclare):
                        print("La variable no está declarada", parametros_recibidos[i].texto)
                        return
                    else:
                        tipo_param = parametros_solicitados[int(i/2)]['tipo']
                        if((tipo_param ==DataType.generic or tipo_param == parametros_recibidos[i].tipo) and parametros_recibidos[i].tipo != DataType.error):
                            nuevo_entorno.addSymbol(parametros_solicitados[int(i/2)]['id'],-1,-1,parametros_recibidos[i].valor,parametros_recibidos[i].tipo)
                        else:
                            print("EL tipo de dato no es el solicitado")
                            return
                nodo_instrucciones.execute(nuevo_entorno)
                self.tipo = nodo_instrucciones.tipo
                self.valor = nodo_instrucciones.valor
                enviroment.concatErrors(nuevo_entorno.pilaErrores)
                enviroment.consolaSalida +=nuevo_entorno.consolaSalida
                enviroment.copiarValores(nuevo_entorno)
                for i in range(0,len(parametros_recibidos),2):
                    if(parametros_recibidos[i].tipo == DataType.array):
                        simbolo = nuevo_entorno.findSymbol(parametros_solicitados[int(i/2)]['id'])
                        enviroment.updateSymbol(parametros_recibidos[i].texto,-1,-1,simbolo['valor'],simbolo['tipo'])
            else:
                print("La cantidad de parametros enviados y solicitados no coinciden")
                return
        else:
            print("La función no existe.",nombre_funcion)
            return
        

        return
        self.hijos[2].execute(enviroment) #Se obtiene la lista de parametros
        id = self.hijos[0].texto # Nombre de la función.
        nuevoEntorno = deepcopy(enviroment)
        nuevoEntorno.copiarAFuncion(id, TipoEntorno.funcion)
        funcion = nuevoEntorno.findSymbol(id)
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
                                    print("Todo correcto")
                                    print(nuevoEntorno.diccionarioSimbolos)
                                    nuevoEntorno.addSymbol(arregloFuncion[int(x/2)]['id'],-1,-1,listaParametros[x].valor,listaParametros[x].tipo)
                                else:
                                    descripcion = "El tipo de datos solicitado <b>"+arregloFuncion[int(x/2)]['tipo'].name+"</b> no coincide con el enviado <b>" +listaParametros[x].tipo.name+"</b>"
                                    enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
                    funcion['instrucciones'].execute(nuevoEntorno)
                    self.tipo = funcion['instrucciones'].tipo
                    self.valor = funcion['instrucciones'].valor
                else:
                    descripcion = "El numero de parametros enviados <b>"+str(noHijos)+"</b> no coincide con el numero solicitado por la funcion <b>" +str(len(funcion['parametros_arr']))+"</b>" 
                    enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
            else:
                descripcion = "<b>"+str(id)+"</b> no es una funcion"
                enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
            del funcion
        else:
            descripcion = "La función <b>"+str(id)+"</b> no está definida"
            enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
        enviroment.concatErrors(nuevoEntorno.pilaErrores)
        enviroment.consolaSalida +=nuevoEntorno.consolaSalida
        del nuevoEntorno
        

    def getC3D(self):
        pass