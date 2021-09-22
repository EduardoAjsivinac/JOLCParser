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
        dato = enviroment.findSymbol(nombre_funcion)
        if dato!= None:
            if (dato['clase']=="funcion"):
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
                                return
                            else:
                                tipo_param = parametros_solicitados[int(i/2)]['tipo']
                                if((tipo_param ==DataType.generic or tipo_param == parametros_recibidos[i].tipo) and parametros_recibidos[i].tipo != DataType.error):
                                    nuevo_entorno.addSymbol(parametros_solicitados[int(i/2)]['id'],-1,-1,parametros_recibidos[i].valor,parametros_recibidos[i].tipo)
                                else:
                                    descripcion = "El tipo de dato <b>" + parametros_recibidos[i].tipo.name + "</b> no coincide con el solicitado <b>"+tipo_param.name+"</b>"
                                    nuevo_entorno.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)
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
                        descripcion = "La cantidad de parametros enviados <b>"+str(int((len(parametros_recibidos)+1))/2)+"</b> no coincide con el solicitado <b>"+len(parametros_solicitados) + "</b>"
                        enviroment.addError(descripcion, self.hijos[0].fila, self.hijos[0].columna)
                        return
                else:
                    descripcion = "La función <b>"+nombre_funcion+"</b> no existe."
                    enviroment.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)
            elif(dato['clase']=="struct"):
                parametros_recibidos = self.hijos[2].hijos
                # Compara el numero de datos recibidos con la solicitada
                if (int((len(parametros_recibidos)+1)/2)==len(dato['valor'].listaAtributos)):
                    indice = 0 # indice para acceso a las posiciones de self.hijos
                    self.valor = deepcopy(dato['valor']) # clase Struct
                    isError = False
                    for param in self.valor.listaAtributos:
                        tipo_dato = self.valor.listaAtributos[param]['tipo']
                        # valida que el tipo de dato sea generico o sea igual al que se recibe
                        if (tipo_dato == DataType.generic or parametros_recibidos[indice].tipo == tipo_dato ):
                            self.valor.listaAtributos[param]['tipo'] = parametros_recibidos[indice].tipo
                            self.valor.listaAtributos[param]['valor'] = parametros_recibidos[indice].valor
                        else:
                            isError = True
                            descripcion= "El tipo de dato "+parametros_recibidos[indice].tipo.name +" no coincide con el dato solicitado <b>"+tipo_dato.name+"</b>"
                            enviroment.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)
                        if isError:
                            self.tipo = DataType.error
                        else:
                            self.tipo = DataType.struct
                        indice += 2
                else:
                    
                    descripcion = "La cantidad de parametros enviada"+str(int((len(parametros_recibidos)+1)/2))+" no coincide con la solicitada"+str(len(dato['valor'].listaAtributos))
                    enviroment.addError(descripcion,self.hijos[0].fila, self.hijos[0].columna)

    def getC3D(self):
        pass