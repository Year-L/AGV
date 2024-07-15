#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry

def callback(data):
    odom_msg = Odometry()
    odom_msg.header = data.header
    odom_msg.pose = data.pose
    odom_pub.publish(odom_msg)

rospy.init_node('pose_to_odom_converter')
odom_pub = rospy.Publisher('/odom_combined', Odometry, queue_size=10)
rospy.Subscriber('/odom_combined_pose', PoseWithCovarianceStamped, callback)
rospy.spin()
