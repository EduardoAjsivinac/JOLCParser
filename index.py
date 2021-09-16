import http.client
import json
from flask import send_file
from flask import Response
from flask.helpers import url_for
from parser.gramatica import run_method
from parser.Entorno import *
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import sys
sys.setrecursionlimit(10000)

app = Flask(__name__)

global analizo
analizo = False
dotresult = ""
tabla_simbolos = []


@app.route('/')
def home():
    return render_template('html/home.html', project_name = "JOLC Parser")

@app.route('/workarea')
def workarea():
    archivo = open("Entradas/Funciones/recursivas.jl")
    entrada=""
    for linea in archivo:
        entrada+=str(linea)
    return render_template('html/workarea.html', project_name = "JOLC Parser", entrada=entrada)

@app.route('/parse', methods=['POST'])
def parser():
    global analizo
    global dotresult
    global tabla_simbolos
    analizo = True
    entrada = request.json['entrada']
    resultado = run_method(entrada)
    nuevoEntorno = Entorno("general", TipoEntorno.eglobal)
    resultado.execute(nuevoEntorno)
    dotresult = "digraph G {" + resultado.getdot()+ "}"
    #tabla_simbolos = nuevoEntorno.getTable().simbolos
    dataresult={
        "errores": nuevoEntorno.pilaErrores,
        "data": nuevoEntorno.consolaSalida
    }
    return dataresult

@app.route('/reports')
def reports():
    global analizo
    global dotresult
    global tabla_simbolos
    if (analizo):
        conn = http.client.HTTPSConnection("quickchart.io")
        print(dotresult)
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
        for x in tabla_simbolos:
            print(tabla_simbolos[x].value)
        return render_template('html/reports.html', project_name = "JOLC Parser", tabla_simbolos = tabla_simbolos)
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