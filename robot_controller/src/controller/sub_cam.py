#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String
from geometry_msgs.msg import Point
from robot_controller.msg import GoalPosition

import cv2
import math
import numpy as np


GOAL = np.array([0,0,0,0,0,0])
ROBOT = np.array([0,0,0])

FINISH = np.array([0,0])

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



def video_callback(msg):
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for the first color (in HSV) - Color 1 (Koordinat Robot)
    lower_bound_color1 = np.array([97,136,132])
    upper_bound_color1 = np.array([138,255,255])

        # Define the lower and upper bounds for the second color (in HSV) - Color 2 (Koordinat Tujuan)
    lower_bound_color2 = np.array([19, 65, 229])
    upper_bound_color2 = np.array([85, 234, 255])

        # Create masks for each color
    mask_robot = cv2.inRange(hsv_image, lower_bound_color1, upper_bound_color1)
    mask = cv2.inRange(hsv_image, lower_bound_color2, upper_bound_color2)


    pub1=rospy.Publisher('Goal_Position',GoalPosition,queue_size=1)
    #rospy.loginfo('x')
    
    cv2.imshow('o', frame)
    bitwise = frame
    
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



    try:
        n = cv2.moments(mask_robot)
        ROBOT[0] = int(n["m10"] / n["m00"])
        ROBOT[1] = int(n["m01"] / n["m00"])
    except:
        ROBOT[0] = 0
        ROBOT[1] = 0
    
    try:
        m = cv2.moments(mask)
        GOAL[0] = int(m["m10"] / m["m00"])
        GOAL[1] = int(m["m01"] / m["m00"])
    except:
        GOAL[0] = 0
        GOAL[1] = 0


    
    FINISH [0] = NODE_G[8]
    FINISH [1] = NODE_G[9] 
    # derajad hadap robot
    GOAL[2] = (ROBOT[0] + GOAL[0])/2 
    GOAL[3] = (ROBOT[1] + GOAL[1])/2 
    
    #derajad set poin robot
    GOAL[4] = math.degrees(math.atan2(GOAL[3],GOAL[2]))
           
    # Derajat hadap robot - Derajat setpoint terhadap robot
    ROBOT[2] = math.degrees(math.atan2(ROBOT[1],ROBOT[0]))
    GOAL[5] = ROBOT[2]-GOAL[4]
    
        
    cv2.circle(bitwise, (ROBOT[0], ROBOT[1]), 10, (0, 0, 255), -1)
    cv2.circle(bitwise, (GOAL[0], GOAL[1]), 10, (0, 0, 255), -1)
    cv2.circle(bitwise, (GOAL[2], GOAL[3]), 10, (0, 0, 255), -1)
    
    pub1.publish(x_robot = ROBOT[0] , y_robot = ROBOT[1],x_depan = GOAL[0] , y_depan = GOAL[1] )


    cv2.imshow('Video', frame)
    print('koordinat x : ', GOAL[2] ,'koordinat y : ',GOAL[3])
    #rospy.loginfo(ROBOT[0])

    cv2.waitKey(1)

        

def subscribe_video():
    rospy.init_node('video_subscriber', anonymous=True)
    rospy.Subscriber('image_raw', Image, video_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        subscribe_video()
    except rospy.ROSInterruptException:
        pass

