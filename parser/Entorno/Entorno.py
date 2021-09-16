from copy import deepcopy
import enum
from os import isatty
from parser.GrammarNodes.Tipo.DataType import DataType

class TipoEntorno(enum.Enum):
    eglobal = 0
    funcion = 1
    cicloFor = 2
    cicloWhile = 3

class Entorno():
    def __init__(self, nombreAmbito, tipoEntorno):
        self.consolaSalida = ""
        self.nombreAmbito = nombreAmbito
        self.pilaErrores = []
        self.diccionarioSimbolos = {}
        self.diccionarioSimbolos[nombreAmbito]={}
        self.tipoEntorno = tipoEntorno
        self.globales = []

# Ejemplo del diccionario de símbolos:
#{
#   'nombre_entorno':
#       {
#           'id':{
#                   'clase':'', funcion, arreglo, simbolo
#                   'valor':'', Node
#                   'tipo':'', Int, float, 
#                   'accesible':'' True, False
#               }
#       }
# }


#region Simbolos
    def findSymbol(self, id):
        for nombre_entorno in self.diccionarioSimbolos: # nombre_entorno
            sim  = self.diccionarioSimbolos[nombre_entorno].get(id, None) # identificador
            if sim != None:
                # Existe
                if (sim['accesible']):
                    return sim
                else:
                    print("El simbolo ", id," existe pero no es accesible:",sim)
        return None
    
    def addSymbol(self, id, linea, columna, value = None, type = None, isAccesible = True):
        if (self.findSymbol(id)==None):
            # No se encuentra la variable, se puede agregar
            self.diccionarioSimbolos[self.nombreAmbito][id]= {
                "clase" : "simbolo",
                "valor" : value,
                "tipo" :type,
                "accesible" : isAccesible
            }
        else:
            descripcion = "La variable <b>" + str(id) + "</b> ya está declarada."
            self.addError(descripcion,linea,columna)

    def updateSymbol(self, id, linea, columna, value = None, type = None, isAccesible = True):
        self.diccionarioSimbolos[self.nombreAmbito][id]= {
                "clase" : "simbolo",
                "valor" : value,
                "tipo" :type,
                "accesible" : isAccesible
            }    
#endregion   

#region Errores
    def addError(self, descripcion, linea= None, columna= None):
        self.pilaErrores.append({
            'descripcion': descripcion, 
            'linea' :linea,
            'columna' : columna,
            'clase' : 'simbolo'
            })
#endregion

#region Funciones
    def addFunction(self, id, nodoCuerpo, linea, columna, parametros_dict = {}, parametros_arreglo=[]):
        if(self.findSymbol(id)==None):
            self.diccionarioSimbolos[self.nombreAmbito][id]= {
                "clase" : "funcion",
                "parametros_dict" : parametros_dict,
                "parametros_arr" : parametros_arreglo,
                "instrucciones" : nodoCuerpo,
                "accesible" : True
            }
        else:
            descripcion = "La variable " + str(id) + " ya está declarada en entorno."
            self.addError(descripcion,linea,columna)
#endregion

#region Subentornos
    def concatErrors(self, pilaErrores):
        self.pilaErrores = self.pilaErrores + pilaErrores
    
    def actualizarValoresEntorno(self, entornoActualizado):
        self.concatErrors(entornoActualizado.pilaErrores)
        self.consolaSalida = entornoActualizado.consolaSalida
        for x in self.diccionarioSimbolos:
            for y in self.diccionarioSimbolos[x]:
                self.diccionarioSimbolos[x][y] = entornoActualizado.diccionarioSimbolos[x][y]
    
    def actualizarValores(self,entornoActualizado):
        for x in self.diccionarioSimbolos:
                for y in self.diccionarioSimbolos[x]:
                    self.diccionarioSimbolos[x][y] = entornoActualizado.diccionarioSimbolos[x][y]
        print(entornoActualizado.diccionarioSimbolos,"\n\n")

    def addEnviroments(self, enviroment):
        for x in enviroment.diccionarioSimbolos:
            self.diccionarioSimbolos[enviroment.nombreAmbito] = enviroment.diccionarioSimbolos[x]
    
    def copiarFunciones(self, entorno):
        for nombre_entorno in entorno.diccionarioSimbolos:
            for nombre_simbolo in entorno.diccionarioSimbolos[nombre_entorno]:
                fun = entorno.diccionarioSimbolos[nombre_entorno][nombre_simbolo]
                if (fun['clase']=="funcion"):
                    self.addFunction(nombre_simbolo,fun['instrucciones'],-1,-1,fun['parametros_dict'],fun['parametros_arr'])
    
    def copiarValores(self, entorno):
        for nombre_entorno in entorno.diccionarioSimbolos:
            for nombre_simbolo in entorno.diccionarioSimbolos[nombre_entorno]:
                sim = entorno.diccionarioSimbolos[nombre_entorno][nombre_simbolo]
                if (sim['clase']=="simbolo"):
                    if(sim['tipo']==DataType.array):
                        self.updateSymbol(nombre_simbolo,-1,-1,sim['valor'],sim['tipo'])
#endregion