import sys
sys.setrecursionlimit(10000)
from parser.GrammarNodes.Instrucciones.AccesoAPosicion import AccesoAPosicion
from parser.GrammarNodes.Expresion.Logicas.NodeOr import NodeOr
from parser.GrammarNodes.Expresion.Nativas import *
from parser.GrammarNodes.Expresion.ListaExpresion import NodeListaExpresiones
from parser.GrammarNodes.Instrucciones import *
from parser.GrammarNodes.Expresion.Aritmeticas.NodeModulo import NodeModulo
from parser.GrammarNodes.Expresion.Relacionales import *
from parser.GrammarNodes.Terminales import *
from parser.GrammarNodes.Expresion.Aritmeticas import *
from parser.GrammarNodes.Tipo.DataType import DataType
from .GrammarNodes.Expresion.GenericoExpresion import GenericoExpresion
from parser.GrammarNodes.Expresion.Logicas import *


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
    'println' : 'PRINTLN',
    'print' : 'PRINT',
    'Nothing' : 'NOTHING',
    'Int64' : 'INT64',
    'Float64' : 'FLOAT64',
    'Bool' : 'BOOL',
    'Char' : 'CHAR',
    'String' : 'STRING',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'function' : 'FUNCTION',
    'end' : 'END',
    'if' : 'IF',
    'elseif' : 'ELSEIF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'in' : 'IN',
    'uppercase' : 'UPPERCASE',
    'lowercase' : 'LOWERCASE',
    'log10' : 'LOG10',
    'log' : 'LOG',
    'sin' : 'SIN',
    'cos' : 'COS',
    'tan' : 'TAN',
    'sqrt' : 'SQRT',
    'parse' : 'PARSE',
    'trunc' : 'TRUNC',
    'float' : 'FLOAT',
    'string' : 'FSTR',
    'typeof' : 'TYPEOF',
    'return' : 'RETURN',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'length' : 'LENGTH',
    'push' : 'PUSH',
    'pop' : 'POP'

 }

tokens  = (
    'PRINTLN',
    'PRINT',
    'NOTHING',
    'INT64',
    'FLOAT64',
    'BOOL',
    'CHAR',
    'STRING',
    'FUNCTION',
    'END',
    'IF',
    'ELSEIF',
    'ELSE',
    'WHILE',
    'FOR',
    'IN',
    'UPPERCASE',
    'LOG10',
    'LOG',
    'SIN',
    'COS',
    'TAN',
    'SQRT',
    'PARSE',
    'TRUNC',
    'FLOAT',
    'FSTR',
    'TYPEOF',
    'RETURN',
    'BREAK',
    'CONTINUE',
    'LENGTH',
    'PUSH',
    'POP',
    # Expresiones regulares
    'IDENTIFICADOR',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'LOWERCASE',
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
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'DOSPTS',
    'PTCOMA',
    'COMA',
    'OR',
    'AND',
    'NOT'
)

# Tokens

t_PRINTLN   = r'println'
t_PRINT     = r'print'
t_FUNCTION  = r'function'
t_END       = r'end'
t_IF        = r'if'
t_ELSEIF    = r'elseif'
t_ELSE      = r'else'
t_WHILE     = r'while'
t_FOR       = r'for'
t_IN        = r'in'
t_UPPERCASE = r'uppercase'
t_LOWERCASE = r'lowercase'
t_LOG10     = r'log10'
t_LOG       = r'log'
t_SIN       = r'sin'
t_COS       = r'cos'
t_TAN       = r'tan'
t_SQRT      = r'sqrt'
t_PARSE     = r'parse'
t_TRUNC     = r'trunc'
t_FLOAT     = r'float'
t_FSTR      = r'string'
t_TYPEOF    = r'typeof'
t_RETURN    = r'return'
t_BREAK     = r'break'
t_CONTINUE  = r'continue'
t_LENGTH    = r'length'
t_PUSH      = r'push'
t_POP       = r'pop'

t_NOTHING   = r'Nothing'
t_INT64     = r'Int64'
t_FLOAT64   = r'Float64'
t_BOOL      = r'Bool'
t_CHAR      = r'Char'
t_STRING    = r'String'

