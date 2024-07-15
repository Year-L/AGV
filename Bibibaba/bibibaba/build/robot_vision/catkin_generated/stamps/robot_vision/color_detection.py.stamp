#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import cv2
import numpy as np
from functools import partial
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class DetectorParam:
    def __init__(self):
        self.minArea = rospy.get_param("~minArea", 500)
        self.firstFrame = None

def detect_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges
    color_ranges = {
        "red": ([0, 120, 70], [10, 255, 255], [170, 120, 70], [180, 255, 255]),
        "black": ([0, 0, 0], [180, 255, 30]),
        "white": ([0, 0, 200], [180, 20, 255]),
        "green": ([36, 25, 25], [70, 255, 255]),
        "blue": ([94, 80, 2], [126, 255, 255])
    }

    output = frame.copy()
    for color, ranges in color_ranges.items():
        if color == "red":
            lower1, upper1, lower2, upper2 = ranges
            mask1 = cv2.inRange(hsv, np.array(lower1), np.array(upper1))
            mask2 = cv2.inRange(hsv, np.array(lower2), np.array(upper2))
            mask = mask1 + mask2
        else:
            lower, upper = ranges
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(output, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return output

def image_cb(msg, cv_bridge, detector_param, image_pub):
    try:
        cv_image = cv_bridge.imgmsg_to_cv2(msg, "bgr8")
        frame = np.array(cv_image, dtype=np.uint8)
    except CvBridgeError as e:
        print(e)
        return

    # Detect colors
    processed_image = detect_color(frame)

    # Publish the processed image
    try:
        image_pub.publish(cv_bridge.cv2_to_imgmsg(processed_image, "bgr8"))
    except CvBridgeError as e:
        print(e)

def main():
    rospy.init_node("color_detector")
    rospy.loginfo("Starting color_detector node")

    bridge = CvBridge()
    image_pub = rospy.Publisher("/cv_bridge_image", Image, queue_size=1)

    detector_param = DetectorParam()
    
    bind_image_cb = partial(image_cb, cv_bridge=bridge, detector_param=detector_param, image_pub=image_pub)
    rospy.Subscriber("/usb_cam/image_raw", Image, bind_image_cb)

    rospy.spin()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
