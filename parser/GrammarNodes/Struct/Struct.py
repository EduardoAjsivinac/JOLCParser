class Struct():

    def __init__(self, mutable):
        self.mutable = mutable
        self.listaAtributos = {} #diccionario de nombres de atributo, key:index
    
    def agregarAtributo(self, llave, valor, tipo):
        self.listaAtributos[llave] = {"valor" : valor, "tipo" : tipo}