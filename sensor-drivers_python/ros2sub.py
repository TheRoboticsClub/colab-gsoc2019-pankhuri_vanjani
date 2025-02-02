# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
import cv2
import numpy as np
from rclpy.node import Node
import sensor_msgs.msg 
from sensor_msgs.msg import Image
import std_msgs.msg 
from cv_bridge import CvBridge, CvBridgeError


bridge = CvBridge()
class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')

        image_topic = "/camserver/rgb"
        self.subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10)
        self.subscription  # prevent unused variable warning

    def image_callback(self, msg):
        #self.get_logger().info('I heard: "%s"' % msg.data)
        print("Received an image!")
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")


        #cv2_img = br.cv2_to_imgmsg(msg, "bgr8")
 
        cv2.imshow(cv2_img)
        cv2.waitKey(6)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
