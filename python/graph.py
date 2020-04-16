from triangulate import triangulate, calibrate
import plotly.graph_objects as go
from datetime import datetime
import os, pickle, random

saved_graph = '.graphInfo'

def getPacketLoss():
	return random.randint(0,50)

def generate():

    print("Running...")
    
    graphInfo = {
                'x_vals': [],
                'y_vals': [],
                'z_vals': []
                }

    if os.path.exists(saved_graph):
        with open(saved_graph, 'rb') as f:
            graphInfo = pickle.load(f)

    while True:
            
            response = raw_input("(1) Press Enter to scan\n(2) Type \"calibrate\" to recalibrate distance\n(3) Type \"clear\" to clear previous scan results\n(4) Type \"quit\" to exit\n")
            if response == 'calibrate' or response == '2':
                calibrate()
                continue

            if response == 'clear' or response == '3':
                graphInfo = {
                        'x_vals': [],
                        'y_vals': [],
                        'z_vals': []
                        }
                print("Graph has been reset")
                continue
            
            if response == 'quit' or response == '4':
                return
            
            x,y = triangulate()

            if len(graphInfo['x_vals']) > 0:
                if (x > (2*(sum(graphInfo['x_vals'])/len(graphInfo['x_vals']))) or y > (2*(sum(graphInfo['y_vals'])/len(graphInfo['y_vals'])))):
                    print("Outlier detected")
                    continue

            z = getPacketLoss()
            graphInfo['x_vals'].append(x)
            graphInfo['y_vals'].append(y)
            graphInfo['z_vals'].append(z)
            print(graphInfo)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = graphInfo['x_vals'], y = graphInfo['y_vals'], mode="markers"))
            refresh_interval = 7
            reload_script = 'window.onload=function() {window.setInterval(function() {window.location.reload(true)}, 1000 * ' + str(refresh_interval) + ')}'
            fig.write_html('graph.html', auto_open = False, post_script = reload_script)
            
            with open(saved_graph, 'wb') as f:
                pickle.dump(graphInfo, f)

if __name__ == '__main__':
    generate()