t_TRUE      = r'true'
t_FALSE     = r'false'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
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
t_OR        = r'\|\|'
t_PTCOMA    = r';'
t_DOSPTS    = r':'
t_COMA    = r','
t_AND       = r'&&'
t_NOT       = r'!'

def t_COMENTARIO_MULTILINEA(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count('\n')

def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

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
    t.lexer.lineno += len(t.value)

def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = " \t"
    
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
    ('left','AND','OR', 'NOT'),
    ('left','MENOR','MAYOR', 'IGUALIGUAL', 'MENORIGUAL', 'MAYORIGUAL', 'DIFIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO', 'MODULO'),
    ('left', 'POTENCIA'),
    ('right','UMENOS'),
    )
#endregion

# Definición de la gramática
#region Instrucciones
#region ListaInstrucciones
def p_lista_instrucciones_simplea(t):
    '''instrucciones    : instrucciones instruccion '''
    t[0]=t[1]
    t[0].addChild(t[2])

def p_lista_instrucciones_complejas(t):
    '''instrucciones    : instrucciones instruccion_funcion '''
    t[0]=t[1]
    t[0].addChild(t[2])


def p_instruccion_simple(t):
    '''instrucciones    : instruccion '''
    t[0]=GenericoInstruccion(None,getNoNode(),"Instrucciones")
    t[0].addChild(t[1])

def p_instruccion_compleja(t):
    '''instrucciones    : instruccion_funcion '''
    t[0]=GenericoInstruccion(None,getNoNode(),"Instrucciones")
    t[0].addChild(t[1])
#endregion
#region Tipos
def p_tipo_nothing(t):
    'tipo : NOTHING'
    t[0] = NodeTipo(None,getNoNode(),t[1],t.lineno(1), find_column(input, t.slice[1]), DataType.nothing)

def p_tipo_int64(t):
    'tipo : INT64'
    t[0] = NodeTipo(None,getNoNode(),t[1],t.lineno(1), find_column(input, t.slice[1]), DataType.int64)

def p_tipo_float64(t):
    'tipo : FLOAT64'
    t[0] = NodeTipo(None,getNoNode(),t[1],t.lineno(1), find_column(input, t.slice[1]), DataType.float64)

def p_tipo_bool(t):
    'tipo : BOOL'
    t[0] = NodeTipo(None,getNoNode(),t[1],t.lineno(1), find_column(input, t.slice[1]), DataType.bool)
    
def p_tipo_char(t):
    'tipo : CHAR'
    t[0] = NodeTipo(None,getNoNode(),t[1],t.lineno(1), find_column(input, t.slice[1]), DataType.char)

def p_tipo_string(t):
    'tipo : STRING'
    t[0] = NodeTipo(None,getNoNode(),t[1],t.lineno(1), find_column(input, t.slice[1]), DataType.string)
    
#endregion
#region Lista identificadores
def p_lista_ids(t):
    'lista_ids : lista_ids COMA IDENTIFICADOR'
    t[0]=t[1]
    t[0].addChild(GenericoExpresion(None,getNoNode(),","))
    t[0].addChild(TerminalIdentificador(t[3],getNoNode(),t[3], t.lineno(3), find_column(input, t.slice[3]), DataType.nothing))

def p_lista_id(t):
    'lista_ids : IDENTIFICADOR'
    t[0] = ListaIdentificadores(None,getNoNode(),"Lista Identificadores")
    t[0].addChild(TerminalIdentificador(t[1],getNoNode(),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.nothing))
#endregion
#region Instrucciones Complejas
def p_instruccion_funcion(t):
    'instruccion_funcion : instruccion_crea_funcion PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))
