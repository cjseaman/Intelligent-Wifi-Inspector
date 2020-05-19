import os
import subprocess

OOR = "Out of Range"
ips = ['192.168.4.2', '192.168.4.3', '192.168.4.4']
addresses = ['LeaPiNode1', 'LeaPiNode2', 'LeaPiNode3']
interface = 'wlan0'
surveyor_location = '../scripting/client/surveyor_c_lite.sh'

def getPacketLoss(bflag_value = 5, lflag_value = 1470):   
 
    bflag_value = str(bflag_value)
    lflag_value = str(lflag_value)
    runCommand = ['./' + surveyor_location]
    
    scan = subprocess.Popen(runCommand, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout,stderr = scan.communicate()
    value = stdout.decode()
    print(value)
    
    return float(value)
    

def getSignal(essid):
    scanCommand = ['sudo', 'iwlist', interface, 'scan']
    lines = [' ',' ',' ',' ']
    Signal = {
        'strength': 0,
        'address': essid
    }
    print("Scanning...")
    
    scan = subprocess.Popen(scanCommand,stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout,stderr = scan.communicate()
    
    lines = stdout.decode().split('\n')

    i = 0
    for line in lines:
        if(essid in line):
            Signal = {
                'strength': lines[i - 2].split('=')[2].split(' ')[0],
                'address': essid
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

