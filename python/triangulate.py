import signalLevel as sig
import os, math, time

distance_file = '.distance'
node1 = 'LeaPiNode1'
node2 = 'LeaPiNode2'
node3 = 'LeaPiNode3'

class Error(Exception):
    pass

class MissingSignal(Error):
    def __init__(self, message):
        self.message = message

def calibrate():
    response = ''

    response = input("Place Diagnostic Tool at Node 2, then press enter...")
    
    signal_2_1 = 0.0
    signal_2_3 = 0.0
    signal_1_3 = 0.0

    time.sleep(5)

    signal_2_1 = float(sig.getSignal(node1)['strength'])
    print(signal_2_1)
    signal_2_3 = float(sig.getSignal(node3)['strength'])  
    print(signal_2_3)

    response = input("Place Diagnostic Tool at Node 1, then press enter...")

    time.sleep(5)

    signal_1_3 = float(sig.getSignal(node3)['strength']) + signal_1_3
    print(signal_1_3)

    signal_2_1 = 70 - signal_2_1 + 1
    signal_2_3 = 70 - signal_2_3 + 1
    signal_1_3 = 70 - signal_1_3 + 1

    cos_1 = (signal_1_3 * signal_1_3 + signal_2_1 * signal_2_1 - signal_2_3 * signal_2_3) / (2 * signal_1_3 * signal_2_1)
    
    if cos_1 > 1 or cos_1 < -1:
        print('Calculated values do not form triangle, try again')
        return
     
    node_3_x = signal_2_3 * cos_1
    print(cos_1)
    node_3_y = signal_2_3 * math.sin(math.acos(cos_1))
    
    distance_info = (node_3_x,node_3_y,signal_2_1) 

    with open(distance_file, "w") as f:
        f.write(str(distance_info))

    return distance_info


def triangulate():
    if(os.path.exists(distance_file)):
        with open(distance_file, "r") as f:
            distances = f.read()
        V = distances.replace('(', '').replace(')', '').replace(' ', '').split(',')
        Vx = float(V[0])
        Vy = float(V[1])
        U = float(V[2])
    else:
            V = calibrate()
            Vx = V[0]
            Vy = V[1]
            U = V[2]

    print(Vx, Vy, U)
    r1 = 70 - float(sig.getSignal(node2)["strength"])
    r2 = 70 - float(sig.getSignal(node1)["strength"])
    r3 = 70 - float(sig.getSignal(node3)["strength"])

    x = (r1*r1 - r2*r2 + U*U)/(2*U)
    if (x < 0):
        x = 0
    y = (r1 * r1 - r3 * r3 + Vx * Vx + Vy * Vy - 2 * Vx * x) / (2 * Vy)
    return x,y,U

if __name__ == '__main__':
    x,y = triangulate()
    print(x)
    print(y)

