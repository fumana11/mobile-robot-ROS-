#!/usr/bin/env python
import rospy
import numpy as np
import math
import time
from collections import deque
from robot_controller.msg import GoalPosition
from std_msgs.msg import String

start_node = "C4"
goal_node = "B2"


ROBOT = np.array([0,0,0,0,0,0,0,0])
GOAL = np.array([0,0,0,0,0,0,0])
NILAI = np.array([0,0])
FINISH = np.array([0,0])
# Contoh penggunaan
graph = {
    'A1': ['A2', 'B1'],
    'A2': ['A1', 'A3','B2'],
    'A3': ['A2','A4','B3'],
    'A4': ['A3','A5','B4'],
    'A5': ['A4','B5'],
    'B1': ['A1','B2','C1'],
    'B2': ['A2','B1','B3','C2'],
    'B3': ['A3','B2','B4','C3'],
    'B4': ['A4','B3','B5','C4'],
    'B5': ['A5','B4','C5'],
    'C1': ['C2','B1','D1'],
    'C2': ['C1','B2','C3','D2'],
    'C3': ['C2','B3','C4','D3'],
    'C4': ['C3','B4','C5','D4'],
    'C5': ['C4','B5','D5',],
    'D1': ['D2','C1','E1'],
    'D2': ['D1','C2','D3','E2'],
    'D3': ['D2','C3','D4','E3'],
    'D4': ['D3','C4','D5','E4'],
    'D5': ['D4','C5','E5'],
    'E1' : ['D1','E2','F1'],
    'E2' : ['D2','E1','E3','F2'],
    'E3' : ['D3','E2','E4','F3'],
    'E4' : ['D4','E3','E5','F4'],
    'E5' : ['D5','E4','F5'],
    'F1' : ['E1','F2','G1'],
    'F2' : ['E2','F1','F3','G2'],
    'F3' : ['E3','F2','F4','G3'],
    'F4' : ['E4','F3','F5','G4'],
    'F5' : ['E5','F4','G5'],
    'G1' : ['F1','G2','H1'],
    'G2' : ['F2','G1','G3','H2'],
    'G3' : ['F3','G2','G4','H3'],
    'G4' : ['F4','G3','G5','H4'],
    'G5' : ['F5','G4','H5'],
    'H1' : ['G1','H2','I1'],
    'H2' : ['G2','H1','H3','I2'],
    'H3' : ['G3','H2','H4','I3'],
    'H4' : ['G4','H3','H5','I4'],
    'H5' : ['G5','H4','I5'],
    'I1' : ['H1','I2','J1'],
    'I2' : ['H2','I1','I3','J2'],
    'I3' : ['H3','I2','I4','J3'],
    'I4' : ['H4','I3','I5','J4'],
    'I5' : ['H5','I4','J5'],
    'J1' : ['I1','J2'],
    'J2' : ['I2','J1','J3'],
    'J3' : ['I3','J2','J4'],
    'J4' : ['I4','J3','J5'],
    'J5' : ['I5','J4']
    
}



#inisialisasi node
NODE_A = np.array([5,90,     5,160,     5,230,     5,298,     5,365])
NODE_B = np.array([68,90,    68,160,    68,230,    68,298,    68,365])
NODE_C = np.array([138,90,    138,160,    138,230,    138,298,    138,365])
NODE_D = np.array([207,90,    207,160,    207,230,    207,298,    207,365])
NODE_E = np.array([276,90,    276,160,    276,230,    276,298,    276,365])
NODE_F = np.array([345,90,    345,160,    345,230,    345,298,    345,365])
NODE_G = np.array([415,90,    415,160,    415,230,    415,298,    415,365])
NODE_H = np.array([485,90,    485,160,    485,230,    485,298,    485,365])
NODE_I = np.array([555,90,    555,160,    555,230,    555,298,    555,365])
NODE_J = np.array([625,90,    625,160,    625,230,    625,298,    625,365])

def bfs(graph, start, goal):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        vertex, path = queue.popleft()
        if vertex == goal:
            return path
        if vertex not in visited:
            visited.add(vertex)
            neighbors = graph[vertex]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    return "Tidak ditemukan jalur"
    
