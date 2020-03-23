from signalLevel import getSignals

def averageStrength(num_items = 10):
	avgStrength = 0
	signalList = {
		"strength": [],
		"address": []
	}
	signals = getSignals()
	n = [0]*len(signals)
	i = 0
	while i < num_items:
		for signal in signals:
			if(signal["address"] in signalList["address"]):
				addr = signalList["address"].index(signal["address"])
				signalList["strength"][addr] = (int(signalList["strength"][addr]) * n[addr] + int(signal["strength"])) / (n[addr] + 1)
				n[addr] = n[addr] + 1
			else:
				signalList["address"].append(signal["address"])
				addr = signalList["address"].index(signal["address"])
				signalList["strength"].append(int(signal["strength"]))
				n[addr] = n[addr] + 1
		i = i + 1

	return signalList

if __name__ == '__main__':
	print('Average Strength:')
	print(averageStrength(3))
