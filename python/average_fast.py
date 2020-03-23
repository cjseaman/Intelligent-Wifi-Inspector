from signalLevel import beaconStrength
from time import sleep

avgStrength = 0
strList = []
i = 0
while True:
	strList.append(beaconStrength())
	avgStrength = sum(strList)/len(strList)
	print(avgStrength)


