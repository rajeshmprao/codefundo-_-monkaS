from flask import Flask, render_template
import sys

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('main.html')

@app.route('/helpme/')
def helpme():
    return render_template('helpme.html')

@app.route('/report/')
def report():
    return render_template('report.html')

@app.route('/locate/')
def locate():
    return render_template('locate.html')
    
if __name__ == "__main__":
    app.run()
