#!/usr/bin/env python


import rospy
from std_msgs.msg import String
import cv2
import os
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import String, Float32
from sensor_msgs.msg import Joy
import sys
sys.path.insert(0, "/home/mir-lab/mirvehicle_ws/src/mirvehicle/scripts")
from image_converter import ImageConverter
sys.path.insert(1, "/home/mir-lab/mir_torcs")
from drive_run import DriveRun
from config import Config
from image_process import ImageProcess


prediction = 0

ic = ImageConverter()



def taker(data):
      joy_pub = rospy.Publisher('/joy', Joy, queue_size = 10)
      joy_data = Joy()
      img = ic.imgmsg_to_opencv(data)
      config = Config()
      image_process = ImageProcess()   
      IImage = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  
      IImage = cv2.resize(IImage, (config.image_size[0],
                                   config.image_size[1]))
      IImage = image_process.process(IImage)
      #cv2.imwrite('balu.jpg', IImage)
      #drive_run = DriveRun(sys.agrv[1])
      drive_run = DriveRun('/home/mir-lab/Desktop/Balu_Autodrive/2018-06-14-15-16-03')
      prediction= drive_run.run(IImage)
      #print(prediction)
      #print(np.shape(prediction))
      #print(type(prediction))
      if(prediction[0][0] > 0.3):
	 #print("1")
         prediction[0][0] = 1
      elif(prediction[0][0] < -0.3):
	   #print("2")
           prediction[0][0] = -1
      else:
	  #print("3")	
          prediction[0][0] = 0
      #new_pred = prediction.astype(np.float)
      #new_predd = np.asscalar(np.array([prediction]))
      #print(type(new_predd))
      #print(np.shape(new_predd))
      #new_predd = joy_data.axes.append(0)
      #0.25 = joy_data.axes.append(3)
      #print(new_predd)
      #print(prediction[0][0])
      joy_data.axes = [prediction[0][0],0,0,0.05,0,0]
      joy_pub.publish(joy_data)
      

def listener():


    rospy.init_node('conerted_image', anonymous=True)

    rospy.Subscriber('/bulldogbolt/camera_left/image_raw_left', Image, taker)
    
    rospy.spin()

def main():
    try:
        if(len(sys.argv) != 2):
            print('Use model_name')
            return
        
        else:
            # load model
            drive = DriveRun('/home/mir-lab/Desktop/Balu_Autodrive/2018-06-14-15-16-03')
            print('model loaded...')
            
            taker(data)

        
    except KeyboardInterrupt:    
        print('\nShutdown requested. Exiting...')

if __name__ == '__main__':
    
	listener()
