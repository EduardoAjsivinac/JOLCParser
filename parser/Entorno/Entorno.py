class Entorno():
    def __init__(self, nombreAmbito):
        self.consolaSalida = ""
        self.nombreAmbito = nombreAmbito
        self.pilaErrores = []
        self.diccionarioSimbolos = {}
        self.diccionarioSimbolos[nombreAmbito]={}
    
    def agregarPila(self, salida): # Consola Output
        self.consolaSalida+=str(salida)

    def agregarError(self, nerror): # Tabla de errores
        self.pilaError.append(nerror)

    def findSymbol(self, id): # Busca el simbolo que son accesibles
        for x in self.diccionarioSimbolos: # Recorre todos los entornos accesibles
            
            sim  = self.diccionarioSimbolos[x].get(id, None)
            if sim != None:
                if (self.nombreAmbito == x):
                    return sim
                else:
                    if (sim['accesible']):
                        return sim
        return None
    
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
            descripcion = "La variable " + str(id) + " ya está declarada."
            self.addError(descripcion,linea,columna)

    def addSymbol(self, id, linea, columna, value = None, type = None):
        if (self.findSymbol(id)==None):
            self.diccionarioSimbolos[self.nombreAmbito][id]= {
                "clase" : "simbolo",
                "valor" : value,
                "tipo" :type,
                "accesible" : False
            }
        else:
            descripcion = "La variable <b>" + str(id) + "</b> ya está declarada."
            self.addError(descripcion,linea,columna)
    
    def updateSymbol(self, id, linea, columna, value = None, type = None):
        self.diccionarioSimbolos[self.nombreAmbito][id]= {
                "clase" : "simbolo",
                "valor" : value,
                "tipo" :type,
                "accesible" : False
            }
    
    def addEnviroments(self, enviroment):
        for x in enviroment.diccionarioSimbolos:
            self.diccionarioSimbolos[enviroment.nombreAmbito] = enviroment.diccionarioSimbolos[x]

    def getDiccionarioSimbolos(self):
        return self.diccionarioSimbolos

    def addError(self, descripcion, linea= None, columna= None):
        self.pilaErrores.append({
            'descripcion': descripcion, 
            'linea' :linea,
            'columna' : columna
            })

    def concatErrors(self, pilaErrores):
        self.pilaErrores = self.pilaErrores + pilaErrores
    
    def actualizarValoresEntorno(self, entornoActualizado):
        for x in self.diccionarioSimbolos:
            for y in self.diccionarioSimbolos[x]:
                self.diccionarioSimbolos[x][y] = entornoActualizado.diccionarioSimbolos[x][y]
    
