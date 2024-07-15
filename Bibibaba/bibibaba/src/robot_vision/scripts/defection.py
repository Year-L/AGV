#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import cv2
import numpy as np
from functools import partial
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class DetectorParam:
    def __init__(self):
        self.minArea = rospy.get_param("~minArea", 150)
        self.maxHeightRatio = rospy.get_param("~maxHeightRatio", 0.5)

def detect_defects(frame, detector_param):
    # Convert image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Binary thresholding with Otsu's method
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Morphological operations to remove noise and smooth the image
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3), (-1, -1))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    height, width = frame.shape[:2]
    output = frame.copy()

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)

        # Filter out contours based on conditions
        if h > (height * detector_param.maxHeightRatio):
            continue
        if area < detector_param.minArea:
            continue

        # Draw bounding box and contours
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 1, 8, 0)
        cv2.drawContours(output, [contour], -1, (0, 255, 0), 2, 8)

    return output

def image_cb(msg, cv_bridge, detector_param, image_pub):
    try:
        cv_image = cv_bridge.imgmsg_to_cv2(msg, "bgr8")
        frame = np.array(cv_image, dtype=np.uint8)
    except CvBridgeError as e:
        print(e)
        return

    # Detect defects
    processed_image = detect_defects(frame, detector_param)

    # Publish the processed image
    try:
        image_pub.publish(cv_bridge.cv2_to_imgmsg(processed_image, "bgr8"))
    except CvBridgeError as e:
        print(e)

def main():
    rospy.init_node("defection_detector")
    rospy.loginfo("Starting defection_detector node")

    bridge = CvBridge()
    image_pub = rospy.Publisher("/cv_bridge_image", Image, queue_size=1)

    detector_param = DetectorParam()
    
    bind_image_cb = partial(image_cb, cv_bridge=bridge, detector_param=detector_param, image_pub=image_pub)
    rospy.Subscriber("/usb_cam/image_raw", Image, bind_image_cb)

    rospy.spin()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
