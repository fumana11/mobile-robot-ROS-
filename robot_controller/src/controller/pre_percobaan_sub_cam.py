#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def video_callback(msg):
    
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    
    cv2.imshow('Video', frame)
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

