from parser.GrammarNodes.Tipo.DataType import DataType, TypeCheckerC3DTable


class C3DAux(object):

    __instance = None
    nombre = None
    label = 0
    temp = 0
    arreglo = "heap"
    librerias = {}

    def agregarLibreria(self,nombre):
        self.librerias[nombre] = nombre
        
    def getArreglo(self):
        return self.arreglo

    def getPointer(self):
        if self.arreglo == "heap":
            return "hp"
        else:
            return "sp"
    
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
            if padre.tipo != DataType.string:
                self.convertirEtiquetas(nodo1)
                self.convertirEtiquetas(nodo2)
                padre.expresion = nodo1.expresion
                padre.expresion += nodo2.expresion
                padre.referencia = self.getTemp()
                if operacion == "/":
                    self.agregarLibreria("fmt")
                    etv = self.getLabel()
                    # Comprobación de división entre 0
                    padre.expresion += "if ( "+ str(nodo2.referencia) +" != 0 ){ goto "+str(etv)+" }\n"
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
                    padre.expresion += str(padre.referencia) + " = " + str(nodo1.referencia) + ";\n"
                    tmp1 = self.getTemp()
                    lbl1 = self.getLabel()
                    lbl2 = self.getLabel()
                    etqPot0 = self.getLabel()
                    padre.expresion += "if("+str(nodo2.referencia)+" != 0){goto "+str(etqPot0)+"}\n" 
                    padre.expresion += str(padre.referencia) + " = 1;\n"
                    padre.expresion += "goto "+str(lbl2)+"\n"
                    padre.expresion += str(etqPot0)+":\n"
                    padre.expresion += str(tmp1) + " = 1;\n"
                    padre.expresion += str(lbl1)+ ":\n"
                    padre.expresion += "if ( " + str(tmp1) + " >= " + str(nodo2.referencia) + "){goto "+str(lbl2)+"}\n"
                    padre.expresion += str(padre.referencia) + " = " + str(padre.referencia) + " * " +  str(nodo1.referencia)+";\n"
                    padre.expresion += str(tmp1) + " = " + str(tmp1) + " + 1;\n"
                    padre.expresion += "goto " + str(lbl1) + "\n"
                    padre.expresion += str(lbl2) + ":\n"
                    return
                elif operacion == "%":
                    self.agregarLibreria("math")
                    padre.expresion += str(padre.referencia) + " = math.Mod(" + str(nodo1.referencia) +" , " + str(nodo2.referencia) + ");\n"
                    return
                padre.expresion += str(padre.referencia) + " = " + str(nodo1.referencia) +" "+ str(operacion) + " " + str(nodo2.referencia) + ";\n"
            else:
                if (operacion == "*"):
                    padre.expresion += nodo1.expresion
                    padre.expresion += nodo2.expresion
                    padre.referencia = self.getTemp()
                    tamC1 = self.getTemp()
                    tamC2 = self.getTemp()
                    cont = self.getTemp()
                    chr1 = self.getTemp()
                    poaschar = self.getTemp()
                    etIni = self.getLabel()
                    etIni2 = self.getLabel()
                    etFin1 = self.getLabel()
                    etFin2 = self.getLabel()
                    padre.expresion += str(tamC1)+ " = " + self.getArreglo() + "[int(" + str(nodo1.referencia) +  ")];\n"
                    padre.expresion += str(tamC2)+ " = " + self.getArreglo() + "[int(" + str(nodo2.referencia) +  ")];\n"
                    
                    padre.expresion += str(padre.referencia) + " = "+ self.getPointer() +";\n"
                    padre.expresion += str(cont) + " = " + str(tamC1)+ " + " + str(tamC2) + ";\n"
                    padre.expresion += self.getArreglo() +  "[int("+str(padre.referencia) + ")] = " + str(cont) + ";\n"
                    padre.expresion += str(cont) + " = 1;\n"
                    padre.expresion += self.getPointer() + " = " + self.getPointer() + " + 1;\n"

                    padre.expresion += str(etIni) +  ":\n"
                    padre.expresion += "if ("+str(tamC1)+" < " + str(cont) + ") {goto "+str(etFin1)+"}\n"
                    # Se hace el procedimiento con cadenas
                    padre.expresion += str(poaschar) + " = " + str(cont) + " + " + str(nodo1.referencia)+";\n"
                    padre.expresion += str(chr1) + " = " + self.getArreglo() + "[int(" +str(poaschar) + ")];\n" #Se obtiene el caracter n
                    padre.expresion += self.getArreglo() + "[int(" + self.getPointer()+")] = " + str(chr1) + ";\n"
                    padre.expresion += self.getPointer()+ " = " + self.getPointer() + " + 1;\n"
                    padre.expresion += str(cont) + " = "+str(cont)+" + 1;\n"
                    padre.expresion += "goto "+str(etIni) + "\n"
                    padre.expresion += str(etFin1) + ":\n"

                    padre.expresion += str(cont) + " = 1;\n" 

                    padre.expresion += str(etIni2) +  ":\n"
                    padre.expresion += "if ("+str(tamC2)+" < " + str(cont) + ") {goto "+str(etFin2)+"}\n"
                    # Se hace el procedimiento con cadenas
                    padre.expresion += str(poaschar) + " = " + str(cont) + " + " + str(nodo2.referencia)+";\n"
                    padre.expresion += str(chr1) + " = " + self.getArreglo() + "[int(" +str(poaschar) + ")];\n" #Se obtiene el caracter n
                    padre.expresion += self.getArreglo() + "[int(" + self.getPointer()+")] = " + str(chr1) + ";\n"
                    padre.expresion += self.getPointer() + " = " + self.getPointer() + " + 1;\n"
                    padre.expresion += str(cont) + " = "+str(cont)+" + 1;\n"
                    padre.expresion += "goto "+str(etIni2) + "\n"
                    padre.expresion += str(etFin2) + ":\n"
                    padre.expresion += self.getPointer()+" = "+self.getPointer()+" + "+str(tamC1)+";\n"
                    padre.expresion += self.getPointer()+" = "+self.getPointer()+" + "+str(tamC2)+";\n"
                    padre.expresion += self.getPointer()+" = "+self.getPointer()+" + 1;\n"
                    #tablaSimbolos.setNextPosHeap(posHeap+padre.size+1)
                elif(operacion == "^"):
                    print("Ref: ",nodo2.referencia, padre.size)
                    padre.expresion += nodo1.expresion
                    padre.expresion += nodo2.expresion
                    padre.referencia = self.getTemp()
                    padre.expresion += "\n//Inicia Aumento\n\n"
                    padre.expresion += str(padre.referencia) + " = " + self.getPointer() + ";\n"
                    
                    # Calculo del tamaño de la cadena
                    tamCad = self.getTemp() # Temporal donde se almacenará el tamaño de la cadena
                    tmpCad = self.getTemp()
                    padre.expresion += str(tmpCad) + " = " +self.getArreglo()+"[int("+ str(nodo1.referencia)+")];\n"
                    padre.expresion += str(tamCad) + " = " + str(tmpCad) + " * " + str(nodo2.referencia)+";\n"
                    padre.expresion += self.getArreglo()+"[int("+str(padre.referencia)+")] = "+ str(tamCad) + ";\n"
                    padre.expresion += self.getPointer() + " = " + self.getPointer() + " + 1;\n"

                    tmpContador = self.getTemp()
                    etqSalida = self.getLabel()
                    etqCiclo = self.getLabel()
                    tmpCont2 = self.getTemp()
                    etqTemp = self.getLabel()
                    tmpCharAc = self.getTemp()
                    tmpPosChar = self.getTemp()
                    # Inicia inserción
                    padre.expresion += str(tmpContador)+" = 0;\n"
                    padre.expresion += str(tmpCont2)+" = 0;\n"
                    padre.expresion += str(etqCiclo)+":\n"
                    padre.expresion += "if("+str(tmpContador)+">="+str(tamCad)+"){goto "+str(etqSalida)+"}\n"
                    padre.expresion += str(tmpContador)+" = "+str(tmpContador)+" + 1;\n"
                    padre.expresion += str(tmpCont2) + " = "+str(tmpCont2) +" + 1;\n"

                    padre.expresion += str(tmpPosChar) + " = " + str(tmpCont2) + " + "+ str(nodo1.referencia)+";\n"
                    padre.expresion += str(tmpCharAc) + " = " + self.getArreglo() + "[int("+str(tmpPosChar)+")];\n"

                    padre.expresion += self.getArreglo()+"[int("+self.getPointer()+")] = "+str(tmpCharAc)+";\n"

                    #padre.expresion += "fmt.Println(hp, "+str(tmpCharAc)+");\n"

                    padre.expresion += "if("+str(tmpCont2)+"<"+str(tmpCad)+"){goto "+str(etqTemp)+"}\n"
                    padre.expresion += str(tmpCont2) + " = 0;\n"
                    padre.expresion += str(etqTemp)+":\n"
                    padre.expresion += self.getPointer() + " = " + self.getPointer() + " +1;\n"
                    padre.expresion += "goto "+ str(etqCiclo)+"\n"
                    padre.expresion += str(etqSalida)+":\n"


                    #padre.expresion += "fmt.Println("+self.getArreglo()+"[int("+str(padre.referencia)+")]);\n"

                    padre.expresion += "\n//Finaliza Aumento\n\n"

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
            padre.tipo = DataType.bool
            if nodo1.tipo != DataType.string and nodo2.tipo != DataType.string:
                print(nodo1.tipo, nodo2.tipo)
                if nodo1.tipo == DataType.bool:
                    self.convertirBooleano(nodo1)
                if nodo2.tipo == DataType.bool:
                    self.convertirBooleano(nodo2)
                padre.expresion += nodo1.expresion
                padre.expresion += nodo2.expresion
                if len(nodo1.ev)>0 and  len(nodo1.ef)>0:
                    tmpS = self.getLabel()
                    if len(nodo1.ev)>0:
                        for x in nodo1.ev:
                            padre.expresion += str(x)+":\n"
                        padre.expresion += str(nodo1.referencia) + " = 1;\n"
                        
                        padre.expresion += "goto "+str(tmpS)+"\n"
                    if len(nodo1.ef)>0:
                        for x in nodo1.ef:
                            padre.expresion += str(x)+":\n"
                        padre.expresion += str(nodo1.referencia) + " = 0;\n"
                    if len(nodo1.ev)>0:
                        padre.expresion += str(tmpS)+":\n"
                
                if len(nodo2.ev)>0 and  len(nodo2.ef)>0:
                    tmpS = self.getLabel()
                    if len(nodo2.ev)>0:
                        for x in nodo2.ev:
                            padre.expresion += str(x)+":\n"
                        padre.expresion += str(nodo2.referencia) + " = 1;\n"
                        
                        padre.expresion += "goto "+str(tmpS)+"\n"
                    if len(nodo2.ef)>0:
                        for x in nodo2.ef:
                            padre.expresion += str(x)+":\n"
                        padre.expresion += str(nodo2.referencia) + " = 0;\n"
                    if len(nodo2.ev)>0:
                        padre.expresion += str(tmpS)+":\n"

                evt = self.getLabel()
                eft = self.getLabel()
                padre.expresion += "if("+ str(nodo1.referencia)+" "+operacion+" " + str(nodo2.referencia)+") {goto "+str(evt)+"}\n"
                padre.expresion += "goto "+str(eft) + "\n"
                padre.ev.append(evt)
                padre.ef.append(eft)
                padre.referencia = self.getTemp()
            else: #comparar strings
                # ==
                # <=
                # >=
                # !=
                # <
                # >
                # Se obtiene la referencia de las dos cadenas
                tam1 = self.getTemp()
                tam2 = self.getTemp()
                padre.expresion += str(tam1) + " = " + self.getArreglo() + "[int("+nodo1.referencia+")];\n"
                padre.expresion += str(tam2) + " = " + self.getArreglo() + "[int("+nodo2.referencia+")];\n"
                cnt1 = self.getTemp()
                cnt2 = self.getTemp()
                padre.expresion += str(cnt1) + " = 1;\n"
                padre.expresion += str(cnt2) + " = 1;\n"
                etqSalto = self.getLabel()
                etv1 = self.getLabel()
                # etf1 = self.getLabel()
                etv2 = self.getLabel()
                # etf2 = self.getLabel()
                padre.expresion += str(etqSalto)+ ":\n"
                # Valida final de cadena
                padre.expresion += "if (" +cnt1 + " >= " + str(tam1)+") {goto "+str(etv1)+" }\n"
                padre.expresion += "if (" +cnt2 + " >= " + str(tam2)+") {goto "+str(etv2)+" }\n"
                tmpChr1 = self.getTemp()
                tmpChr2 = self.getTemp()
                posArray1 = self.getTemp()
                posArray2 = self.getTemp()
                padre.expresion += str(posArray1) + " = " + str(cnt1) + " + " + str(nodo1.referencia) + ";\n"
                padre.expresion += str(posArray2) + " = " + str(cnt2) + " + " + str(nodo2.referencia) + ";\n"
                padre.expresion += str(tmpChr1)+ " = " + self.getArreglo() + "[int("+str(posArray1)+")];\n"
                padre.expresion += str(tmpChr2)+ " = " + self.getArreglo() + "[int("+str(posArray2)+")];\n"
                padre.expresion += "if ("+str(tmpChr1) +" "+ operacion + " " +str(tmpChr2)+"){goto }"
    
    
    
    def convertirBooleano(self, nodo):
        if len(nodo.ev) == 0 and len(nodo.ef)==0:
            ev = self.getLabel()
            ef = self.getLabel()
            nodo.ev.append(ev)
            nodo.ef.append(ef)
            tmpEtq = self.getTemp()
            nodo.expresion += str(tmpEtq) + " = "+str(nodo.referencia)+" ;\n"
            nodo.expresion += "if("+str(tmpEtq)+" == 1) {goto "+str(ev)+"}\n"
            nodo.expresion += "goto "+str(ef)+"\n"
            nodo.referencia = tmpEtq
    #endregion

    #region ifs
    def traducirIfs(self, nodoExpresion, nodoInstruccion, padre):
        if nodoExpresion != None: # Indica que viene un ELSE, ya que no hay nada que validar
            self.agregarIfEtiquetas(nodoExpresion) #Agrega las etiquetas correspondientes si no las tiene (true o false)
            padre.expresion += nodoExpresion.expresion
            for x in nodoExpresion.ev:
                padre.expresion += str(x) + ":\n"
            padre.expresion += nodoInstruccion.expresion
            evt = self.getLabel()
            padre.ev.append(evt)
            padre.expresion += "goto " + str(evt) + "\n"
            for x in nodoExpresion.ef:
                padre.expresion += str(x) + ":\n"
            padre.ef = []
        else:
            padre.expresion += nodoInstruccion.expresion
            # este código está en duda... ya que habría que probar funciones anidadas
            for x in padre.ef:
                padre.expresion += str(x) + ":\n"
            for x in padre.ev:
                padre.expresion += str(x) + ":\n"

    def agregarIfEtiquetas(self, nodo):
        #Los nodos que entren deben ser booleanos
        if nodo.tipo == DataType.bool:
            if len(nodo.ev) == 0 or len(nodo.ef) == 0:
                evt = self.getLabel()
                eft = self.getLabel()
                nodo.expresion += "if ( " + str(nodo.referencia) + " == 1){goto "+str(evt)+" }\n"
                nodo.expresion += "goto " + str(eft)+ "\n"
                nodo.ev.append(evt)
                nodo.ef.append(eft)
        else:
            print("Error, el tipo de dato no es booleano")
    #endregion

    #region while
    def traducirWhile(self, nodoExpresion, nodoInstruccion, padre):
        # Algoritmo
        # 1. Se coloca una etiqueta (el salto del while)
        # 2. Se coloca la expresión de validación de nodo Expresion
        # 3. Agrega las instrucciones dentro del while
        # 4. Agrega una etiqueta goto del paso
        if nodoExpresion.tipo == DataType.bool:
            etemp = self.getLabel()
            padre.expresion += str(etemp)+":\n"
            
            self.agregarIfEtiquetas(nodoExpresion)
            if (padre.isContinue):
                padre.expresion += str(padre.etContinue)+":\n"
            padre.expresion += nodoExpresion.expresion
            for x in nodoExpresion.ev:
                padre.expresion += str(x) + ":\n"
            padre.expresion +=  nodoInstruccion.expresion
            padre.expresion += "goto "+ str(etemp)+"\n"
            for x in nodoExpresion.ef:
                padre.expresion += str(x) + ":\n"    
    #endregion
    
    #region print
    def traducirPrint(self, listaExpresiones, padre, isPrintln):
        if listaExpresiones.tipo != DataType.error:
            for nodoExp in listaExpresiones.hijos:
                padre.expresion += nodoExp.expresion
                if nodoExp.tipo!= DataType.error:
                    if nodoExp.tipo != DataType.string:
                        if (nodoExp.tipo == DataType.int64):
                            padre.expresion +='''fmt.Printf(\"%g\",'''+str(nodoExp.referencia)+''');\n'''
                        elif (nodoExp.tipo == DataType.float64):
                            padre.expresion +='''fmt.Printf(\"%g\",'''+str(nodoExp.referencia)+''');\n'''
                        elif (nodoExp.tipo == DataType.bool):
                            padre.expresion +='''fmt.Printf(\"%g\",'''+str(nodoExp.referencia)+''');\n'''
                        
                    else:
                        tmpRef1 = self.getTemp()
                        tmpCont = self.getTemp()
                        tmpEtq = self.getLabel()
                        tmpEtqS = self.getLabel()
                        tmpChr = self.getTemp()
                        # nodoExpresion.referencia es la posición del HEAP de la cadena.

                        padre.expresion += str(tmpRef1) + " = "+ self.getArreglo() + "[int("+str(nodoExp.referencia)+")];\n" # Se obtiene el tamaño de la cadena 
                        padre.expresion += str(tmpCont) + " = 1;\n"
                        padre.expresion += str(tmpEtqS) + ":\n"
                        padre.expresion += "if("+str(tmpCont)+">"+str(tmpRef1)+") {goto "+str(tmpEtq)+"}\n"
                        padre.expresion += str(tmpCont) +" = " + str(tmpCont)+" + 1;\n"
                        padre.expresion += str(nodoExp.referencia) +" = " + str(nodoExp.referencia) +" + 1;\n"
                        padre.expresion += str(tmpChr) + " = " + self.getArreglo() + "[int("+str(nodoExp.referencia)+")];\n"
                        padre.expresion += "fmt.Printf(\"%c\",int("+str(tmpChr)+"));\n"
                        padre.expresion += "goto "+str(tmpEtqS)+"\n"
                        padre.expresion += str(tmpEtq)+ ":\n"
            self.agregarLibreria("fmt")
            if(isPrintln):
                padre.expresion += '''fmt.Printf("%s","\\n");\n'''
    #endregion
    
    #region Cadenas
    def traducirCadena(self, padre, symbolTable):
        # La cadena SIEMPRE se almacenará en el heap, tenga o no tenga que ocupar espacios de memoria.
        # Acá siempre llegan cadenas y se obtiene una referencia.
        tam = len(padre.valor)
        pos = symbolTable.getNextPosHeap()
        padre.expresion += self.getArreglo()+"[int("+self.getPointer()+")] = "+str(tam)+";\n"
        padre.referencia = self.getTemp()
        padre.expresion += str(padre.referencia)+" = "+self.getPointer()+";\n"
        padre.expresion += self.getPointer() + " = "+self.getPointer()+" + 1;\n"
        for x in padre.valor:
            # Se recorre la cadena elemento por elemento y se ingresa al heap.
            padre.expresion += self.getArreglo()+"[int("+self.getPointer()+")] = " + str(ord(x)) + ";\n"
            padre.expresion += self.getPointer() + " = "+self.getPointer()+" + 1;\n"
    #endregion

    #region Upper
    def traducirCase(self, padre, hijo, tablaSimbolos, isUpper):
        if(hijo.tipo == DataType.string):
            padre.tipo = DataType.string
            padre.expresion += hijo.expresion
            tamCad = self.getTemp()
            cont  = self.getTemp()
            etqSalida = self.getLabel()
            etqCiclo = self.getLabel()
            tmpPosLectura = self.getTemp()
            tmpCharLectura = self.getTemp()
            padre.expresion += str(tamCad) +" = " + self.getArreglo()+"[int("+str(hijo.referencia)+")];\n"


            padre.referencia = self.getTemp()
            padre.expresion += str(padre.referencia) + " = "+ self.getPointer()+";\n"
            padre.expresion += self.getArreglo() + "[int("+self.getPointer()+")] = " + str(tamCad) + ";\n"
            

            padre.expresion += str(cont) +" = 0;\n"
            padre.expresion += str(etqCiclo)+":\n"
            padre.expresion += self.getPointer() + " = " + self.getPointer()+" + 1;\n" 
            padre.expresion += "if(" + str(tamCad) + "<" + str(cont) + "){ goto "+etqSalida+"}\n"


            etqSalto = self.getLabel()
            padre.expresion += str(cont) +" = "+str(cont) +" + 1;\n"
            padre.expresion += str(tmpPosLectura) + " = " +str(hijo.referencia) + " + " + str(cont)+";\n"
            padre.expresion += str(tmpCharLectura) + " = " + self.getArreglo() + "[int("+str(tmpPosLectura)+")];\n"
            if (isUpper):
                padre.expresion += "if(" + str(tmpCharLectura) + "< 97 ){ goto "+str(etqSalto)+" }\n" #Agregar etiqueta
                padre.expresion += "if(" + str(tmpCharLectura) + "> 122 ){ goto "+str(etqSalto)+" }\n" #Agregar etiqueta
                padre.expresion += str(tmpCharLectura) + " = " +  str(tmpCharLectura) + " - 32;\n"
            else:
                padre.expresion += "if(" + str(tmpCharLectura) + "< 65 ){ goto "+str(etqSalto)+" }\n" #Agregar etiqueta
                padre.expresion += "if(" + str(tmpCharLectura) + "> 90 ){ goto "+str(etqSalto)+" }\n" #Agregar etiquet
                padre.expresion += str(tmpCharLectura) + " = " +  str(tmpCharLectura) + " + 32;\n"
            
            padre.expresion += str(etqSalto) + ":\n"
            #padre.expresion += "fmt.Println("+str(tmpCharLectura)+","+self.getPointer()+");\n"
            padre.expresion += self.getArreglo()+"[int("+self.getPointer()+")] = " + str(tmpCharLectura) + ";\n"
            padre.expresion += "//Finaliza upper\n"
            
            



            
            padre.expresion += "goto " + str(etqCiclo) + "\n"
            padre.expresion += str(etqSalida)+":\n"

        else:
            print("Error")
    #endregion

    #endregion