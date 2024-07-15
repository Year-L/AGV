#!/usr/bin/env python3
# coding=utf-8

import rospy
from std_msgs.msg import String
import serial
from time import sleep

# 全局变量用于存储航点名称
waypoints = ['1', '2', '3', '4', '5']
current_index = 0

# 初始化串口
serial_port = serial.Serial('/dev/jxb', 115200, timeout=0.5)
if serial_port.isOpen():
    rospy.loginfo("串口打开成功")
else:
    rospy.loginfo("串口打开失败")

# 串口发送函数
def send_to_stm32(send_data):
    send_data_hex = bytes.fromhex(send_data)
    if serial_port.isOpen():
        serial_port.write(send_data_hex)
        rospy.loginfo(f"发送数据到STM32: {send_data_hex}")
    else:
        rospy.logwarn("串口发送失败")

# 导航结果回调函数，用于处理导航到达后的逻辑
def resultNavi(msg):
    global current_index
    rospy.loginfo("导航结果 = %s", msg.data)
    if msg.data == "done":  # 确保这是到达的正确消息
        send_data = f"0{current_index+1}"  # 根据航点编号生成发送数据
        send_to_stm32(send_data)
        
        rospy.sleep(60)
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

