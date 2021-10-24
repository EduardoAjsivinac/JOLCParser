
class SymbolTable():
    def __init__(self, nombreEntorno):
        self.listaSimbolos = []
        self.nombreEntorno = []
        self.nombreEntorno.append(nombreEntorno)
        self.posicion = 0
        self.erroresSalida = []
    
    def insertSymbolEntity(self, nombre, tipo, tam, isGlobal = False):
        # buscar si existe la variable.
        for x in self.listaSimbolos:
            if x.nombre == nombre and x.entorno == self.nombreEntorno:
                return
        self.listaSimbolos.append(SymbolEntity(nombre,tipo,tam,self.nombreEntorno,self.posicion, isGlobal))
        # Se va sumando el tamaño a la posición
        # porque será la posición del siguiente elemento
        self.posicion +=tam

    def agregarError(self, descripcion, linea, columna, clase):
        self.erroresSalida.append({
            'descripcion': descripcion, 
            'linea' :linea,
            'columna' : columna,
            'clase' : clase
            })

    def imprimir(self):
        for x in self.listaSimbolos:
            print(x.nombre, x.tipo.name, x.tam, x.entorno, x.posicion, x.isGlobal)

    def findSymbol(self, nombre):
        # buscar si existe la variable.
        for x in self.listaSimbolos:
            if x.nombre == nombre and x.entorno == self.nombreEntorno:
                return x
        return None


class SymbolEntity():
    def __init__(self, nombre, tipo, tam, entorno, posicion, isGlobal):
        self.nombre = nombre
        self.tipo = tipo
        self.tam = tam
        self.entorno = entorno
        self.posicion = posicion
        self.isGlobal = isGlobal