from parser.GrammarNodes.Expresion.Aritmeticas.NodeModulo import NodeModulo
from parser.GrammarNodes.Expresion.Logicas import *
from parser.GrammarNodes.Terminales import *
from parser.GrammarNodes.Expresion.Aritmeticas import *
from parser.GrammarNodes.Tipo.DataType import DataType
from .GrammarNodes.Expresion.GenericoExpresion import GenericoExpresion


# Define variables globales
global noNode

# -----------------------------------------------
# Analizador léxico realizado en lex.py para JOLC
# Universidad de San Carlos de Guatemala
# Organización de Lenguajes y Compiladores 2
#
# Eduardo Isaí Ajsivinac Xico
# 201503584
# -----------------------------------------------

#region Léxico

reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE'
 }

tokens  = (
    # Expresiones regulares
    'IDENTIFICADOR',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CHAR',

    # Palabras reservadas
    'TRUE',
    'FALSE',

    # Signos y símbolos
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'POTENCIA',

    'MAYOR',
    'MENOR',
    'MENORIGUAL',
    'MAYORIGUAL',
    'IGUALIGUAL',
    'DIFIGUAL',
    'DIFERENTE',
    'PARIZQ',
    'PARDER',
    'DOSPTS',
    'PTCOMA'
)

# Tokens
t_TRUE      = r'true'
t_FALSE     = r'false'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_POTENCIA  = r'\^'
t_MODULO    = r'%'
t_MENOR     = r'<'
t_MAYOR     = r'>'
t_IGUAL     = r'='
t_IGUALIGUAL= r'=='
t_MENORIGUAL= r'<='
t_MAYORIGUAL= r'>='
t_DIFIGUAL  = r'!='
t_DIFERENTE = r'!'
t_PTCOMA    = r';'
t_DOSPTS    = r':'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_CADENA(t):
    r'\".*?\"'
    #Supresion de comillas
    t.value = t.value[1:-1]
    return t

def t_IDENTIFICADOR(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'IDENTIFICADOR')# Check for reserved words
     return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()

#endregion

# -----------------------------------------------
# Analizador sintáctico realizado en yacc.py para JOLC
# Universidad de San Carlos de Guatemala
# Organización de Lenguajes y Compiladores 2
#
# Eduardo Isaí Ajsivinac Xico
# 201503584
# -----------------------------------------------

#region Sintáctico

#region Configuraciones iniciales
precedence = (
    ('left','DIFERENTE'),
    ('left','MENOR','MAYOR', 'IGUALIGUAL', 'MENORIGUAL', 'MAYORIGUAL', 'DIFIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO', 'MODULO'),
    ('left', 'POTENCIA'),
    ('right','UMENOS'),
    )
#endregion

# Definición de la gramática
def p_instrucciones_lista(t):
    '''instrucciones    : instruccion '''
    t[0]=t[1]
                        

def p_instrucciones_evaluar(t):
    'instruccion : expresion'
    t[0] = t[1]

#region Expresion
#region Logicas
def p_expresion_menor(t):
    '''expresion : expresion MENOR expresion'''
    t[0] = NodeMenor(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"<"))
    t[0].addChild(t[3])

def p_expresion_mayor(t):
    '''expresion : expresion MAYOR expresion'''
    t[0] = NodeMayor(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),">"))
    t[0].addChild(t[3])

def p_expresion_igualigual(t):
    '''expresion : expresion IGUALIGUAL expresion'''
    t[0] = NodeIgual(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"=="))
    t[0].addChild(t[3])

def p_expresion_menorigual(t):
    '''expresion : expresion MENORIGUAL expresion'''
    t[0] = NodeMenorIgual(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"<="))
    t[0].addChild(t[3])

def p_expresion_mayorigual(t):
    '''expresion : expresion MAYORIGUAL expresion'''
    t[0] = NodeMayorIgual(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),">="))
    t[0].addChild(t[3])

def p_expresion_difigual(t):
    '''expresion : expresion DIFIGUAL expresion'''
    t[0] = NodeDiferenteIgual(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"!="))
    t[0].addChild(t[3])
#endregion
#region Aritmeticas
def p_expresion_suma(t):
    '''expresion : expresion MAS expresion'''
    t[0] = NodeSuma(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"+"))
    t[0].addChild(t[3])

def p_expresion_resta(t):
    '''expresion : expresion MENOS expresion'''
    t[0] = NodeResta(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"-"))
    t[0].addChild(t[3])

def p_expresion_multiplicacion(t):
    '''expresion : expresion POR expresion'''
    t[0] = NodeMultiplicacion(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"*"))
    t[0].addChild(t[3])

def p_expresion_division(t):
    '''expresion : expresion DIVIDIDO expresion'''
    t[0] = NodeDivision(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"/"))
    t[0].addChild(t[3])

def p_expresion_modulo(t):
    '''expresion : expresion MODULO expresion'''
    t[0] = NodeModulo(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"%"))
    t[0].addChild(t[3])

def p_expresion_potencia(t):
    '''expresion : expresion POTENCIA expresion'''
    t[0] = NodePotencia(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"^"))
    t[0].addChild(t[3])

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]


def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = NodeAgrupacion(None, getNoNode(), "E")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"("))
    t[0].addChild(t[2])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")"))
#endregion
#region Terminales con Tipo de Dato
def p_expresion_entero(t):
    '''expresion    : ENTERO'''
    t[0] = TerminalEntero(t[1], str(getNoNode()),t[1], t.lineno(1), t.lexpos(1), DataType.int64)

def p_expresion_decimal(t):
    '''expresion    : DECIMAL'''
    t[0] = TerminalDecimal(t[1], str(getNoNode()),t[1], t.lineno(1), t.lexpos(1), DataType.float64)

def p_expresion_cadena(t):
    '''expresion    : CADENA'''
    t[0] = TerminalCadena(t[1], str(getNoNode()),t[1], t.lineno(1), t.lexpos(1), DataType.string)

def p_expresion_identificador(t):
    '''expresion    : IDENTIFICADOR'''
    t[0] = TerminalIdentificador(t[1], str(getNoNode()),t[1], t.lineno(1), t.lexpos(1), DataType.identificador)


#endregion
#endregion

#region Errores
def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

#endregion

#endregion

import ply.yacc as yacc
parser = yacc.yacc()

def getNoNode():
    global noNode
    noNode = noNode + 1
    return noNode


def run_method(entrada):
    global noNode
    noNode = 0;
    return parser.parse(entrada)