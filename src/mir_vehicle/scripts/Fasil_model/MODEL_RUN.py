#!/usr/bin/env python

import datetime
import os
import cv2
import time
import rospy
import sys
import numpy as np
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from image_converter import ImageConverter
from drive_run import DriveRun
from config import Config
from image_process import ImageProcess
xMin = 0
yMin = 410
xMax = 800
yMax = 800
class NeuralControl:
    def __init__(self):
        rospy.init_node('controller')
        self.ic = ImageConverter()
        self.image_process = ImageProcess()
        self.rate = rospy.Rate(10)
        self.drive= DriveRun(sys.argv[1])
        rospy.Subscriber('/bulldogbolt/camera_left/image_raw_left', Image, self.controller_cb)
        self.image = None
        self.image_processed = False

    def controller_cb(self, image): 
        img = self.ic.imgmsg_to_opencv(image)
	cropImg = img[yMin:yMax,xMin:xMax]
        img = cv2.resize(cropImg,(160,70))
        self.image = self.image_process.process(img)
        self.image_processed = True


if __name__ == "__main__":
    try:
        neural_control = NeuralControl()
        while not rospy.is_shutdown():
            if neural_control.image_processed == True:
                prediction = neural_control.drive.run(neural_control.image)
		print(prediction)
		joy_pub = rospy.Publisher('/joy', Joy, queue_size = 10)
	        rate = rospy.Rate(10)
      	  	joy_data = Joy()
            	joy_data.axes = [prediction[0][0],0,0,0,0.07,0]
        	joy_pub.publish(joy_data)
        	print(prediction[0][0])
                neural_control.image_processed = False
                neural_control.rate.sleep()

    except KeyboardInterrupt:
	   print ('\nShutdown requested. Exiting...')
