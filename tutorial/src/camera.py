#!/usr/bin/env python

import rospy

import cv2
import numpy as np
import matplotlib
import time
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
device_cam = cv2.VideoCapture(0)
bridge = CvBridge()

def nothing(x):
    pass

while True :    
    _, frame= device_cam.read()
    scale_percent = 10 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    layer = frame.shape [:2]
    
    #cv2.imshow('Layer_Webcam', frame)

    pub = rospy.Publisher('Video_data', String, queue_size=60)
    rospy.init_node('Supervisory', anonymous=True)
    rate = rospy.Rate(60) # 10hz
    
    rospy.loginfo(layer)
    pub.publish(layer)
    rate.sleep()
    
    if cv2.waitKey(1) == 27:
        device.release()
        cv2.destroyAllWindows()
        break
        try:
        	talker()
        except rospy.ROSInterruptException:
        	pass
