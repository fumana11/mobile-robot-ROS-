#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import time
import cv2
import math

class ImageProcessing:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)

    def callback(self, data):
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        gray_image_blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
        cv2.imshow("gray_image_blur", gray_image_blur)

        cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node('path_planning_camera_node')
    image_processing = ImageProcessing()
    rospy.spin()