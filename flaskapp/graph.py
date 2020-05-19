from triangulate import triangulate, calibrate
from signalLevel import getPacketLoss
import plotly.graph_objects as go
from datetime import datetime
import os, pickle, random

saved_graph = '.graphInfo'
graph_location = './templates/index.html'

def generate(response):
    U = 0
    graphInfo = {
                'x_vals': [],
                'y_vals': [],
                'z_vals': []
                }

    if os.path.exists(saved_graph):
        with open(saved_graph, 'rb') as f:
            graphInfo = pickle.load(f)
        
    # response = input("(1) Press Enter to scan\n(2) Type \"calibrate\" to recalibrate distance\n(3) Type \"clear\" to clear previous scan results\n(4) Type \"quit\" to exit\n")
    if response == 'calibrate' or response == '2':
        U = calibrate()[2]
        response = 'clear'

    if response == 'clear' or response == '3':
        graphInfo = {
                'x_vals': [],
                'y_vals': [],
                'z_vals': []
                }
        print("Graph being reset...")
    
    if response == 'quit' or response == '4':
        return

    if response is not 'clear' and response is not '3':
        x,y,U = triangulate()

    if response is not 'clear' and response is not '3':
        z = getPacketLoss()
    
    if len(graphInfo['x_vals']) == 0: 
        graphInfo['x_vals'].append(0)
        graphInfo['y_vals'].append(0)
        graphInfo['z_vals'].append(0)
    elif len(graphInfo['x_vals']) == 1:    
        graphInfo['x_vals'].append(U)
        graphInfo['y_vals'].append(0)
        graphInfo['z_vals'].append(0)
    
    if response is not 'clear' and response is not '3':
        graphInfo['x_vals'].append(x)
        graphInfo['y_vals'].append(y)
        graphInfo['z_vals'].append(z)
    print(graphInfo)
    
    size_of_markers = 12
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = graphInfo['x_vals'], y = graphInfo['y_vals'], mode="markers", marker = dict(color=graphInfo['z_vals'], size=size_of_markers)))
    refresh_interval = 7
    reload_script = 'window.onload=function() {window.setInterval(function() {window.location.reload(true)}, 1000 * ' + str(refresh_interval) + ')}'
    fig.write_html(graph_location, auto_open = False)
    
    with open(saved_graph, 'wb') as f:
        pickle.dump(graphInfo, f)

if __name__ == '__main__':
    while(1):
        response = input("(1) Press Enter to scan\n(2) Type \"calibrate\" to recalibrate distance\n(3) Type \"clear\" to clear previous scan results\n(4) Type \"quit\" to exit\n")
        generate(response)
        if response == '4':
            break

