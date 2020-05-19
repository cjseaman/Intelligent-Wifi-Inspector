from flask import Flask
from flask import render_template
from graph import generate
from triangulate import calibrate1, calibrate2
from flask_bootstrap import Bootstrap
import os
app = Flask(__name__)
app.config.update (
    TEMPLATES_AUTO_RELOAD = True,
    EXPLAIN_TEMPLATE_LOADING = True
)

signal_2_1 = 0.0
signal_2_3 = 0.0
signal_1_3 = 0.0

#heatmap page w scan, clear, calibrate
@app.route('/')
def hello_world():
    if os.path.exists(".distance"):
        return render_template('wrapper.html', result='Previous calibration found, ready to scan.\nTo recalibrate please calibrate Node 2 and then Node 1')
    return render_template('wrapper.html', result='Welcome. Please Calibrate Node 2 and then Node 1')

@app.route('/clear')
def clear():
    generate('clear')
    return render_template('wrapper.html', result="Graph has been cleared.")

@app.route('/calibrateNode2')
def calibrateNode2():
    signal_2_1,signal_2_3 = calibrate1()
    return render_template('wrapper.html', result="Calibrated Node 2. Please calibrate Node 1.")

@app.route('/calibrateNode1')
def calibrateNode1():
    calibrate2()
    return render_template('wrapper.html', result="Calibration complete. Ready to scan.")

@app.route('/scan')
def scan():
    generate('scan')
    return render_template('wrapper.html', result="Scan complete. Press scan again to add another point or clear to remove all points.")
