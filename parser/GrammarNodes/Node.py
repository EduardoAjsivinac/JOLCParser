from abc import ABCMeta, abstractmethod
from parser.Entorno.SymbolTable import SymbolTable
from parser.GrammarNodes.Tipo.DataType import DataType
from parser.Entorno.Entorno import Entorno
import sys
sys.setrecursionlimit(5000)
class Nodo(metaclass=ABCMeta):

    def __init__(self, valor, id_nodo, texto, fila = -1, columna=-1, tipo = DataType.nothing):
        self.id_nodo = id_nodo
        self.valor = valor
        self.fila = fila
        self.columna = columna
        self.hijos = []
        self.tipo = tipo
        self.texto = texto
        self.isIdentifier = False
        self.identifierDeclare = False #Bandera para saber si está declarado el identificador antes o si es un identificador con valor Nothing
        self.isContinue = False
        self.isBreak = False
        self.isReturn = False
        self.arraySize = 0
        self.expresion = ""
        self.referencia = ""
        self.size = 1

    def getid(self):
        return str(self.id_nodo)


    def addChild(self, hijo):
        if(len(self.hijos)==0):
            self.columna = hijo.columna
            self.fila = hijo.fila
        self.hijo = hijo.columna
        self.hijos.append(hijo)
        

    def getdot(self):
        texto = "nodo" +str(self.getid())+"[label=\""+str(self.texto)+"\"];"
        if (len(self.hijos)>0):
            texto += "nodo" +str(self.getid())+"->{"
            texto2 = "" 
            for x in range(0,len(self.hijos)):
                if (x!=0):
                    texto +=","
                texto += "nodo" + self.hijos[x].getid()
                texto2 += self.hijos[x].getdot()
            texto += "};"
            texto +=texto2
        return texto

    @abstractmethod
    def execute(self, enviroment:Entorno):
        pass

    @abstractmethod
    def createTable(self, simbolTable : SymbolTable):
        pass

    @abstractmethod
    def getC3D(self, symbolTable):
        pass