def callback(msg):
    global b
    
    c = len(result_path) -1
    node (b)
    
    ROBOT[0] = msg.x_robot  #x robot belakang
    ROBOT[1] = msg.y_robot  # y robot belakang
    ROBOT[2] = msg.x_depan  # x robot depan
    ROBOT[3] = msg.y_depan  # y robot depan
     
     # Mencari titik tengah robot
    ROBOT[4] = (ROBOT[2] + ROBOT[0])/2 #titik tengah x1 x2
    ROBOT[5] = (ROBOT[3] + ROBOT[1])/2 #titik tengah y1 y2
    Y = ROBOT[1]-ROBOT[3]   #Y2-Y1
    X = ROBOT[0]-ROBOT[2]   #X2-X1
    GOAL[0] = FINISH [0]
    GOAL[1] = FINISH [1]
   # derajad hadap robot
    GOAL[2] = ROBOT[4] - GOAL [0]
    GOAL[3] = ROBOT[5] - GOAL [1]
    
    #derajad set poin robot terhadap tujuan
    GOAL[4] = math.degrees(math.atan2(GOAL[3],GOAL[2]))
 
    # Derajat hadap robot - Derajat setpoint terhadap robot
    ROBOT[6] = math.degrees(math.atan2(Y,X))
    GOAL[5] = ROBOT[6]-GOAL[4]
       
       
    GOAL[6] = math.sqrt((GOAL[2]*GOAL[2] + GOAL[3]*GOAL[3])) #jarak
    #print('goal : ', GOAL[5] ,' d robot : ',ROBOT[6], ' d tujuan : ',GOAL[4],'jarak : ',GOAL[6])
        
    #print(FINISH[0])
    
    
    if GOAL[6] >30 :
          #belok kiri
           if(GOAL[5]>-338 and GOAL[5]<-180):
               pub.publish("1")
               print("Kiri jarak : ", GOAL[6])
           elif(GOAL[5]<=130 and GOAL[5]>=21):
               pub.publish("1")
               print("Kiri jarak : ", GOAL[6])
          #Belok kanan
           elif GOAL[5]>-180 and GOAL[5]<-10:
               pub.publish("3")
               print("kanan jarak : ", GOAL[6])
           elif GOAL[5]>130 and GOAL[5]<350:
               pub.publish("3")
               print("kanan jarak : ", GOAL[6])
          #Maju
           elif(GOAL[5]<0 and GOAL[5]>=-10):
               pub.publish("w")
               print("maju jarak : ", GOAL[6])
           elif(GOAL[5]<=360 and GOAL[5]>350):
               pub.publish("w")
           elif(GOAL[5]<=-338 and GOAL[5]>-359):
               pub.publish("w")
               print("maju jarak : ", GOAL[6])
           elif(GOAL[5]<=20 and GOAL[5]>=0):
               pub.publish("w")
               print("maju jarak : ", GOAL[6])
    else :
           if c > b :
             b +=1
           else:
             b=b
             pub.publish("4")
             print("berhenti jarak : ", GOAL[6])    


