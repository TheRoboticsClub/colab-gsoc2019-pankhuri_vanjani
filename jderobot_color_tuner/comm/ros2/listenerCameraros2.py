import rclpy
from sensor_msgs.msg import Image as ImageROS2
import threading
from math import pi as PI
from jderobotTypes import Image
import cv2
import numpy as np
import time
import datetime

from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String

import comm

MAXRANGE = 8 #max length received from imageD
MINRANGE = 0


def depthToRGB8(float_img_buff, encoding):
    '''
    Translates from Distance Image format to RGB. Inf values are represented by NaN, when converting to RGB, NaN passed to 0 

    @param float_img_buff: ROS Image to translate

    @type img: ros image

    @return a Opencv RGB image

    '''
    gray_image = None
    if (encoding[-3:-2]== "U"):
        gray_image = float_img_buff
    else:    
        float_img = np.zeros((float_img_buff.shape[0], float_img_buff.shape[1], 1), dtype = "float32")
        float_img.data = float_img_buff.data
        gray_image=cv2.convertScaleAbs(float_img, alpha=255/MAXRANGE)


    cv_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)

    return cv_image


def imageMsg2Image(img, bridge):
    '''
    Translates from ROS Image to JderobotTypes Image. 

    @param img: ROS Image to translate
    @param bridge: bridge to do translation

    @type img: sensor_msgs.msg.Image
    @type brige: CvBridge

    @return a JderobotTypes.Image translated from img

    '''
    image = Image()
    print("hi")

    image.width = img.width
    image.height = img.height
    image.format = "RGB8"
    #image.timeStamp = img.header.stamp.seconds + (img.header.stamp.nsecs *1e-9)
    cv_image=0
    if (img.encoding[-2:] == "C1"):
        gray_img_buff = bridge.imgmsg_to_cv2(img, img.encoding)
        cv_image  = depthToRGB8(gray_img_buff, img.encoding)
    else:
        cv_image = bridge.imgmsg_to_cv2(img, "RGB8")
    image.data = cv_image
    return image

class ListenerCameraros2:
    '''
        ROS2 Camera (Image) Subscriber. Camera Client to Receive Images from ROS nodes.
    '''
    def __init__(self, topic):
        '''
        ListenerCamera Constructor.

        @param topic: ROS2 topic to subscribe
        
        @type topic: String

        '''
        self.topic = topic
        self.data = Image()
        self.sub = None
        self.lock = threading.Lock()
        #self.__noderos2 = comm.Communicator.getnoderos2(self)


        self.bridge = CvBridge()
        self.start()
 
    def __callback (self, img):
        '''
        Callback function to receive and save Images. 

        @param img: ROS Image received
        
        @type img: sensor_msgs.msg.Image

        '''
        image = imageMsg2Image(img, self.bridge)

        self.lock.acquire()
        self.data = image
        self.lock.release()
        
    def stop(self):
        '''
        Stops (Unregisters) the client.

        '''
        self.sub.unregister()

    def start (self):
        '''
        Starts (Subscribes) the client.

        '''
        #self.sub = rospy.Subscriber(self.topic,ImageROS2,self.__callback)
        #self.sub = rclpy.subscription.Subscription(handle,ImageROS2, self.topic, self.__callback,None, 10, True)

        self.sub = self.__noderos2.create_subscription(ImageROS2,self.topic, self.__callback,10)

  
    def getImage(self):
        '''
        Returns last Image. 

        @return last JdeRobotTypes Image saved

        '''
        self.lock.acquire()
        image = self.data
        self.lock.release()
        
        return image

    def hasproxy (self):
        '''
        Returns if Subscriber has ben created or not. 

        @return if Subscriber has ben created or not (Boolean)

        '''
        return hasattr(self,"sub") and self.sub


