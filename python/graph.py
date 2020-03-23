from average import averageStrength
import plotly.graph_objects as go
from datetime import datetime

num = 30
timeList = []
master_addresses = []
master_strengths = []

while True:
	signalList = averageStrength(3)
	timeList.append(datetime.now())
	addresses = signalList["address"]
	strengths = signalList["strength"]
	for i in range(len(addresses)):
		if (addresses[i] not in master_addresses):
			master_addresses.append(addresses[i])
			master_strengths.append([int(strengths[i])])
		else:
			master_strengths[master_addresses.index(addresses[i])].append(int(strengths[i]))
	fig = go.Figure()
	for addr in master_addresses:
		fig.add_trace(go.Scatter(x=timeList, y=master_strengths[master_addresses.index(addr)], mode="lines", name=addr))

	refresh_interval = 7
	reload_script = 'window.onload=function() {window.setInterval(function() {window.location.reload(true)}, 1000 * ' + str(refresh_interval) + ')}'

	fig.write_html('graph.html', auto_open = False, post_script = reload_script)
