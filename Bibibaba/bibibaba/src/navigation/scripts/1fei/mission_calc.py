#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from PSO_for_singleAGV import pso
from std_msgs.msg import Int16MultiArray

def talker():
    pub = rospy.Publisher('locations', Int16MultiArray, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10);
    while not rospy.is_shutdown():
        # mission_result = result
        rospy.loginfo(mission_result)
        pub.publish(mission_result)
        rate.sleep()

if __name__ == '__main__':
    try:
        order_st = [[0,1,2,0,3,0,2,0,2,1]]
        order_ed = [[3,2,1,2,1,0,2,3,1,1]]
    
        glob_p,result = pso(order_st,order_ed)
        mission_result = Int16MultiArray(data=result)
        talker()
    except rospy.ROSInterruptException:
        pass

    
    
