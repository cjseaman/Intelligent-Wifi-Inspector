
import os
import subprocess

OOR = "Out of Range"
ips = ['192.168.4.2', '192.168.4.3']
addresses = ['LeaPiNode1', 'LeaPiNode2']
interface = 'wlan1'


def getSignal(address):
    scanCommand = ['sudo', 'iwlist', interface, 'scan']
    lines = [' ',' ',' ',' ']
    Signal = {
        'strength': 0,
        'address': address
    }
    print("Scanning...")
    
    scan = subprocess.Popen(scanCommand,stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout,stderr = scan.communicate()
    
    lines = stdout.decode().split('\n')

    i = 0
    for line in lines:
        if(address in line):
            Signal = {
                'strength': lines[i - 2].split('=')[1].split('/')[0],
                'address': address
            }
        i = i + 1

    return Signal

def getAllSignals():

    all_signals = []
    for add in addresses:
        signal = getSignal(add)
        all_signals.append(signal)
    return all_signals

if __name__ == '__main__':
    print(getAllSignals())
