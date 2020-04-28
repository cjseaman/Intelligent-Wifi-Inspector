from triangulate import triangulate, calibrate
import plotly.graph_objects as go
from datetime import datetime
import os, pickle, random

saved_graph = '.graphInfo'
graph_location = '/var/www/html/index.html'

def getPacketLoss():
    pass

def generate():
    n_points = 0
    print("Running...")
    
    graphInfo = {
                'x_vals': [],
                'y_vals': [],
                'z_vals': [],
                }

    if os.path.exists(saved_graph):
        with open(saved_graph, 'rb') as f:
            graphInfo = pickle.load(f)

    while True:
            
        response = input("(1) Press Enter to scan\n(2) Type \"calibrate\" to recalibrate distance\n(3) Type \"clear\" to clear previous scan results\n(4) Type \"quit\" to exit\n")
        if response == 'calibrate' or response == '2':
            U = calibrate()[2]
            response = 'clear'

        if response == 'clear' or response == '3':
            graphInfo = {
                    'x_vals': [],
                    'y_vals': [],
                    'z_vals': []
                    }
            print("Graph has been reset")
            n_points = 0
            continue
        
        if response == 'quit' or response == '4':
            return
        
        x,y,U = triangulate()
        n_points = n_points + 1

        if len(graphInfo['x_vals']) > 0:
            if (x > (2*(sum(graphInfo['x_vals'])/len(graphInfo['x_vals']))) or y > (2*(sum(graphInfo['y_vals'])/len(graphInfo['y_vals'])))):
                print("Outlier detected")

        z = n_points
        
        if n_points <= 1: 
            graphInfo['x_vals'].append(0)
            graphInfo['y_vals'].append(0)
            graphInfo['z_vals'].append(0)
            
            graphInfo['x_vals'].append(U)
            graphInfo['y_vals'].append(0)
            graphInfo['z_vals'].append(0)
        
        graphInfo['x_vals'].append(x)
        graphInfo['y_vals'].append(y)
        graphInfo['z_vals'].append(z)
        print(graphInfo)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = graphInfo['x_vals'], y = graphInfo['y_vals'], mode="markers", marker = dict(color=graphInfo['z_vals'])))
        refresh_interval = 7
        reload_script = 'window.onload=function() {window.setInterval(function() {window.location.reload(true)}, 1000 * ' + str(refresh_interval) + ')}'
        fig.write_html(graph_location, auto_open = False)
        
        with open(saved_graph, 'wb') as f:
            pickle.dump(graphInfo, f)

if __name__ == '__main__':
    generate()