#endregion
#region Instruccion Crear Función
def p_instruccion_crea_funcion_sin_parametros(t):
    'instruccion_crea_funcion : FUNCTION IDENTIFICADOR PARIZQ PARDER cuerpo_funcion END'
    t[0] = InstruccionCrearFuncion(None, getNoNode(),"Function")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"function"))
    t[0].addChild(TerminalIdentificador(t[2],getNoNode(),t[2], t.lineno(1), find_column(input, t.slice[1]), DataType.nothing))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"("))
    t[0].addChild(GenericoExpresion(None,getNoNode(),")"))
    t[0].addChild(t[5])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"end"))
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_crea_funcion_con_parametros(t):
    'instruccion_crea_funcion : FUNCTION IDENTIFICADOR PARIZQ lista_parametros PARDER cuerpo_funcion END'
    t[0] = InstruccionCrearFuncionParametros(None, getNoNode(),"Function")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"function"))
    t[0].addChild(TerminalIdentificador(t[2],getNoNode(),t[2], t.lineno(1), find_column(input, t.slice[1]), DataType.nothing))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"("))
    t[0].addChild(t[4])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")"))
    t[0].addChild(t[6])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"end"))
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_lista_parametros(t):
    'lista_parametros : lista_parametros COMA parametro'
    t[0] = t[1]
    t[0].addChild(GenericoExpresion(None,getNoNode(),","))
    t[0].addChild(t[3])

def p_lista_parametro(t):
    'lista_parametros : parametro'
    t[0] = ListaParametros(None,getNoNode(),"Lista Parametros")
    t[0].addChild(t[1])

def p_parametro_tipo(t):
    'parametro : IDENTIFICADOR DOSPTS DOSPTS tipo'
    t[0] = Parametro(None, getNoNode(),"Parametro")
    t[0].addChild(TerminalIdentificador(t[1],getNoNode(),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.nothing))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"::"))
    t[0].addChild(t[4])

def p_parametro(t):
    'parametro : IDENTIFICADOR'
    t[0] = Parametro(None, getNoNode(),"Parametro")
    t[0].addChild(TerminalIdentificador(t[1],getNoNode(),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.generic)) #se agrega tipo de dato generic 

def p_cuerpo_funciones(t):
    'cuerpo_funcion : cuerpo_funcion instruccion'
    t[0]=t[1]
    t[0].addChild(t[2])

def p_cuerpo_funcion(t):
    'cuerpo_funcion : instruccion'
    t[0]=GenericoInstruccion(None,getNoNode(),"Instrucciones")
    t[0].addChild(t[1])

#endregion
#region Instrucciones Simples
def p_instruccion_imprimir(t):
    'instruccion : imprimir PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_asignacion_declaracion(t):
    'instruccion : asignacion_declaracion PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_llamada_funcion(t):
    'instruccion : llamada_funcion PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_instruccion_if(t):
    'instruccion : instruccion_if PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_instruccion_while(t):
    'instruccion : instruccion_while PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_instruccion_for(t):
    'instruccion : instruccion_for PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_instruccion_return(t):
    'instruccion : instruccion_return PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_instruccion_break(t):
    'instruccion : instruccion_break PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_instruccion_continue(t):
    'instruccion : instruccion_continue PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))

def p_instruccion_instruccion_nativa_push(t):
    'instruccion : funcion_nativa_push PTCOMA'
    t[0] = GenericoInstruccion(None, getNoNode(),"Instruccion")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),";"))
    
#endregion
#region Instruccion If
def p_instruccion_if(t):
    'instruccion_if : IF expresion cuerpo_funcion else_if_else END'
    t[0] = InstruccionIf(None,getNoNode(),"Instruccion if")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"if", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(t[2])
    t[0].addChild(t[3])
    if (t[4]!= None):
        t[0].addChild(t[4])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"end", t.lineno(5), find_column(input, t.slice[5])))

def p_else_if_else(t):
    '''else_if_else : ELSEIF expresion cuerpo_funcion else_if_else
                    | ELSE cuerpo_funcion
                    | '''
    if(len(t)==1):
        # Sin else ni elseif
        t[0] = None
    elif(len(t)==3):
        # Con else
        t[0] = InstruccionElse(None,getNoNode(),"Instruccion else")
        t[0].addChild(GenericoExpresion(None,getNoNode(),"else", t.lineno(1), find_column(input, t.slice[1])))
        t[0].addChild(t[2])
    elif(len(t)==5):
        t[0] = InstruccionElseIf(None,getNoNode(),"Instruccion elseif")
        t[0].addChild(GenericoExpresion(None,getNoNode(),"elseif", t.lineno(1), find_column(input, t.slice[1])))
        t[0].addChild(t[2])
        t[0].addChild(t[3])
        if t[4] != None:
            t[0].addChild(t[4])
