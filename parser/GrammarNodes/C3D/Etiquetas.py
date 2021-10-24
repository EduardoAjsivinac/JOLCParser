from parser.GrammarNodes.Tipo.DataType import DataType, TypeCheckerC3DTable


class C3DAux(object):

    __instance = None
    nombre = None
    label = 0
    temp = 0
    arreglo = "heap"

    def getArreglo(self):
        return self.arreglo
    
    def changeArreglo(self):
        if self.arreglo == "heap":
            self.arreglo = "stack"
        else:
            self.arreglo = "heap"

    def getLabel(self):
        self.label +=1
        return str("L"+str(self.label))

    def getTemp(self):
        self.temp +=1
        return str("t"+str(self.temp-1))

    def __new__(cls):
        if C3DAux.__instance is None:
            C3DAux.__instance = object.__new__(cls)
        return C3DAux.__instance
    


    #region
    # Traducción C3D
    #region Aritmeticas
    def traducirAritmetica(self, operacion, nodo1, nodo2, tablaSimbolos, padre):
        if nodo2 != None:
            padre.tipo = TypeCheckerC3DTable(operacion,tablaSimbolos,nodo1,nodo2)
        else:
            #es negativo
            if nodo1.tipo == DataType.int64 or nodo1.tipo == DataType.float64:
                padre.tipo = DataType.nodo1.tipo
                neg = self.getTemp()
                nodo1.referencia = self.getTemp()
                nodo1.expresion += str(neg)+ " = 0 - 1;\n"
                nodo1.expresion +=str(nodo1.referencia) + " = " + str(nodo1.referencia) + " * " +str(neg) + "; \n"
                return
            else:
                padre.tipo = DataType.error
        if padre.tipo != DataType.error:
            self.convertirEtiquetas(nodo1)
            self.convertirEtiquetas(nodo2)
            padre.expresion = nodo1.expresion
            padre.expresion += nodo2.expresion
            padre.referencia = self.getTemp()
            if operacion == "/":
                etv = self.getLabel()
                # Comprobación de división entre 0
                padre.expresion += "if ( "+ str(nodo2.referencia) +" != 0 ){ goto "+str(etv)+" }"
                padre.expresion += '''fmt.Printf("%c", 77);\n'''
                padre.expresion += '''fmt.Printf("%c", 97);\n'''
                padre.expresion += '''fmt.Printf("%c", 116);\n'''
                padre.expresion += '''fmt.Printf("%c", 104);\n'''
                padre.expresion += '''fmt.Printf("%c", 69);\n'''
                padre.expresion += '''fmt.Printf("%c", 114);\n'''
                padre.expresion += '''fmt.Printf("%c", 114);\n'''
                padre.expresion += '''fmt.Printf("%c", 111);\n'''
                padre.expresion += '''fmt.Printf("%c", 114);\n'''
                padre.expresion += padre.referencia + " = 0;\n"
                etv2 = self.getLabel()
                padre.expresion += "goto "+ str(etv2) +";\n"
                padre.expresion += str(etv)+":\n"
                padre.expresion += str(padre.referencia) + " = " + str(nodo1.referencia) +" "+ str(operacion) + " " + str(nodo2.referencia) + ";\n"
                padre.expresion += str(etv2)+":\n"
                return
            elif operacion == "^":
                padre.expresion += str(padre.referencia) + " = " + str(nodo1.referencia) + "\n"
                tmp1 = self.getTemp()
                lbl1 = self.getLabel()
                lbl2 = self.getLabel()
                padre.expresion += str(tmp1) + " = 1;\n"
                padre.expresion += str(lbl1)+ ":\n"
                padre.expresion += "if ( " + str(tmp1) + " >= " + str(nodo2.referencia) + "){goto "+str(lbl2)+"}\n"
                padre.expresion += str(padre.referencia) + " = " + str(padre.referencia) + " * " +  str(nodo1.referencia)+";\n"
                padre.expresion += str(tmp1) + " = " + str(tmp1) + " + 1;\n"
                padre.expresion += "goto " + str(lbl1) + "\n"
                padre.expresion += str(lbl2) + ":\n"
                return
            padre.expresion += str(padre.referencia) + " = " + str(nodo1.referencia) +" "+ str(operacion) + " " + str(nodo2.referencia) + ";\n"

    def convertirEtiquetas(self, nodo):
        if len(nodo.ev) >0 or len(nodo.ef) >0:
            tmp = self.getTemp()
            etq = self.getLabel()
            nodo.referencia = tmp
            for x in nodo.ev:
                nodo.expresion += x + ":\n"
            nodo.expresion+= str(tmp) + " = 1;\n"
            nodo.expresion += "goto " + str(etq) + "\n"
            for x in nodo.ef:
                nodo.expresion += x + ":\n"
            nodo.expresion+= str(tmp) + " = 0;\n"
            nodo.expresion += str(etq) + ":\n"
    #endregion
    

    #region Relacionales
    def traducirRelacional(self, operacion, nodo1, nodo2, tablaSimbolos, padre):
        padre.tipo = TypeCheckerC3DTable(operacion,tablaSimbolos,nodo1,nodo2)
        if padre.tipo != DataType.error:
            expresion1 = ""
            expresion2 = ""
            self.convertirBooleano(nodo1,expresion1)
            self.convertirBooleano(nodo2,expresion2)
            padre.expresion += nodo1.expresion
            padre.expresion += nodo2.expresion
            evt = self.getLabel()
            eft = self.getLabel()
            padre.expresion += "if("+ str(nodo1.referencia)+" "+operacion+" " + str(nodo2.referencia)+") {goto "+str(evt)+"}\n"
            padre.expresion += "goto "+str(eft) + "\n"
            padre.ev.append(evt)
            padre.ef.append(eft)
            padre.referencia = self.getTemp()
    
    def convertirBooleano(self, nodo, expresion):
        if len(nodo.ev) == 0 and len(nodo.ef)==0:
            ev = self.getLabel()
            ef = self.getLabel()
            nodo.ev.append(ev)
            nodo.ef.append(ef)
            expresion += "if("+str(nodo.referencia)+" == 1) {goto "+str(ev)+"}\n"
            expresion += "goto "+str(ef)+"\n"
    #endregion

    #endregion