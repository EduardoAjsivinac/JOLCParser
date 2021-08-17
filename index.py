from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('html/home.html', project_name = "JOLC Parser")

@app.route('/parser')
def parser():
    return render_template('html/parser.html', project_name = "JOLC Parser")

@app.route('/reports')
def reports():
    return render_template('html/reports.html', project_name = "JOLC Parser")


if __name__ == '__main__':
    app.run(debug=True)