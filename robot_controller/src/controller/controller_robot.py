#!/usr/bin/env python3
import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import UInt16

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.Qt import Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from gui import Ui_Form

pub = rospy.Publisher('controllerPub', String, queue_size=10)
rospy.init_node('controller_gui') #, anonymous=True)
rate = rospy.Rate(10) # 10hz

robotMoveValue      = "Berhenti"
sensorDepanValue    = 0
sensorBelakangValue = 0


class info_thread(QThread):
    
    def callback_robotMove(self,data):
        global robotMoveValue 
        robotMoveValue = data.data
        #print("Robot Move:", data.data)

    def callback_sensorDepan(self,data):
        global sensorDepanValue 
        sensorDepanValue = data.data
        #print("Jarak Depan:", data.data)
    
    def callback_sensorBelakang(self,data):
        global sensorBelakangValue 
        sensorBelakangValue = data.data
        #print("Jarak Belakang:", data.data)

    def run(self):
        while not rospy.is_shutdown():
            try:
                rospy.Subscriber('robotMove', String, self.callback_robotMove)
                rospy.Subscriber('sensorDepan', UInt16, self.callback_sensorDepan)
                rospy.Subscriber('sensorBelakang', UInt16, self.callback_sensorBelakang)
                                
                rospy.spin()

            except rospy.ROSInterruptException:
                pass

class uiLoop (QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.info_th = info_thread(self)
        self.info_th.start()

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.updateValue)
        self.timer.start(100)

	
        #self.btn_forward.pressed.connect(self.handle_btn_forward)
        #self.btn_reverse.pressed.connect(self.handle_btn_reverse)
        #self.btn_turnRight.pressed.connect(self.handle_btn_turnRight)
        #self.btn_turnLeft.pressed.connect(self.handle_btn_turnLeft)
        #self.btn_rotateRight.pressed.connect(self.handle_btn_rotateRight)
        #self.btn_rotateLeft.pressed.connect(self.handle_btn_rotateLeft)
        
        #self.btn_forward.clicked.connect(self.handle_btn_forward)
        #self.btn_reverse.clicked.connect(self.handle_btn_reverse)
        #self.btn_turnRight.clicked.connect(self.handle_btn_turnRight)
        #self.btn_turnLeft.clicked.connect(self.handle_btn_turnLeft)
        #self.btn_rotateRight.clicked.connect(self.handle_btn_rotateRight)
        #self.btn_rotateLeft.clicked.connect(self.handle_btn_rotateLeft)
        #self.btn_stop.clicked.connect(self.handle_btn_stop)
        
        
        self.btn_forward.pressed.connect(self.handle_btn_forward)
        self.btn_forward.released.connect(self.handle_btn_stop)
        
        self.btn_reverse.pressed.connect(self.handle_btn_reverse)
        self.btn_reverse.released.connect(self.handle_btn_stop)
        
        self.btn_turnRight.pressed.connect(self.handle_btn_turnRight)
        self.btn_turnRight.released.connect(self.handle_btn_stop)
        
        self.btn_turnLeft.pressed.connect(self.handle_btn_turnLeft)
        self.btn_turnLeft.released.connect(self.handle_btn_stop)
        
        self.btn_rotateRight.pressed.connect(self.handle_btn_rotateRight)
        self.btn_rotateRight.released.connect(self.handle_btn_stop)
        
        self.btn_rotateLeft.pressed.connect(self.handle_btn_rotateLeft)
        self.btn_rotateLeft.released.connect(self.handle_btn_stop)
        
        self.btn_stop.pressed.connect(self.handle_btn_stop)
        
        
    def updateValue(self):
        
        #print("robotMove:",robotMoveValue)
        #print("sensorDepan:",sensorDepanValue)
        #print("sensorBelakang:",sensorBelakangValue)

        self.lbl_robotMove.setText(str(robotMoveValue))
        self.lbl_sensorDepan.setText(str(sensorDepanValue))
        self.lbl_sensorBelakang.setText(str(sensorBelakangValue))


    def handle_btn_forward(self):
        pub.publish("w")
    
    def handle_btn_reverse(self):
        pub.publish("s")
    
    def handle_btn_turnRight(self):
        pub.publish("d")
    
    def handle_btn_turnLeft(self):
        pub.publish("a")
    
    def handle_btn_rotateRight(self):
        pub.publish("3")
    
    def handle_btn_rotateLeft(self):
        pub.publish("1")
    
    def handle_btn_stop(self):
        pub.publish("2")
    

if __name__ =='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Windows')
    window = uiLoop()
    window.setWindowTitle('Controller Robot Mobile')
    window.show()
    sys.exit(app.exec_())