#endregion
#region Instruccion While
def p_instruccion_while(t):
    'instruccion_while : WHILE expresion cuerpo_funcion END'
    t[0] = InstruccionWhile(None,getNoNode(),"Instruccion While")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"while", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(t[2])
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"end", t.lineno(4), find_column(input, t.slice[4])))
#endregion
#region Instruccion For
def p_instruccion_for_rango(t):
    'instruccion_for : FOR IDENTIFICADOR IN expresion DOSPTS expresion cuerpo_funcion END'
    t[0] = InstruccionForRango(None,getNoNode(),"Instruccion For")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"for", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(TerminalIdentificador(t[2],getNoNode(),t[2], t.lineno(2), find_column(input, t.slice[2]), DataType.nothing))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"in", t.lineno(3), find_column(input, t.slice[3])))
    t[0].addChild(t[4])
    t[0].addChild(GenericoExpresion(None,getNoNode(),":", t.lineno(5), find_column(input, t.slice[5])))
    t[0].addChild(t[6])
    t[0].addChild(t[7])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"end", t.lineno(8), find_column(input, t.slice[8])))

def p_instruccion_for_cadena(t):
    'instruccion_for : FOR IDENTIFICADOR IN expresion cuerpo_funcion END'
    t[0] = InstruccionForCadena(None,getNoNode(),"Instruccion For")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"for", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(TerminalIdentificador(t[2],getNoNode(),t[2], t.lineno(2), find_column(input, t.slice[2]), DataType.nothing))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"in", t.lineno(3), find_column(input, t.slice[3])))
    t[0].addChild(t[4])
    t[0].addChild(t[5])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"end", t.lineno(6), find_column(input, t.slice[6])))
#endregion
#region Instruccion Asignacion Declaracion
def p_instruccion_declaracion(t):
    'asignacion_declaracion : IDENTIFICADOR IGUAL expresion DOSPTS DOSPTS tipo'
    t[0] = InstruccionDeclaracion(None, getNoNode(),"Declaracion")
    t[0].addChild(TerminalIdentificador(t[1],getNoNode(),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.nothing))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"="))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"::"))
    t[0].addChild(t[6])

def p_instruccion_asignacion(t):
    'asignacion_declaracion : IDENTIFICADOR IGUAL expresion'
    t[0] = InstruccionAsignacion(None, getNoNode(),"Asignacion")
    t[0].addChild(TerminalIdentificador(t[1],getNoNode(),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.nothing))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"="))
    t[0].addChild(t[3])

def p_instruccion_asignacion_arreglo(t):
    'asignacion_declaracion : IDENTIFICADOR CORIZQ expresion CORDER asignacion_declaracion_array_multi IGUAL expresion'
    t[0] = AsignacionAPosicion(None,getNoNode(),"Asignacion a posicion")
    nuevaPos = TerminalPosicionArray(None,getNoNode(),"Posicion")
    nuevaPos.addChild(GenericoExpresion(None,getNoNode(),"["))
    nuevaPos.addChild(t[3])
    nuevaPos.addChild(GenericoExpresion(None,getNoNode(),"]"))
    t[5].hijos.insert(0,nuevaPos)
    t[0].addChild(TerminalIdentificador(t[1],getNoNode(),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.identificador))
    t[0].addChild(t[5])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"="))
    t[0].addChild(t[7])


def p_instruccion_asignacion_arreglo_posicion(t):
    '''asignacion_declaracion_array_multi : CORIZQ expresion CORDER asignacion_declaracion_array_multi
                                    |'''
    if (len(t)==5):
        t[0]=t[4]
        nuevaPos = TerminalPosicionArray(None,getNoNode(),"Posicion")
        nuevaPos.addChild(GenericoExpresion(None,getNoNode(),"["))
        nuevaPos.addChild(t[2])
        nuevaPos.addChild(GenericoExpresion(None,getNoNode(),"]"))
        t[0].hijos.insert(0,nuevaPos)
    else:
        t[0] = ArregloAPosicion(None,getNoNode(),"Arreglo a posicion")
    
