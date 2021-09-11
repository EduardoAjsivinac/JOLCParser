import enum



class DataType(enum.Enum):    
    error =0
    nothing = 1
    int64 = 2
    float64 = 3
    bool = 4
    char = 5
    string = 6
    array = 7
    struct = 8
    identificador = 9
    generic = 10

matriz_checker =[
    [0,0,0,0,0,0,0,0,0], # Todo Error
    [0,1,1,1,1,1,1,1,1], # Nothing
    [0,1,2,3,0,0,0,0,0], # Int64
    [0,1,3,3,0,0,0,0,0], # Float64
    [0,0,0,0,4,0,0,0,0], # bool
    [0,0,0,0,0,6,6,0,0], # char
    [0,0,0,0,0,6,6,0,0], # string
    [0,0,0,0,0,0,0,0,0], # array
    [0,0,0,0,0,0,0,0,0] # struct
]

# Error
# Nothing
# Int64
# Float64
# Bool
# Char
# String
# Array
# Struct
matrizoperation={'+':[0,1,2,3,4,5,6,7,8]}

matrizchecker = {
    '+' : {
            DataType.int64 : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64,
                DataType.char : DataType.char
            },DataType.float64 : {
                DataType.int64 : DataType.float64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.float64
            },DataType.bool : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64,
                DataType.char : DataType.char
            },DataType.char : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.char
            }
        },
    '-' : {
            DataType.int64 : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64
            },DataType.float64 : {
                DataType.int64 : DataType.float64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.float64
            },DataType.bool : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64
            }
        },
    '*' : {
            DataType.int64 : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64
            },DataType.float64 : {
                DataType.int64 : DataType.float64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.float64
            },DataType.bool : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64
            },DataType.string : {
                DataType.string : DataType.string
            }
        },
    '/' : {
            DataType.int64 : {
                DataType.int64 : DataType.float64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.float64
            },DataType.float64 : {
                DataType.int64 : DataType.float64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.float64
            },DataType.bool : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64
            }
        },
    '%' : {
            DataType.int64 : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64
            },DataType.float64 : {
                DataType.int64 : DataType.float64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.float64
            },DataType.bool : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64
            }
        },
    '^' : {
            DataType.int64 : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64
            },DataType.float64 : {
                DataType.int64 : DataType.float64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.float64
            },DataType.bool : {
                DataType.int64 : DataType.int64,
                DataType.float64 : DataType.float64,
                DataType.bool : DataType.int64
            },DataType.string : {
                DataType.int64 : DataType.string,
                DataType.bool : DataType.string
            }
        },
    '!=' : {
            DataType.nothing : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.int64 : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.float64 : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.bool : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.char : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.string : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            }
        },
    '==' : {

            DataType.nothing : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.int64 : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.float64 : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.bool : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.char : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            },DataType.string : {
                DataType.nothing : DataType.bool,
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool,
                DataType.char : DataType.bool,
                DataType.string : DataType.bool
            }
        },
    '<' : {
            DataType.int64 : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.float64 : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.bool : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.char : {
                DataType.char : DataType.bool
            },DataType.string : {
                DataType.string : DataType.bool
            }
        },
    '>' : {
            DataType.int64 : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.float64 : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.bool : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.char : {
                DataType.char : DataType.bool
            },DataType.string : {
                DataType.string : DataType.bool
            }
        },
    '<=' : {
            DataType.int64 : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.float64 : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.bool : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.char : {
                DataType.char : DataType.bool
            },DataType.string : {
                DataType.string : DataType.bool
            }
        },
    '>=' : {
            DataType.int64 : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.float64 : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.bool : {
                DataType.int64 : DataType.bool,
                DataType.float64 : DataType.bool,
                DataType.bool : DataType.bool
            },DataType.char : {
                DataType.char : DataType.bool
            },DataType.string : {
                DataType.string : DataType.bool
            }
        }
}

merror = {DataType.error:DataType.error}


def TypeChecker(op, enviroment, firstnode, secondnode):
    # Se crea la matriz de validaciones
    firstType = firstnode.tipo
    secondType = secondnode.tipo
    tipo = matrizchecker.get(op,merror).get(firstType,merror).get(secondType,merror.get(DataType.error))
    if (tipo!= DataType.error):
        return tipo
    if (firstType != DataType.error and secondType != DataType.error):
        descripcion =""
        if(firstnode.isIdentifier and not firstnode.identifierDeclare):
            descripcion = "La variable <b>" + firstnode.texto + "</b> no está declarada"
        elif(secondnode.isIdentifier and not secondnode.identifierDeclare):
            descripcion = "La variable <b>" + secondnode.texto + "</b> no está declarada"
        else:
            descripcion = "<b>"+ firstType.name + "</b> es incompatible con <b>"+ secondType.name + "</b> para la operacion <b>" + op + "</b>"
        enviroment.addError(descripcion, secondnode.fila, secondnode.columna)
    return tipo