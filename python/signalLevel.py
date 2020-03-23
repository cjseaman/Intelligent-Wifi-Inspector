
import os
import subprocess
def getSignals():
	scanCommand = ['sudo', 'iwlist', 'wlan1', 'scanning']

	scan = subprocess.Popen(scanCommand,
		stdout = subprocess.PIPE, stderr = subprocess.PIPE)

	stdout,stderr = scan.communicate()

	lines = stdout.split('\n')

	indexes = [i for i, j in enumerate(lines) if j.strip() == 'ESSID:"LeaPiNode"']

	signals = []

	for index in indexes:
		Signal = {
			'strength': lines[index - 2].split('=')[2].split(' ')[0],
			'address': lines[index - 5].split(': ')[1]
		}
		signals.append(Signal)

	return signals

if __name__ == '__main__':
	signals = getSignals()
	print('Beacon Strengths: ')
	for signal in signals:
		print(signal['address'])
		print(signal['strength'])
