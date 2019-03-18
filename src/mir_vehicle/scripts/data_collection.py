#!/usr/bin/env python

import rospy
import cv2
import os
import numpy as np
import datetime
import time

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from image_converter import ImageConverter
from std_msgs.msg import String

vehicle_steer = 0
vehicle_vel = 0

ic = ImageConverter()
path = '/home/mir-lab/Desktop/Collected_Data/' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '/')
if os.path.exists(path):
    print('path exists. continuing...')
else:
    os.makedirs(path)

text = open(str(path) + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".txt", "w+")


def vehicle_param(value):
    global vehicle_vel, vehicle_steer
    vehicle_vel = value.linear.x
    vehicle_steer = value.angular.z
    #return (vehicle_vel, vehicle_steer)

def recorder(data):
    img = ic.imgmsg_to_opencv(data)
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    cv2.imwrite(str(path) + str(time_stamp) + '.jpg',img)
    text.write(str(time_stamp) + '\t' + str(vehicle_steer) + '\t' + str(vehicle_vel) + "\r\n")

def main():
   rospy.init_node('data_collection')
   rospy.Subscriber('/bulldogbolt/cmd_vel', Twist, vehicle_param)
   rospy.Subscriber('/bulldogbolt/camera_left/image_raw_left', Image, recorder)
   rospy.spin()

if __name__ == '__main__':
    main()