def node(a):
     
    A=result_path[a]
    
    if A == 'A1':
        FINISH[0] = NODE_A[0]
        FINISH[1] = NODE_A[1]
    if A == 'A2':
        FINISH[0] = NODE_A[2]
        FINISH[1] = NODE_A[3]
    if A == 'A3':
        FINISH[0] = NODE_A[4]
        FINISH[1] = NODE_A[5]
    if A == 'A4':
        FINISH[0] = NODE_A[6]
        FINISH[1] = NODE_A[7]
    if A == 'A5':
        FINISH[0] = NODE_A[8]
        FINISH[1] = NODE_A[9]
    if A == 'B1':
        FINISH[0] = NODE_B[0]
        FINISH[1] = NODE_B[1]
    if A == 'B2':
        FINISH[0] = NODE_B[2]
        FINISH[1] = NODE_B[3]
    if A == 'B3':
        FINISH[0] = NODE_B[4]
        FINISH[1] = NODE_B[5]
    if A == 'B4':
        FINISH[0] = NODE_B[6]
        FINISH[1] = NODE_B[7]
    if A == 'B5':
        FINISH[0] = NODE_B[8]
        FINISH[1] = NODE_B[9]
    if A == 'C1':
        FINISH[0] = NODE_C[0]
        FINISH[1] = NODE_C[1]
    if A == 'C2':
        FINISH[0] = NODE_C[2]
        FINISH[1] = NODE_C[3]
    if A == 'C3':
        FINISH[0] = NODE_C[4]
        FINISH[1] = NODE_C[5]
    if A == 'C4':
        FINISH[0] = NODE_C[6]
        FINISH[1] = NODE_C[7]
    if A == 'C5':
        FINISH[0] = NODE_C[8]
        FINISH[1] = NODE_C[9]
    if A == 'D1':
        FINISH[0] = NODE_D[0]
        FINISH[1] = NODE_D[1]
    if A == 'D2':
        FINISH[0] = NODE_D[2]
        FINISH[1] = NODE_D[3]
    if A == 'D3':
        FINISH[0] = NODE_D[4]
        FINISH[1] = NODE_D[5]
    if A == 'D4':
        FINISH[0] = NODE_D[6]
        FINISH[1] = NODE_D[7]
    if A == 'D5':
        FINISH[0] = NODE_D[8]
        FINISH[1] = NODE_D[9]
    if A == 'E1':
        FINISH[0] = NODE_E[0]
        FINISH[1] = NODE_E[1]
    if A == 'E2':
        FINISH[0] = NODE_E[2]
        FINISH[1] = NODE_E[3]
    if A == 'E3':
        FINISH[0] = NODE_E[4]
        FINISH[1] = NODE_E[5]
    if A == 'E4':
        FINISH[0] = NODE_E[6]
        FINISH[1] = NODE_E[7]
    if A == 'E5':
        FINISH[0] = NODE_E[8]
        FINISH[1] = NODE_E[9]
    if A == 'F1':
        FINISH[0] = NODE_F[0]
        FINISH[1] = NODE_F[1]
    if A == 'F2':
        FINISH[0] = NODE_F[2]
        FINISH[1] = NODE_F[3]
    if A == 'F3':
        FINISH[0] = NODE_F[4]
        FINISH[1] = NODE_F[5]
    if A == 'F4':
        FINISH[0] = NODE_F[6]
        FINISH[1] = NODE_F[7]
    if A == 'F5':
        FINISH[0] = NODE_F[8]
        FINISH[1] = NODE_F[9]
    if A == 'G1':
        FINISH[0] = NODE_G[0]
        FINISH[1] = NODE_G[1]
    if A == 'G2':
        FINISH[0] = NODE_G[2]
        FINISH[1] = NODE_G[3]
    if A == 'G3':
        FINISH[0] = NODE_G[4]
        FINISH[1] = NODE_G[5]
    if A == 'G4':
        FINISH[0] = NODE_G[6]
        FINISH[1] = NODE_G[7]
    if A == 'G5':
        FINISH[0] = NODE_G[8]
        FINISH[1] = NODE_G[9]
    if A == 'H1':
        FINISH[0] = NODE_H[0]
        FINISH[1] = NODE_H[1]
    if A == 'H2':
        FINISH[0] = NODE_H[2]
        FINISH[1] = NODE_H[3]
    if A == 'H3':
        FINISH[0] = NODE_H[4]
        FINISH[1] = NODE_H[5]
    if A == 'H4':
        FINISH[0] = NODE_H[6]
        FINISH[1] = NODE_H[7]
    if A == 'H5':
        FINISH[0] = NODE_H[8]
        FINISH[1] = NODE_H[9]
    if A == 'I1':
        FINISH[0] = NODE_I[0]
        FINISH[1] = NODE_I[1]
    if A == 'I2':
        FINISH[0] = NODE_I[2]
        FINISH[1] = NODE_I[3]
    if A == 'I3':
        FINISH[0] = NODE_I[4]
        FINISH[1] = NODE_I[5]
    if A == 'I4':
        FINISH[0] = NODE_I[6]
        FINISH[1] = NODE_I[7]
    if A == 'I5':
        FINISH[0] = NODE_I[8]
        FINISH[1] = NODE_I[9]
    if A == 'J1':
        FINISH[0] = NODE_J[0]
        FINISH[1] = NODE_J[1]
    if A == 'J2':
        FINISH[0] = NODE_J[2]
        FINISH[1] = NODE_J[3]
    if A == 'J3':
    
        FINISH[0] = NODE_J[4]
        FINISH[1] = NODE_J[5]
    if A == 'J4':
        FINISH[0] = NODE_J[6]
        FINISH[1] = NODE_J[7]
    if A == 'J5':
        FINISH[0] = NODE_J[8]
        FINISH[1] = NODE_J[9]
    print('tujuan ke node : ',A)
    #print(A, '= ','x', FINISH[0], '||', 'y', FINISH[1])
    #time.sleep(2)     

    
    #time.sleep(2)
    
     

    #print('goal : ', GOAL[5] ,' d robot : ',ROBOT[6], ' d tujuan : ',GOAL[4],'jarak : ',GOAL[6])



if __name__ == '__main__':
        rospy.init_node('pergerakan_robot', anonymous=True)
        pub = rospy.Publisher('controllerPub', String, queue_size=10)
        result_path = bfs(graph, start_node, goal_node)
        b = 0
       
           
        

        rospy.Subscriber('Goal_Position',GoalPosition, callback)
        rospy.spin()
    