#endregion
#region Instrucción imprimir
def p_imprimir_println(t):
    'imprimir : PRINTLN PARIZQ lista_expresion PARDER'
    t[0] = InstruccionPrintln(None,getNoNode(),"Instruccion println")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"println"))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"("))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")"))
    

def p_imprimir_print(t):
    'imprimir : PRINT PARIZQ lista_expresion PARDER'
    t[0] = InstruccionPrint(None,getNoNode(),"Instruccion print")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"println"))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"("))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")"))
#endregion
#region Instrucción Llamada a funciones
def p_llamada_funcion_sin_parametros(t):
    'llamada_funcion : IDENTIFICADOR PARIZQ PARDER'
    t[0] = InstruccionLlamadaFuncion(None,getNoNode(),"Llamada Funcion")
    t[0].addChild(TerminalIdentificador(t[1],getNoNode(),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.nothing))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"("))
    t[0].addChild(GenericoExpresion(None,getNoNode(),")"))

def p_llamada_funcion_con_parametros(t):
    'llamada_funcion : IDENTIFICADOR PARIZQ lista_expresion PARDER'
    t[0] = InstruccionLlamadaFuncionParam(None,getNoNode(),"Llamada Funcion")
    t[0].addChild(TerminalIdentificador(t[1],getNoNode(),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.nothing))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"("))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")"))
#endregion
#region Funciones Nativas
def p_funcion_uppercase(t):
    'funcion_nativa : UPPERCASE PARIZQ expresion PARDER'
    t[0] = FuncionUppercase(None,getNoNode(),"Funcion uppercase")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"uppercase", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_lowercase(t):
    'funcion_nativa : LOWERCASE PARIZQ expresion PARDER'
    t[0] = FuncionLowercase(None,getNoNode(),"Funcion lowercase")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"lowercase", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_log10(t):
    'funcion_nativa : LOG10 PARIZQ expresion PARDER'
    t[0] = FuncionLog10(None,getNoNode(),"Funcion logaritmo10")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"log10", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_log(t):
    'funcion_nativa : LOG PARIZQ expresion COMA expresion PARDER'
    t[0] = FuncionLog(None,getNoNode(),"Funcion logaritmo")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"log", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),",", t.lineno(4), find_column(input, t.slice[4])))
    t[0].addChild(t[5])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(6), find_column(input, t.slice[6])))

def p_funcion_sin(t):
    'funcion_nativa : SIN PARIZQ expresion PARDER'
    t[0] = FuncionSin(None,getNoNode(),"Funcion sin")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"sin", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_cos(t):
    'funcion_nativa : COS PARIZQ expresion PARDER'
    t[0] = FuncionCos(None,getNoNode(),"Funcion sin")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"cos", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_tan(t):
    'funcion_nativa : TAN PARIZQ expresion PARDER'
    t[0] = FuncionTan(None,getNoNode(),"Funcion tan")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"tan", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_sqrt(t):
    'funcion_nativa : SQRT PARIZQ expresion PARDER'
    t[0] = FuncionSqrt(None,getNoNode(),"Funcion sqrt")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"sqrt", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_parse(t):
    'funcion_nativa : PARSE PARIZQ tipo COMA expresion PARDER'
    t[0] = FuncionParse(None,getNoNode(),"Funcion parse")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"parse", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),",", t.lineno(4), find_column(input, t.slice[4])))
    t[0].addChild(t[5])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(6), find_column(input, t.slice[6])))

def p_funcion_trunc(t):
    'funcion_nativa : TRUNC PARIZQ tipo COMA expresion PARDER'
    t[0] = FuncionTrunc(None,getNoNode(),"Funcion trunc")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"trunc", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),",", t.lineno(4), find_column(input, t.slice[4])))
    t[0].addChild(t[5])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(6), find_column(input, t.slice[6])))

