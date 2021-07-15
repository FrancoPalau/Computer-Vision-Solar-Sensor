#!/usr/bin/env python
# coding=utf-8

# INPUTS: CAMERA IMAGE FROM TOPIC
# OUTPUTS: PAPs STEPS + IMAGE WITH CENTER AND AXIES 


import numpy as np
import roslib
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import time
import rospy
from std_msgs.msg import String
from pruebas.msg import numsteps

# Create publisher to see result of algorithm.
pub_sun_center_img = rospy.Publisher('sun_center',Image)
pub_numsteps = rospy.Publisher('num_steps_close_loop',numsteps)
# # Create publisher to send PAPs setpoits steps
# pub_num_steps = rospy.Publisher('num_steps',Image)

precision = 0.04167
# precision_2 = 0.03125
grades_per_step_alt = 7.5/8  # Grades per step divided microsteps mode
grades_per_step_azi = 7.5/8

# Ultil functions
def get_mean(distances):
    return np.mean(distances, axis=0)
def num_steps(mean_dist):
    return int(round(precision * mean_dist[0] / grades_per_step_alt)),\
           int(round(precision * mean_dist[1] / grades_per_step_azi))
def draw_circles(circles, output):
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        # cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), 0)
        cv2.circle(output, (x, y), 0, (0, 128, 255), 4)
def draw_axis(output, th3, distAzi, distAlt):
    # Draw axis names
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(output, 'Altitude', (th3.shape[0] // 2 + 10, 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(output, 'Azimuth', (0, th3.shape[1] // 2 - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Azimuth axis
    cv2.line(output, (0, th3.shape[0] // 2), (th3.shape[1], th3.shape[0] // 2), (0, 0, 255), 2)
    # Altitude axis
    cv2.line(output, (th3.shape[1] // 2, 0), (th3.shape[1] // 2, th3.shape[0]), (0, 255, 255), 2)

    # Draw distance text
    cv2.putText(output, 'DistAlt=' + str(distAlt) + "pixels",
                (10, th3.shape[0] - 20), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(output, 'DistAzi=' + str(distAzi) + "pixels",
                (10, th3.shape[0] - 40), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)


# Definition of callback function of subscriber. The arg, is the image that camera is 
# recording, which is the topic this node is subscribed. 
def callback(data):
    # IMPORTANT
    # cv_bridge is a ROS package used to convert images from ROS to OpenCV or vis versa.
    
    bridge = CvBridge()
    
    # Convert image to be used with cv2 library
    try:
      cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)


    # Begins Franco Palau's code
    # No tengo camara entonces pruebo con una imagen de un sol
    num_pics = 1
    list_centers = []
    output = cv_image.copy()

    # Our operations on the frame come here
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(11,11),0)

 
    ret, th3 = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

    #cv2.imshow('frame', th3)
    #cv2.imwrite('frame.png', th3)

    rows = gray.shape[1]
    circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 1, rows / 4,
                            param1=10, param2=15)
                            # ,minRadius=30, maxRadius=80)
    # print(th3.shape)
    if num_pics < 10:
        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            draw_circles(circles, output)

            # print(circles)

            # Distance from centre of image to centre of sun
            distAzi = (-1)*(circles[0][1] - th3.shape[0] // 2)
            distAlt = (-1)*(circles[0][0] - th3.shape[1] // 2)
            list_centers.append((distAzi, distAlt))
            steps_set_points = numsteps()
            steps_set_points.al,steps_set_points.az = num_steps(get_mean(list_centers))


            draw_axis(output, th3, distAzi, distAlt)

            # show the output image
            # cv2.imshow("output", np.hstack([output]))
            # cv2.imwrite('output.png', np.hstack([output]))
  
            try:
                # Use publisher to pusblish the original image with the circle and axies
                # cv2_to_imgmsg to convert image to msg for ROS
                pub_sun_center_img.publish(bridge.cv2_to_imgmsg(output, "bgr8"))
                pub_numsteps.publish(steps_set_points)
                rospy.loginfo("Sun detected. Entering close loop mode")
                rospy.set_param('close_loop_flag',True)
            except CvBridgeError as e:
                print(e)

        else:
            rospy.loginfo("Sun not detected")
            rospy.set_param('close_loop_flag',False)
            # cv2.imshow('frame', th3)
            # cv2.imwrite('frame.png', th3)

# Subscriptor definition. 
def listener():
    # Init node with name 'vision_sensor'. 
    rospy.init_node('vision_sensor', anonymous=True,log_level=rospy.DEBUG)

    # Create subscriber. Topic name: imagerp, msg: Image, function callback.
    rospy.Subscriber("imagerp", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()