import signalLevel as sig
import os, math, time

distance_file = '.distance'
node1 = '0A:BD:55:EC:5E:C4'
node2 = 'D2:09:30:9D:F6:23'

class Error(Exception):
	pass

class MissingSignal(Error):
	def __init__(self, message):
		self.message = message

def calibrate(address=node1):
	response = ''

	response = raw_input("Place Diagnostic Tool at Node 2, then press enter to calibrate...")
        
        signal = 0.0;

        for i in range(1,10):
            time.sleep(0.5)
	    signal = float(sig.getSignal(address)['strength']) + signal

        signal = signal/10;
        print(signal)

	with open(distance_file, "w") as f:
		f.write(str(signal))

	return signal


def triangulate():
	if(os.path.exists(distance_file)):
            with open(distance_file, "r") as f:
                    U = 70 - float(f.read())
	else:
            U = 70 - float(calibrate())

	signals = sig.getAllSignals()

	if len(signals) < 2:
            raise MissingSignal("Node could not be found")
	for signal in signals:
            if(signal["address"]  == node2):
                r1 = 70 - float(signal["strength"])
            elif(signal["address"] == node1):
                r2 = 70 - float(signal["strength"])
            else:
                raise MissingSignal("One or both nodes could not be found")

	x = (r1*r1 - r2*r2 + U*U)/(2*U)
        if (x < 0):
            x = 0
	square = r1*r1 - x*x
	if(square >= 0):
            y = math.sqrt(square)
	else:
            y = math.sqrt(-square)
	return x,y

if __name__ == '__main__':
    x,y = triangulate()
    print(x)
    print(y)