def p_funcion_float(t):
    'funcion_nativa : FLOAT PARIZQ expresion PARDER'
    t[0] = FuncionFloat(None,getNoNode(),"Funcion float")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"float", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_string(t):
    'funcion_nativa : FSTR PARIZQ expresion PARDER'
    t[0] = FuncionString(None,getNoNode(),"Funcion string")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"string", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_typeof(t):
    'funcion_nativa : TYPEOF PARIZQ expresion PARDER'
    t[0] = FuncionTypeof(None,getNoNode(),"Funcion typeof")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"typeof", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_length(t):
    'funcion_nativa : LENGTH PARIZQ expresion PARDER'
    t[0] = FuncionLength(None,getNoNode(),"Funcion length")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"length", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(2), find_column(input, t.slice[2])))
    t[0].addChild(t[3])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(4), find_column(input, t.slice[4])))

def p_funcion_pop(t):
    'funcion_nativa : POP NOT PARIZQ IDENTIFICADOR acceso_posicion_array_multi PARDER'
    t[0] = FuncionPop(None,getNoNode(),"Funcion pop")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"pop!", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(3), find_column(input, t.slice[3])))
    t[0].addChild(TerminalIdentificador(t[4],getNoNode(),t[4], t.lineno(4), find_column(input, t.slice[4]), DataType.identificador))
    temporal = AccesoAArreglo(None,getNoNode(),"Acceso a Arreglo")
    for x in t[5].hijos:
        temporal.addChild(x)
    t[0].addChild(temporal)
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(6), find_column(input, t.slice[6])))

def p_funcion_push(t):
    'funcion_nativa_push : PUSH NOT PARIZQ IDENTIFICADOR acceso_posicion_array_multi COMA expresion PARDER'
    t[0] = FuncionPush(None,getNoNode(),"Funcion pop")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"push!", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(GenericoExpresion(None,getNoNode(),"(", t.lineno(3), find_column(input, t.slice[3])))
    t[0].addChild(TerminalIdentificador(t[4],getNoNode(),t[4], t.lineno(4), find_column(input, t.slice[4]), DataType.identificador))
    temporal = AccesoAArreglo(None,getNoNode(),"Acceso a Arreglo")
    for x in t[5].hijos:
        temporal.addChild(x)
    t[0].addChild(temporal)
    t[0].addChild(GenericoExpresion(None,getNoNode(),",", t.lineno(6), find_column(input, t.slice[6])))
    t[0].addChild(t[7])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")", t.lineno(8), find_column(input, t.slice[8])))

#endregion
#region Return
def p_instruccion_return(t):
    'instruccion_return : RETURN'
    t[0] = InstruccionReturn(None,getNoNode(),"Funcion return")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"return", t.lineno(1), find_column(input, t.slice[1])))

def p_instruccion_return_valor(t):
    'instruccion_return : RETURN expresion'
    t[0] = InstruccionReturnValor(None,getNoNode(),"Funcion return")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"return", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addChild(t[2])
#endregion

#region Break
def p_instruccion_break(t):
    'instruccion_break : BREAK'
    t[0] = InstruccionBreak(None,getNoNode(),"Funcion break")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"break", t.lineno(1), find_column(input, t.slice[1])))
#endregion
#region Continue
def p_instruccion_continue(t):
    'instruccion_continue : CONTINUE'
    t[0] = InstruccionContinue(None,getNoNode(),"Funcion continue")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"break", t.lineno(1), find_column(input, t.slice[1])))
#endregion


#region Expresion
#region ListaExpresiones
def p_lista_expresiones(t):
    'lista_expresion : lista_expresion COMA expresion'
    t[0]=t[1]
    t[0].addChild(GenericoExpresion(None,getNoNode(),","))
    t[0].addChild(t[3])

def p_lista_expresion(t):
    'lista_expresion : expresion'
    t[0] = NodeListaExpresiones(None,getNoNode(),"Lista Exp")
    t[0].addChild(t[1])
#endregion
#region Relacionales
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
#region Logicas
def p_expresion_or(t):
    'expresion : expresion OR expresion'
    t[0] = NodeOr(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"||"))
    t[0].addChild(t[3])

def p_expresion_and(t):
    'expresion : expresion AND expresion'
    t[0] = NodeAnd(None, getNoNode(), "E")
    t[0].addChild(t[1])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"&&"))
    t[0].addChild(t[3])

