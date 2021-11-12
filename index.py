import http.client
import json
from flask import send_file
from flask import Response
from flask.helpers import url_for
from parser.GrammarNodes.C3D.Etiquetas import C3DAux
from parser.gramatica import run_method
from parser.Entorno import *
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import sys
import os
sys.setrecursionlimit(10000)

app = Flask(__name__)

global analizo
global tabla_errores
analizo = False
dotresult = ""
tabla_simbolos = []

def crearC3D(entrada, tablaSimbolos):
    textoRetorno = '''package main
import ( '''
    for x in C3DAux().librerias:
        textoRetorno+="\"" + str(x) + "\"\n"
    textoRetorno +=''' )
var stack [10000000]float64
var heap [10000000]float64
var hp, sp float64
var '''
    for i in range(0,C3DAux().temp):
        textoRetorno += "t" + str(i)+ ", "
    textoRetorno += "t" + str(C3DAux().temp) + " float64;\n"
    return textoRetorno +"\n"+C3DAux().getTextoFunciones()+"\n" +entrada


@app.route('/')
def home():
    return render_template('html/home.html', project_name = "JOLC Parser")

@app.route('/workarea')
def workarea():
    global analizo
    analizo = False
    archivo = open("Entradas/prueba.jl")
    entrada=""
    for linea in archivo:
        entrada+=str(linea)
    return render_template('html/workarea.html', project_name = "JOLC Parser", entrada=entrada)

@app.route('/parse', methods=['POST'])
def parser():
    global analizo
    global dotresult
    global tabla_simbolos
    global tabla_errores
    
    entrada = request.json['entrada']
    resultado = run_method(entrada)
    # { raiz, errores }
    if len(resultado['errores']) == 0:
        analizo = True
        nuevoEntorno = Entorno("general", TipoEntorno.eglobal)
        resultado['raiz'].execute(nuevoEntorno)
        dotresult = "digraph G {" + resultado['raiz'].getdot()+ "}"
        nuevoEntorno.listaEntornosReporte['global'] = nuevoEntorno.diccionarioSimbolos['general']
        tabla_simbolos = nuevoEntorno.listaEntornosReporte
        tabla_errores = nuevoEntorno.pilaErrores 
        dataresult={
            "errores": nuevoEntorno.pilaErrores,
            "data": nuevoEntorno.consolaSalida
        }
        return dataresult
    dataresult={
        "errores": resultado['errores'],
        "data": ""
    }
    return dataresult

@app.route('/translate', methods=['POST'])
def translate():
    global analizo
    global dotresult
    global tabla_simbolos
    global tabla_errores
    C3DAux().librerias = {}
    C3DAux().listaTamEntornos = []
    entrada = request.json['entrada']
    resultado = run_method(entrada)
    # { raiz, errores }
    if len(resultado['errores']) == 0:
        C3DAux().label = 0
        C3DAux().temp = 0
        analizo = True
        tablaSimbolos = SymbolTable({"nombre": "Global", "numero" : 0})
        resultado['raiz'].createTable(tablaSimbolos)
        #tablaSimbolos.imprimir()
        #tablaSimbolos.setNextPosArray
        C3DAux().agregarATam(0)
        resultado['raiz'].expresion = "func main(){\n"
        resultado['raiz'].expresion += "sp = 0;\n"
        resultado['raiz'].expresion += "hp = "+str(tablaSimbolos.posicion)+";\n"
        C3DAux().expresionFunciones = ""
        C3DAux().getTemp() # T0 para los return
        C3DAux().getTemp() # T1 para los sp
        resultado['raiz'].getC3D(tablaSimbolos)
        resultado['raiz'].expresion += "}\n"
        consolaSalida = crearC3D(resultado['raiz'].expresion,tablaSimbolos)
        file = open("./Entradas/Salida.go", "w")
        file.write(consolaSalida)
        file.close()
        dotresult = "digraph G {" + resultado['raiz'].getdot()+ "}"
        dataresult={
            "errores": tablaSimbolos.erroresSalida,
            "data": consolaSalida
        }
        return dataresult
    dataresult={
        "errores": resultado['errores'],
        "data": ""
    }
    return dataresult

@app.route('/reports')
def reports():
    global analizo
    global dotresult
    global tabla_simbolos
    global tabla_errores
    if (analizo):
        conn = http.client.HTTPSConnection("quickchart.io")
        payload = json.dumps({
            "graph": dotresult,
            "layout": "dot",
            "format": "svg"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/graphviz", payload, headers)
        res = conn.getresponse()
        data = res.read()
        f = open("static/images/tree.svg","w")
        f.write(data.decode("utf-8"))
        f.close()
        # return render_template('html/reports.html', project_name = "JOLC Parser", tabla_simbolos = tabla_simbolos, tabla_errores = tabla_errores)
        return render_template('html/reports.html', project_name = "JOLC Parser")
    return redirect(url_for('workarea'))

@app.route("/getSVGImage")
def getPlotCSV():
    f = open("static/images/tree.svg")
    result = f.read()
    f.close()
    csv = result.encode('utf-8')
    return Response(
        csv,
        mimetype="image/svg+xml",
        headers={"Content-disposition":
                 "attachment; filename=tree.svg"})

if __name__ == '__main__':
    app.run(debug=True)