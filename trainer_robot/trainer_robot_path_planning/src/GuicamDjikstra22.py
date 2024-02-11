### Djikstra
# import pyqt5
from lib2to3.pytree import convert
from multiprocessing.resource_sharer import stop
from PyQt5 import QtGui,QtWidgets,QtCore    
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from psutil import STATUS_DEAD
#from Djikstra import arr

# import file desain
from Yoyoyo import Ui_Form
import pyrebase
import time
import numpy as np
import cv2
import math
import time
import numpy as np

config = {
  "authDomain": "rbtk-699.firebaseapp.com",
  "apiKey": "AIzaSyAXKBZL9kLcM5PkKCF-hmOpY-U4q7EcX6c",
  "databaseURL": "https://rbtk-699-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "rbtk-699.appspot.com"}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
 
CAMERA_NUMBER = 0
STATUS_FRAME = 0 #0 RAW, 1 HSV, 2 DEPAN, 3 BELAKANG, 4 LAPANGAN, 5 BITWISE
RD_LO = np.array([69,47,235])
RD_HI = np.array([255,255,255])
RB_LO = np.array([133,187,0])
RB_HI = np.array([255,255,255])
L_LO = np.array([39,65,47])
L_HI = np.array([255,255,255])
B_LO = np.array([68,0,241])
B_HI = np.array([222,255,255])

CAP = None

ROBOT = np.array([0,0,0,0,0,0,0]) #xdepan ydepan xblkg yblkg xtotal ytotal
GOL = np.array([0,0,0,0,0,0,0,0,0]) #sudut goll
LAP = np.array([0,0])
BOX = np.array([0,0])
FINISH = np.array([0,0])
STA = np.array([0,0])

#inisialisasi node
NODE_A = np.array([60,90,     60,180,     60,270,     60,360,     60,450])
NODE_B = np.array([120,90,    120,180,    120,270,    120,360,    120,450])
NODE_C = np.array([180,90,    180,180,    180,270,    180,360,    180,450])
NODE_D = np.array([240,90,    240,180,    240,270,    240,360,    240,450])
NODE_E = np.array([300,90,    300,180,    300,270,    300,360,    300,450])
NODE_F = np.array([360,90,    360,180,    360,270,    360,360,    360,450])
NODE_G = np.array([420,90,    420,180,    420,270,    420,360,    420,450])
NODE_H = np.array([480,90,    480,180,    480,270,    480,360,    480,450])
NODE_I = np.array([540,90,    540,180,    540,270,    540,360,    540,450])
NODE_J = np.array([600,90,    600,180,    600,270,    600,360,    600,450])

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def run(self):
        global CAP
        global start
        global goal

        # capture from web cam
        
        while True:
            ret, frame = CAP.read()
            if ret:
                # Proses Masking Robot depan, belakang, lapangan
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                masking_robotdepan = cv2.inRange(hsv,RD_LO,RD_HI)
                try:
                    M = cv2.moments(masking_robotdepan)
                    ROBOT[0] = int(M["m10"] / M["m00"])
                    ROBOT[1] = int(M["m01"] / M["m00"])
                except:
                    pass

                masking_robotbelakang = cv2.inRange(hsv,RB_LO,RB_HI)
                try:
                    M = cv2.moments(masking_robotbelakang)
                    ROBOT[2] = int(M["m10"] / M["m00"])
                    ROBOT[3] = int(M["m01"] / M["m00"])
                except:
                    pass

                masking_lapangan = cv2.inRange(hsv,L_LO,L_HI)
                try:
                    M = cv2.moments(masking_robotdepan)
                    LAP[0] = int(M["m10"] / M["m00"])
                    LAP[1] = int(M["m01"] / M["m00"])
                except:
                    pass

                masking_box = cv2.inRange(hsv,B_LO,B_HI)
                try:
                    M = cv2.moments(masking_box)
                    BOX[0] = int(M["m10"] / M["m00"])
                    BOX[1] = int(M["m01"] / M["m00"])
                except:
                    pass
                
                # Mencari titik tengah robot
                ROBOT[4] = (ROBOT[0] + ROBOT[2])/2 #titik tengah x1 x2
                ROBOT[5] = (ROBOT[1] + ROBOT[3])/2 #titik tengah y1 y2
                Y = ROBOT[3]-ROBOT[1]   #Y2-Y1
                X = ROBOT[2]-ROBOT[0]   #X2-X1

                # Derajat Hadap Robot
                GOL[5] = ROBOT[5] - FINISH[0]  # titik tengahY - Ygoal
                GOL[6] = ROBOT[4] - FINISH[1]  # titik tengahX - Xgoal
                
                #Derajat setpoint terhadap robot 
                GOL[3] = math.degrees(math.atan2(GOL[5],GOL[6]))
                
                # Derajat hadap robot - Derajat setpoint terhadap robot
                ROBOT[6] = math.degrees(math.atan2(Y,X))
                GOL[4] = ROBOT[6]-GOL[3]    
                    
                #Perhitungan jarak robot terhadap goal
                GOL[7] = math.sqrt((GOL[6]*GOL[6])+(GOL[5]*GOL[5]))

                # Menampilkan titik koordinat pada UI
                bitwise = frame
                # Robot
                cv2.circle(bitwise, (ROBOT[0], ROBOT[1]), 5, (255, 0, 0), -1)
                cv2.circle(bitwise, (ROBOT[2], ROBOT[3]), 5, (0, 0, 255), -1)
                cv2.circle(bitwise, (ROBOT[4], ROBOT[5]), 5, (255, 0, 255), -1)
                
                # Finish
                cv2.circle(bitwise, (GOL[0], GOL[1]), 10, (0, 255, 0), -1)
                # Box
                cv2.circle(bitwise, (BOX[0], BOX[1]), 10, (0, 0, 0), -1)

                # Mapping
                cv2.circle(bitwise, (NODE_A[0], NODE_A[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_A[2], NODE_A[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_A[4], NODE_A[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_A[6], NODE_A[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_A[8], NODE_A[9]), 10, (0, 0, 255), -1)

                cv2.circle(bitwise, (NODE_B[0], NODE_B[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_B[2], NODE_B[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_B[4], NODE_B[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_B[6], NODE_B[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_B[8], NODE_B[9]), 10, (0, 0, 255), -1)

                cv2.circle(bitwise, (NODE_C[0], NODE_C[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_C[2], NODE_C[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_C[4], NODE_C[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_C[6], NODE_C[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_C[8], NODE_C[9]), 10, (0, 0, 255), -1)

                cv2.circle(bitwise, (NODE_D[0], NODE_D[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_D[2], NODE_D[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_D[4], NODE_D[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_D[6], NODE_D[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_D[8], NODE_D[9]), 10, (0, 0, 255), -1)

                cv2.circle(bitwise, (NODE_E[0], NODE_E[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_E[2], NODE_E[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_E[4], NODE_E[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_E[6], NODE_E[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_E[8], NODE_E[9]), 10, (0, 0, 255), -1)

                cv2.circle(bitwise, (NODE_F[0], NODE_F[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_F[2], NODE_F[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_F[4], NODE_F[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_F[6], NODE_F[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_F[8], NODE_F[9]), 10, (0, 0, 255), -1)

                cv2.circle(bitwise, (NODE_G[0], NODE_G[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_G[2], NODE_G[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_G[4], NODE_G[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_G[6], NODE_G[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_G[8], NODE_G[9]), 10, (0, 0, 255), -1)

                cv2.circle(bitwise, (NODE_H[0], NODE_H[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_H[2], NODE_H[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_H[4], NODE_H[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_H[6], NODE_H[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_H[8], NODE_H[9]), 10, (0, 0, 255), -1)

                cv2.circle(bitwise, (NODE_I[0], NODE_I[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_I[2], NODE_I[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_I[4], NODE_I[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_I[6], NODE_I[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_I[8], NODE_I[9]), 10, (0, 0, 255), -1)

                cv2.circle(bitwise, (NODE_J[0], NODE_J[1]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_J[2], NODE_J[3]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_J[4], NODE_J[5]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_J[6], NODE_J[7]), 10, (0, 0, 255), -1)
                cv2.circle(bitwise, (NODE_J[8], NODE_J[9]), 10, (0, 0, 255), -1)

                if STATUS_FRAME == 0:
                    self.change_pixmap_signal.emit(frame)
                elif STATUS_FRAME == 1:
                    self.change_pixmap_signal.emit(hsv)
                elif STATUS_FRAME == 2:
                    self.change_pixmap_signal.emit(masking_robotdepan)
                elif STATUS_FRAME == 3:
                    self.change_pixmap_signal.emit(masking_robotbelakang)
                elif STATUS_FRAME == 4:
                    self.change_pixmap_signal.emit(masking_lapangan)
                elif STATUS_FRAME == 5:
                    self.change_pixmap_signal.emit(bitwise)
                elif STATUS_FRAME == 6:
                    self.change_pixmap_signal.emit(masking_box)
                
                # Proser pergerakan djikstra

                # diameter 
                
                #startx = ROBOT[0]
                #starty = ROBOT[1]

                #NJAJAL
                startx = STA[0]
                starty = STA[1]

                # proses start
                NODES = [['A1',  NODE_A[0], NODE_A[1]],
                        ['A2',  NODE_A[2], NODE_A[3]],
                        ['A3',  NODE_A[4], NODE_A[5]],
                        ['A4',  NODE_A[6], NODE_A[7]],
                        ['A5',  NODE_A[8], NODE_A[9]],
                        ['B1',  NODE_B[0], NODE_B[1]],
                        ['B2',  NODE_B[2], NODE_B[3]],
                        ['B3',  NODE_B[4], NODE_B[5]],
                        ['B4',  NODE_B[6], NODE_B[7]],
                        ['B5',  NODE_B[8], NODE_B[9]],
                        ['C1',  NODE_C[0], NODE_C[1]],
                        ['C2',  NODE_C[2], NODE_C[3]],
                        ['C3',  NODE_C[4], NODE_C[5]],
                        ['C4',  NODE_C[6], NODE_C[7]],
                        ['C5',  NODE_C[8], NODE_C[9]],
                        ['D1',  NODE_D[0], NODE_D[1]],
                        ['D2',  NODE_D[2], NODE_D[3]],
                        ['D3',  NODE_D[4], NODE_D[5]],
                        ['D4',  NODE_D[6], NODE_D[7]],
                        ['D5',  NODE_D[8], NODE_D[9]],
                        ['E1',  NODE_E[0], NODE_E[1]],
                        ['E2',  NODE_E[2], NODE_E[3]],
                        ['E3',  NODE_E[4], NODE_E[5]],
                        ['E4',  NODE_E[6], NODE_E[7]],
                        ['E5',  NODE_E[8], NODE_E[9]]]

                start = ''
                D = 30 #diameter jarak antara titik pusat x
                E = 45 #diameter jarak antara titik pusat y

                for node3 in NODES:
                    if node3[1]-D <= startx <= node3[1]+D and node3[2]-E <= starty <= node3[2]+E:
                        start = node3[0]
                        break

                #print(start)

                #print('start', start)

                # Searching box berada di dalam atau di luar finish
                #if GOL[0] >=  BOX[0]+D and GOL[0] <=  BOX[0]+D and GOL[1] >=  BOX[0]-E and GOL[1] <=  BOX[1]+E:
                #if (GOL[7] > 15):
                #    goalx = BOX[0]
                #    goaly = BOX[1]
                #    print("Goal Box")
                #else:
                #    goalx = GOL[0]
                #    goaly = GOL[1]
                #    print("Goal Akhir")

                #NJAJAL
                goalx = GOL[0]
                goaly = GOL[1]

                # goal proses
                NODES2 = [['A1',  NODE_A[0], NODE_A[1]],
                        ['A2',  NODE_A[2], NODE_A[3]],
                        ['A3',  NODE_A[4], NODE_A[5]],
                        ['A4',  NODE_A[6], NODE_A[7]],
                        ['A5',  NODE_A[8], NODE_A[9]],
                        ['B1',  NODE_B[0], NODE_B[1]],
                        ['B2',  NODE_B[2], NODE_B[3]],
                        ['B3',  NODE_B[4], NODE_B[5]],
                        ['B4',  NODE_B[6], NODE_B[7]],
                        ['B5',  NODE_B[8], NODE_B[9]],
                        ['C1',  NODE_C[0], NODE_C[1]],
                        ['C2',  NODE_C[2], NODE_C[3]],
                        ['C3',  NODE_C[4], NODE_C[5]],
                        ['C4',  NODE_C[6], NODE_C[7]],
                        ['C5',  NODE_C[8], NODE_C[9]],
                        ['D1',  NODE_D[0], NODE_D[1]],
                        ['D2',  NODE_D[2], NODE_D[3]],
                        ['D3',  NODE_D[4], NODE_D[5]],
                        ['D4',  NODE_D[6], NODE_D[7]],
                        ['D5',  NODE_D[8], NODE_D[9]],
                        ['E1',  NODE_E[0], NODE_E[1]],
                        ['E2',  NODE_E[2], NODE_E[3]],
                        ['E3',  NODE_E[4], NODE_E[5]],
                        ['E4',  NODE_E[6], NODE_E[7]],
                        ['E5',  NODE_E[8], NODE_E[9]]]

                goal = ''
                D = 30 #diameter jarak antara titik pusat x
                E = 45 #diameter jarak antara titik pusat y

                for node2 in NODES2:
                    if node2[1]-D <= goalx <= node2[1]+D and node2[2]-E <= goaly <= node2[2]+E:
                        goal = node2[0]
                        break

                #print(goal)
                #print('goal', goal)

                def initial_graph() :
                    return {
                        'A1': {'A2':1,         'B1':1},
                        'A2': {'A1':1, 'A3':1, 'B2':1},
                        'A3': {'A2':1, 'A4':1, 'B3':1},
                        'A4': {'A3':1, 'A5':1, 'B4':1},
                        'A5': {'A4':1,         'B5':1},
                        'B1': {'A1':1, 'B2':1,         'C1':1},
                        'B2': {'A2':1, 'B1':1, 'B3':1, 'C2':1},
                        'B3': {'A3':1, 'B2':1, 'B4':1, 'C3':1},
                        'B4': {'A4':1, 'B3':1, 'B5':1, 'C4':1},
                        'B5': {'A5':1, 'B4':1,         'C5':1},
                        'C1': {'B1':1, 'C2':1,         'D1':1},
                        'C2': {'B2':1, 'C1':1, 'B3':1, 'D2':1},
                        'C3': {'B3':1, 'C2':1, 'B4':1, 'D3':1},
                        'C4': {'B4':1, 'C3':1, 'B5':1, 'D4':1},
                        'C5': {'B5':1, 'C4':1,         'D5':1},
                        'D1': {'C1':1, 'D2':1,         'E1':1},
                        'D2': {'C2':1, 'D1':1, 'B3':1, 'E2':1},
                        'D3': {'C3':1, 'D2':1, 'B4':1, 'E3':1},
                        'D4': {'C4':1, 'D3':1, 'B5':1, 'E4':1},
                        'D5': {'C5':1, 'D4':1,         'E5':1},
                        'E1': {'D1':1, 'E2':1,         'F1':1},
                        'E2': {'D2':1, 'E1':1, 'B3':1, 'F2':1},
                        'E3': {'D3':1, 'E2':1, 'B4':1, 'F3':1},
                        'E4': {'D4':1, 'E3':1, 'B5':1, 'F4':1},
                        'E5': {'D5':1, 'E4':1,         'F5':1},
                        'F1': {'E1':1, 'F2':1,         'G1':1},
                        'F2': {'E2':1, 'F1':1, 'B3':1, 'G2':1},
                        'F3': {'E3':1, 'F2':1, 'B4':1, 'G3':1},
                        'F4': {'E4':1, 'F3':1, 'B5':1, 'G4':1},
                        'F5': {'E5':1, 'F4':1,         'G5':1},
                        'G1': {'F1':1, 'G2':1,         'H1':1},
                        'G2': {'F2':1, 'G1':1, 'B3':1, 'H2':1},
                        'G3': {'F3':1, 'G2':1, 'B4':1, 'H3':1},
                        'G4': {'F4':1, 'G3':1, 'B5':1, 'H4':1},
                        'G5': {'F5':1, 'G4':1,         'H5':1},
                        'H1': {'G1':1, 'H2':1,         'I1':1},
                        'H2': {'G2':1, 'H1':1, 'B3':1, 'I2':1},
                        'H3': {'G3':1, 'H2':1, 'B4':1, 'I3':1},
                        'H4': {'G4':1, 'H3':1, 'B5':1, 'I4':1},
                        'H5': {'G5':1, 'H4':1,         'I5':1},
                        'I1': {'H1':1, 'I2':1,         'J1':1},
                        'I2': {'H2':1, 'I1':1, 'B3':1, 'J2':1},
                        'I3': {'H3':1, 'I2':1, 'B4':1, 'J3':1},
                        'I4': {'H4':1, 'I3':1, 'B5':1, 'J4':1},
                        'I5': {'H5':1, 'I4':1,         'J5':1},
                        'J1': {'I1':1,         'J2':1},
                        'J2': {'I2':1, 'J1':1, 'J3':1},
                        'J3': {'I3':1, 'J2':1, 'J4':1},
                        'J4': {'I4':1, 'J3':1, 'J5':1},
                        'J5': {'I5':1,         'J4':1}}

                #print(initial_graph())
                #goal
                initial = goal
                path = {}
                adj_node = {}
                queue = []
                graph = initial_graph()
                for node in graph:
                    path[node] = float("inf")
                    adj_node[node] = None
                    queue.append(node)

                path[initial] = 0

                while queue:
                    # find min distance which wasn't marked as current
                    key_min = queue[0]
                    min_val = path[key_min]
                    for n in range(1, len(queue)):
                        if path[queue[n]] < min_val:
                            key_min = queue[n]  
                            min_val = path[key_min]
                    cur = key_min
                    queue.remove(cur)
                    #print(cur)

                    for i in graph[cur]:
                        alternate = graph[cur][i] + path[cur]
                        if path[i] > alternate:
                            path[i] = alternate
                            adj_node[i] = cur

                #start
                x = start
                print('\nThe path between', x, 'to', initial)
                print(x, end = ',')
                #time.sleep(5)
                arr = []
                while True:
                    x = adj_node[x]
                    if x is None:
                        print("")
                        break
                    print(x, end = ',')
                    arr.append(x)
                    #time.sleep(5)

                B = len(arr)
                print('\nBanyak Path:',B)
                print('\nLooping ambil data Path:')

                j = 0
                while B > j:
                    A=arr[j]
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
                    print(A, '= ','x', FINISH[0], '||', 'y', FINISH[1])
                    
                    #if(start == goal):
                    #    j += 1
                    if(GOL[7]>20):
                        #Belok kiri
                        if(GOL[4]>-350 and GOL[4]<-180):
                            db.child("test").child("apa").set(1)
                            print("Kiri")
                        elif(GOL[4]<=90 and GOL[4]>=10):
                            db.child("test").child("apa").set(1)
                            print("Kiri")
                        #Belok kanan
                        elif GOL[4]>-180 and GOL[4]<-10:
                            db.child("test").child("apa").set(2)
                            print("kanan")
                        elif GOL[4]>270 and GOL[4]<350:
                            db.child("test").child("apa").set(2)
                            print("kanan")
                        #Maju
                        elif(GOL[4]<0 and GOL[4]>-10):
                            db.child("test").child("apa").set(3)
                            print("maju")
                        elif(GOL[4]<-350 and GOL[4]>-359):
                            db.child("test").child("apa").set(3)
                            print("maju")
                        elif(GOL[4]<=10 and GOL[4]>=0):
                            db.child("test").child("apa").set(3)
                            print("maju")
                    else:
                        db.child("test").child("apa").set(0)
                        print("stop")
                    time.sleep(5)
                    j += 1

class main_gui( QtWidgets.QDialog, Ui_Form ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh_ui)
        self.timer.start(500)
        
        self.btnRefresh.pressed.connect(self.btnRefresh_handle)
        
        self.rb_raw.clicked.connect(self.rb_raw_handle)
        self.rb_hsv.clicked.connect(self.rb_hsv_handle)
        self.rb_depan.clicked.connect(self.rb_depan_handle)
        self.rb_belakang.clicked.connect(self.rb_belakang_handle)
        self.rb_lapangan.clicked.connect(self.rb_lapangan_handle)
        self.rb_bitwise.clicked.connect(self.rb_bitwise_handle)
        self.rb_box.clicked.connect(self.rb_box_handle)
        self.btnGo.clicked.connect(self.btnGo_handle)

        self.rb_hh.valueChanged.connect(self.rb_hh_handle)
        self.rb_hl.valueChanged.connect(self.rb_hl_handle)
        self.rb_sh.valueChanged.connect(self.rb_sh_handle)
        self.rb_sl.valueChanged.connect(self.rb_sl_handle)
        self.rb_vh.valueChanged.connect(self.rb_vh_handle)
        self.rb_vl.valueChanged.connect(self.rb_vl_handle)

        self.rd_hh.valueChanged.connect(self.rd_hh_handle)
        self.rd_hl.valueChanged.connect(self.rd_hl_handle)
        self.rd_sh.valueChanged.connect(self.rd_sh_handle)
        self.rd_sl.valueChanged.connect(self.rd_sl_handle)
        self.rd_vh.valueChanged.connect(self.rd_vh_handle)
        self.rd_vl.valueChanged.connect(self.rd_vl_handle)

        self.l_hh.valueChanged.connect(self.l_hh_handle)
        self.l_hl.valueChanged.connect(self.l_hl_handle)
        self.l_sh.valueChanged.connect(self.l_sh_handle)
        self.l_sl.valueChanged.connect(self.l_sl_handle)
        self.l_vh.valueChanged.connect(self.l_vh_handle)
        self.l_vl.valueChanged.connect(self.l_vl_handle)

        self.b_hh.valueChanged.connect(self.b_hh_handle)
        self.b_hl.valueChanged.connect(self.b_hl_handle)
        self.b_sh.valueChanged.connect(self.b_sh_handle)
        self.b_sl.valueChanged.connect(self.b_sl_handle)
        self.b_vh.valueChanged.connect(self.b_vh_handle)
        self.b_vh_2.valueChanged.connect(self.b_vl_handle)

        self.PBkiri.clicked.connect(self.PBkiri_handle)
        self.PBkanan.clicked.connect(self.PBkanan_handle)
        self.PBmaju.clicked.connect(self.PBmaju_handle)
        self.PBmundur.clicked.connect(self.PBmundur_handle)
        self.PBstop.clicked.connect(self.PBstop_handle)
        self.PBkananhabis.clicked.connect(self.PBkananhabis_handle)
        self.PBkirihabis.clicked.connect(self.PBkirihabis_handle)
        self.PBlolipop.clicked.connect(self.PBlolipop_handle)

    # Menampilkan angka perhitungan pada UI
    def refresh_ui(self):
        self.info.setText(
            "Start : " + str(ROBOT[0]) + "," + str(ROBOT[1]))

    def refresh_ui(self):
        self.info_2.setText(
            "Goal : " + str(FINISH[0]) + "," + str(FINISH[1]))
           
    # Inisialisasi gerakan
    # Belok Kiri Lurus
    def PBkiri_handle(self):
        print("kiri")
        kiri = 6
        db.child("test").child("apa").set(kiri)
    
    # Belok Kanan Lurus
    def PBkanan_handle(self):
        print("kanan")
        kanan = 7
        db.child("test").child("apa").set(kanan)
    
    # Maju
    def PBmaju_handle(self):
        print("maju")
        maju = 3
        db.child("test").child("apa").set(maju)

    # Mundur
    def PBmundur_handle(self):
        print("mundur")
        mundur = 4
        db.child("test").child("apa").set(mundur)

    # Stop
    def PBstop_handle(self):
        print("stop")
        stop = 0
        db.child("test").child("apa").set(stop)

    # Belok Kiri Habis
    def PBkirihabis_handle(self):
        print("kirihabis")
        kirihabis = 1
        db.child("test").child("apa").set(kirihabis)

    # Belok Kanan Habis
    def PBkananhabis_handle(self):
        print("kananhabis")
        kananhabis = 2
        db.child("test").child("apa").set(kananhabis)

    # Lolipop
    def PBlolipop_handle(self):
        print("lolipop")
        lolipop1 = 8
        db.child("test").child("apa").set(lolipop1)
        time.sleep(2)
        lolipop2 = 0
        
    # Setting Warna Robot Depan    
    def rd_hh_handle(self,angka):
        RD_HI[0] = angka
    def rd_hl_handle(self,angka):
        RD_LO[0] = angka
    def rd_sh_handle(self,angka):
        RD_HI[1] = angka
    def rd_sl_handle(self,angka):
        RD_LO[1] = angka
    def rd_vh_handle(self,angka):
        RD_HI[2] = angka
    def rd_vl_handle(self,angka):
        RD_LO[2] = angka

    # Setting Warna Robot Belakang
    def rb_hh_handle(self,angka):
        RB_HI[0] = angka
    def rb_hl_handle(self,angka):
        RB_LO[0] = angka
    def rb_sh_handle(self,angka):
        RB_HI[1] = angka
    def rb_sl_handle(self,angka):
        RB_LO[1] = angka
    def rb_vh_handle(self,angka):
        RB_HI[2] = angka
    def rb_vl_handle(self,angka):
        RB_LO[2] = angka

    # Setting Warna Lapangan
    def l_hh_handle(self,angka):
        L_HI[0] = angka
    def l_hl_handle(self,angka):
        L_LO[0] = angka
    def l_sh_handle(self,angka):
        L_HI[1] = angka
    def l_sl_handle(self,angka):
        L_LO[1] = angka
    def l_vh_handle(self,angka):
        L_HI[2] = angka
    def l_vl_handle(self,angka):
        L_LO[2] = angka

    # Setting Warna box
    def b_hh_handle(self,angka):
        B_HI[0] = angka
    def b_hl_handle(self,angka):
        B_LO[0] = angka
    def b_sh_handle(self,angka):
        B_HI[1] = angka
    def b_sl_handle(self,angka):
        B_LO[1] = angka
    def b_vh_handle(self,angka):
        B_HI[2] = angka
    def b_vl_handle(self,angka):
        B_LO[2] = angka

    # Button masking
    def rb_raw_handle(self):
        global STATUS_FRAME
        STATUS_FRAME = 0

    def rb_hsv_handle(self):
        global STATUS_FRAME
        STATUS_FRAME = 1

    def rb_depan_handle(self):
        global STATUS_FRAME
        STATUS_FRAME = 2

    def rb_belakang_handle(self):
        global STATUS_FRAME
        STATUS_FRAME = 3

    def rb_lapangan_handle(self):
        global STATUS_FRAME
        STATUS_FRAME = 4

    def rb_bitwise_handle(self):
        global STATUS_FRAME
        STATUS_FRAME = 5

    def rb_box_handle(self):
        global STATUS_FRAME
        STATUS_FRAME = 6

    def btnRefresh_handle(self):
        global CAP
        CAP = cv2.VideoCapture(self.camera_number.value())
        
        # start the thread
        self.thread.start()
    
    # Mengirim data ke python
    def btnGo_handle(self):
        GOL[0] = self.goX.value() # =varcurrentpathx
        print(GOL[0])
        GOL[1] = self.goY.value() # =varcuttentpathy
        print(GOL[1])
        STA[0] = self.staX.value()
        print(STA[0])
        STA[1] = self.staY.value()
        print(STA[1])

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(460, 460, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = main_gui()
    window.setWindowTitle('MOBILE ROBOTIC WITH WIFI COMMUNICATION')
    window.show()
    sys.exit(app.exec_())