from copy import deepcopy
import numpy as np

from parser.GrammarNodes.Tipo.DataType import DataType

class SymbolTable():
    def __init__(self, nombreEntorno):
        self.listaSimbolos = [] # Servira Para reportes
        self.nombreEntorno = []
        self.nombreEntorno.append(nombreEntorno)
        self.posicion = 0
        self.noEntorno = 1 # El 0 es el global
        self.erroresSalida = []
    def agregarExpresionFunciones(self, texto):
        self.expresionFunciones+=texto+"\n"
    
    def getTextoFunciones(self):
        return self.expresionFunciones

    def agregarLibreria(self,nombre):
        self.librerias[nombre] = nombre

    def getNoVar(self):
        return len(self.listaSimbolos)

    def getNextPosArray(self):
        return self.posicion
    
    def setNextPosArray(self, pos):
        self.posicion = pos
    
    def compararEntornos(self,arr1,arr2): 
        if(len(arr1)==len(arr2)):
            for i in range(0,len(arr1)):
                if(arr1[i]!=arr2[i]):
                    return False
            return True
        else:
            # Va a comparar los dos entornos.
            # Arreglo 2, desde el que se está intentando acceder
            # Si el arreglo 2 es más grande que el primero, es posible que la variable esté.
            # Cuando el arreglo 1 es mas grande que el segundo, se está intentando acceder a una
            # variable de un nivel más bajo, por lo que no está
            if (len(arr2)>len(arr1)):
                # Si el arreglo 2 es mas grande que el primero, verificar cada una de las posiciones
                # Inicia a comparar cada una de las posiciones hasta llegar al límite del arreglo 2.
                # Al finalizar, se deben de comparar los siguientes entornos para verificar que sean 
                # ifs, else if, else, while y todas las condiciones que puedan acceder a variables superiores
                # por ejemplo, las globales.
                for i in range(0,len(arr1)):
                    if arr1[i]!=arr2[i]:
                        #Si por lo menos uno es diferente, NO existe.
                        return False
                    
                # Si todas las posiciones anteriores son iguales, es hora de verificar que las siguientes
                # sean instrucciones "ACCESIBLES"
                
                for i in range(len(arr1),len(arr2)):
                    if arr2[i]['nombre'] != "if" and arr2[i]['nombre'] != "while" and arr2[i]['nombre'] != "elseif" and arr2[i]['nombre'] != "if" :
                        return False
                return True
            else:
                print("Se intenta acceder desde: ", arr2, " a ",arr1)
            return False
    
    def insertSymbolEntity(self, nombre, tipo, tam, isGlobal = False):
        # Algoritmo para insertar símbolos
        # 1. Se busca el símbolo dentro de la tabla
        # 2. Si no existe, se inserta
        simbolo = self.findSymbol(nombre)
        if simbolo == None:
            self.listaSimbolos.append(SymbolEntity(nombre,tipo,tam,self.nombreEntorno,self.posicion,isGlobal))
            self.posicion +=1
        
    def insertFunctionEntity(self, nombre, tam, noParametros, listaAtributos):
        # Se inserta la función sin consultar si existe o no. 
        # En caso de que exista, se reemplaza. Cambiar esto si hay tiempo.
        # El penúltimo atributo se utilizó unicamente para la llamada a funciones, no aplica a la posición del heap sino aplica
        # a la posición que van a tener los aprametros.
        posInicia = len(self.listaSimbolos)
        self.listaSimbolos.append(SymbolEntity(nombre,DataType.nothing,tam,self.nombreEntorno,noParametros,True))
        # Se insertan todos los elementos de la lista que no estén en la lista anterior.
        # Esto se validará con la diferencia (el tamaño)
        contador = 0
        for id in listaAtributos:
            if(contador>=posInicia):
                self.listaSimbolos.append(SymbolEntity(id.nombre, id.tipo, id.tam, id.entorno, id.posicion+1, id.isGlobal))
            contador  += 1

    def agregarError(self, descripcion, linea, columna, clase):
        self.erroresSalida.append({
            'descripcion': descripcion, 
            'linea' :linea,
            'columna' : columna,
            'clase' : clase
            })
    
    def agregarEntorno(self, nombre):
        self.nombreEntorno.append({"nombre" : nombre, "numero" : self.noEntorno})
        self.noEntorno += 1
        
    def eliminarEntorno(self):
        self.nombreEntorno.pop()
    
    def imprimir(self):
        for x in self.listaSimbolos:
            print("", x.nombre,",", x.tipo.name,",", x.tam,",", x.entorno,",", x.posicion, ",", x.isGlobal)

    def findSymbol(self, nombre):
        # buscar si existe la variable.
        for x in self.listaSimbolos:
            if x.nombre == nombre and (x.tipo == DataType.nothing, self.compararEntornos(x.entorno,self.nombreEntorno)):
                return x
        return None

    def findPosArraySymbol(self, nombre):
        # buscar si existe la variable.
        cont = 0
        for x in self.listaSimbolos:
            if x.nombre == nombre:
                return cont
            cont +=1
        return -1

    def getNivelEntorno(self):
        return len(self.nombreEntorno)

    def getTipoEntorno(self):
        # Retorna global o función
        if (len(self.nombreEntorno) == 1):
            return "Global"
        else:
            for x in reversed(self.nombreEntorno):
                if (x['nombre'] != "if" and x['nombre'] != "else" and x['nombre'] != "elseif", x['nombre'] != "while"):
                    return x['nombre']
            return "Global"

    def buscarFuncion(self, nombre):
        for x in self.listaSimbolos:
            if x.tipo == DataType.nothing:
                print(x.nombre, nombre)
                if(x.nombre == nombre):
                    return x
        return None

class SymbolEntity():
    def __init__(self, nombre, tipo, tam, entorno, posicion, isGlobal):
        self.nombre = nombre
        self.tipo = tipo
        self.tam = tam
        self.entorno = deepcopy(entorno)
        self.posicion = posicion
        self.isGlobal = isGlobal