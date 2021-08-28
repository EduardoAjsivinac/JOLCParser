class Entorno():
    def __init__(self):
        self.pilasalida = []
        self.nombreAmbito = None
        self.tablaSimbolos = TablaSimbolos()
        self.pilaErrores = []
    
    def agregarPila(self, salida):
        self.pilasalida.append(salida)

    def agregarError(self, nerror):
        self.pilaError.append(nerror)

    def getTable(self):
        return self.tablaSimbolos

    def addSymbol(self, id, value = None, type = None):
        self.tablaSimbolos.simbolos[id] = Symbol(id, value, type)
    
    def addError(self, descripcion, linea= None, columna= None):
        self.pilaErrores.append({
            'descripcion': descripcion, 
            'linea' :linea+1,
            'columna' : columna+1
            })

class TablaSimbolos():

    def __init__(self):
        self.ambito = ""
        self.simbolos = {}


class Symbol():
    def __init__(self, id, value, type):
        self.value = value
        self.id = id
        self.type = type

    def getValue(self):
        return self.value
    
    def getType(self):
        return self.type

    def getId(self):
        return self.id