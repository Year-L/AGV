#!/usr/bin/env python3
# coding=utf-8

import rospy
from std_msgs.msg import String

# 全局变量用于存储航点名称
waypoints = ['1', '2' ,'3', '4', '5']
current_index = 0

# 导航结果回调函数，用于处理导航到达后的逻辑
def resultNavi(msg):
    global current_index
    rospy.loginfo("导航结果 = %s", msg.data)
    if msg.data == "done":  # 确保这是到达的正确消息   	
        rospy.sleep(2) 
        current_index += 1
        if current_index < len(waypoints):
            publish_waypoint(waypoints[current_index])
        if current_index == len(waypoints):
            rospy.loginfo("所有航点已导航完成")
    elif msg.data == "Failed to get to WayPoint ...":  # 处理导航失败的情况
        rospy.logwarn("导航失败，重新尝试当前航点")
        publish_waypoint(waypoints[current_index])

def publish_waypoint(waypoint):
    rospy.loginfo(f"发布航点 {waypoint}")
    msg = String()
    msg.data = waypoint
    navi_pub.publish(msg)

if __name__ == "__main__":
    rospy.init_node("demo_map_tools")

    # 发布航点名称话题
    navi_pub = rospy.Publisher("/waterplus/navi_waypoint", String, queue_size=10)
    
    # 订阅导航结果话题
    result_sub = rospy.Subscriber("/waterplus/navi_result", String, resultNavi, queue_size=10)
    
    # 延时1秒钟，让后台的话题发布操作能够完成
    rospy.sleep(1)
    
    # 发送第一个航点
    publish_waypoint(waypoints[current_index])
    
    # 构建循环让程序别退出，等待导航结果
    rospy.spin()

