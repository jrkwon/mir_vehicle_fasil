#!/usr/bin/env python
# 
# Author: Jonathan Sprinkle
# Copyright (c) 2015-2016 Arizona Board of Regents
# All rights reserved.
# 
# Permission is hereby granted, without written agreement and without 
# license or royalty fees, to use, copy, modify, and distribute this
# software and its documentation for any purpose, provided that the 
# above copyright notice and the following two paragraphs appear in 
# all copies of this software.
# 
# IN NO EVENT SHALL THE ARIZONA BOARD OF REGENTS BE LIABLE TO ANY PARTY 
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES 
# ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN 
# IF THE ARIZONA BOARD OF REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF 
# SUCH DAMAGE.
# 
# THE ARIZONA BOARD OF REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
# AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER
# IS ON AN "AS IS" BASIS, AND THE ARIZONA BOARD OF REGENTS HAS NO OBLIGATION
# TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

##############################################################################
# Author: Jaerock Kwon
# ============================================================================
# 12/1/2017: Change the namespace 'catvehicle' to 'mirvehicle'
#
# ============================================================================


import rospy
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Twist, Pose
from sensor_msgs.msg import Joy
import sys, getopt
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
        img = cv2.resize(img,(160,70))
        self.image = self.image_process.process(img)
        self.image_processed = True


# requires the ros-indigo-joysticks
"""
class joy2cmdvel:

    def __init__(self):
        rospy.init_node('joy2cmdvel', anonymous=True)

        self.ns = rospy.get_param("~namespace", "mirvehicle")
        self.velmax = rospy.get_param("~velmax",11)

        rospy.loginfo(rospy.get_caller_id() + " startup in namespace {0} with max velocity {1}".format(self.ns,self.velmax))


        #rospy.Subscriber('/joy'.format(self.ns), Joy, self.callback)
        self.pub_cmdvel = rospy.Publisher('{0}/cmd_vel'.format(self.ns), Twist, queue_size=1)

        self.x = 0
        self.z = 0

    def callback(self,data):
#        rospy.loginfo(rospy.get_caller_id() + " heard linear=%lf, angular=%lf", data.axes[3], data.axes[0])
        self.x = data.axes[4]*self.velmax
	#self.x = data.axes[3]
        self.z = data.axes[0]

    def publish(self):
        msgTwist = Twist()
        msgTwist.linear.x = self.x
        msgTwist.angular.z = self.z
        self.pub_cmdvel.publish(msgTwist)
        
def usage():
    print('joy2cmdvel -n mirvehicle')
"""

def main(argv):

    node = joy2cmdvel()
    rate = rospy.Rate(10) # run at 100Hz
    while not rospy.is_shutdown():
        node.publish()
        rate.sleep()

if __name__ == '__main__':
    try:
        neural_control = NeuralControl()
        while not rospy.is_shutdown():
            if neural_control.image_processed == True:
                prediction = (neural_control.drive.run(neural_control.image))
		print(prediction)
		joy_twist = rospy.Publisher('/bulldogbolt/cmd_vel', Twist, queue_size=10)
	        rate = rospy.Rate(10)
      	  	twist_data = Twist()
		twist_data.linear.x = 20
		twist_data.linear.y = 0
		twist_data.linear.z = 0
                twist_data.angular.z = prediction
		twist_data.angular.x = 0
		twist_data.angular.y =0
        	joy_twist.publish(twist_data)
        	print(prediction[0][0])
                neural_control.image_processed = False
                neural_control.rate.sleep()

    except KeyboardInterrupt:
	   print ('\nShutdown requested. Exiting...')