def p_expresion_not(t):
    'expresion : NOT expresion'
    t[0] = NodeNot(None, getNoNode(), "E")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"!"))
    t[0].addChild(t[2])

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
    t[0] = NodeNegativo(None,getNoNode(),"E")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"-"))
    t[0].addChild(t[2])


def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = NodeAgrupacion(None, getNoNode(), "E")
    t[0].addChild(GenericoExpresion(None,getNoNode(),"("))
    t[0].addChild(t[2])
    t[0].addChild(GenericoExpresion(None,getNoNode(),")"))
    #print("Parentesis")
#endregion
#region Terminales con Tipo de Dato
def p_expresion_entero(t):
    '''expresion    : ENTERO'''
    t[0] = TerminalEntero(t[1], str(getNoNode()),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.int64)

def p_expresion_decimal(t):
    '''expresion    : DECIMAL'''
    t[0] = TerminalDecimal(t[1], str(getNoNode()),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.float64)

def p_expresion_cadena(t):
    '''expresion    : CADENA'''
    t[0] = TerminalCadena(t[1], str(getNoNode()),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.string)

def p_expresion_identificador(t):
    '''expresion    : IDENTIFICADOR'''
    t[0] = TerminalIdentificador(t[1], str(getNoNode()),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.identificador)

def p_expresion_verdadero(t):
    'expresion : TRUE'
    t[0] = TerminalVerdadero(True, str(getNoNode()),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.bool)

def p_expresion_falso(t):
    'expresion : FALSE'
    t[0] = TerminalFalso(False, str(getNoNode()),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.bool)

def p_expresion_uppercase(t):
    'expresion      : funcion_nativa'
    t[0] = t[1]

def p_expresion_llamada_funcion(t):
    'expresion      : llamada_funcion'
    t[0] = t[1]

def p_expresion_declaracion_arreglo(t):
    'expresion      : declaracion_arreglo'
    t[0] = t[1]

def p_expresion_posicion_array(t):
    'expresion      : acceso_posicion_array '
    t[0] = t[1]
#endregion
#region Declaración arreglo
def p_declaracion_arreglo(t):
    'declaracion_arreglo : CORIZQ lista_expresion CORDER'
    t[0] = TerminalArreglo(None, str(getNoNode()),"Arreglo", t.lineno(1), find_column(input, t.slice[1]), DataType.array)
    t[0].addChild(GenericoExpresion(None,getNoNode(),"["))
    t[0].addChild(t[2])
    t[0].addChild(GenericoExpresion(None,getNoNode(),"]"))


def p_posicion_array(t):
    'acceso_posicion_array : IDENTIFICADOR CORIZQ expresion CORDER acceso_posicion_array_multi'
    t[0] = t[5]
    nuevaPos = TerminalPosicionArray(None,getNoNode(),"Posicion")
    nuevaPos.addChild(GenericoExpresion(None,getNoNode(),"["))
    nuevaPos.addChild(t[3])
    nuevaPos.addChild(GenericoExpresion(None,getNoNode(),"]"))
    t[0].hijos.insert(0,nuevaPos)
    t[0].hijos.insert(0,TerminalIdentificador(t[1],getNoNode(),t[1], t.lineno(1), find_column(input, t.slice[1]), DataType.identificador))

def p_posicion_array_multi(t):
    '''acceso_posicion_array_multi : CORIZQ expresion CORDER acceso_posicion_array_multi
                                    |'''
    if (len(t)==5):
        t[0]=t[4]
        nuevaPos = TerminalPosicionArray(None,getNoNode(),"Posicion")
        nuevaPos.addChild(GenericoExpresion(None,getNoNode(),"["))
        nuevaPos.addChild(t[2])
        nuevaPos.addChild(GenericoExpresion(None,getNoNode(),"]"))
        t[0].hijos.insert(0,nuevaPos)
    else:
        t[0] = AccesoAPosicion(None,getNoNode(),"Acceso a Posicion")
    
    
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
    global input
    input = entrada
    global noNode
    noNode = 0;
    return parser.parse(entrada)