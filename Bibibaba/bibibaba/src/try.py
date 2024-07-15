
import rospy
from geometry_msgs.msg import Twist
import serial

# 创建串口对象
ser = serial.Serial('/dev/ttyUSB0', 9600)

ser.write(0xff)
ser.write(0x88)
ser.write(0x13)
ser.write(0x00)
ser.write(0x00)
ser.write(0x00)
ser.write(0x00)
ser.write(0x00)
ser.write(0x00)
ser.write(0xfe)
