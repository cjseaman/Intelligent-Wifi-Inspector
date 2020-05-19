from flask import render_template
import signalLevel as sig
import os, math, time

distance_file = '.distance'
node1 = 'LeaPiNode1'
node2 = 'LeaPiNode2'
node3 = 'LeaPiNode3'

def signal_to_distance(signal):
    return pow(2, (-signal - 25 + 0.1)/36)


def calibrate1():
    signal_2_1 = 0.0
    signal_2_3 = 0.0
    

    signal_2_1 = (float(sig.getSignal(node1)['strength']) + float(sig.getSignal(node1)['strength'])) / 2
    print(signal_2_1)
    signal_2_3 = (float(sig.getSignal(node3)['strength']) + float(sig.getSignal(node3)['strength'])) / 2

    signal_2_1 = signal_to_distance(signal_2_1)
    signal_2_3 = signal_to_distance(signal_2_3)
    
    with open(".sig_2_1", "w") as f:
        f.write(str(signal_2_1))

    with open(".sig_2_3", "w") as f:
        f.write(str(signal_2_3))
    
    return signal_2_1,signal_2_3

        
def calibrate2():
    signal_1_3 = 0.0

    if os.path.exists(".sig_2_1"):
        with open(".sig_2_1", "r") as f:
           signal_2_1 = f.read()
        signal_2_1 = float(signal_2_1)

        with open(".sig_2_3", "r") as f:
            signal_2_3 = f.read()
        signal_2_3 = float(signal_2_3)
    else:
        print("Need to calibrate Node 2 First")
        return
    signal_1_3 = (float(sig.getSignal(node3)['strength']) + float(sig.getSignal(node3)['strength'])) / 2

    signal_1_3 = signal_to_distance(signal_1_3)
    
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

    
def calibrate():
    response = ''
    response = input("Place Diagnostic Tool at Node 2, then press enter...")
    
    signal_2_1 = 0.0
    signal_2_3 = 0.0
    signal_1_3 = 0.0

    signal_2_1 = (float(sig.getSignal(node1)['strength']) + float(sig.getSignal(node1)['strength'])) / 2
    print(signal_2_1)
    signal_2_3 = (float(sig.getSignal(node3)['strength']) + float(sig.getSignal(node3)['strength'])) / 2
    print(signal_2_3)

    response = input("Place Diagnostic Tool at Node 1, then press enter...")

    signal_1_3 = (float(sig.getSignal(node3)['strength']) + float(sig.getSignal(node3)['strength'])) / 2
    print(signal_1_3)

    signal_2_1 = signal_to_distance(signal_2_1)
    signal_2_3 = signal_to_distance(signal_2_3)
    signal_1_3 = signal_to_distance(signal_1_3)
    print("Distances 2-1, 2-3, 1-3:")
    print(signal_2_1, signal_2_3, signal_1_3)
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
    r1 = signal_to_distance(float(sig.getSignal(node1)["strength"]))
    r2 = signal_to_distance(float(sig.getSignal(node2)["strength"]))
    r3 = signal_to_distance(float(sig.getSignal(node3)["strength"]))

    x = (r1*r1 - r2*r2 + U*U)/(2*U)
    if (x < 0):
        x = 0
    y = (r1 * r1 - r3 * r3 + Vx * Vx + Vy * Vy - 2 * Vx * x) / (2 * Vy)
    return x,y,U

if __name__ == '__main__':
    x,y,U = triangulate()
    print(x)
    print(y)

