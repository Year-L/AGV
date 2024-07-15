#!/usr/bin/env python  
import rospy  
import actionlib  
import collections
from actionlib_msgs.msg import *  
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist  
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal  
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion
from random import sample  
from math import pow, sqrt, atan2

class MultiNav():  
    def __init__(self):  
        rospy.init_node('MultiNav', anonymous=True)  
        rospy.on_shutdown(self.shutdown)  
  
        # 停留时间设置为30秒  
        self.rest_time = rospy.get_param("~rest_time", 10)  
  
        # 是否在模拟环境中运行  
        self.fake_test = rospy.get_param("~fake_test", False)  
  
        # 目标状态返回值  
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED', 'SUCCEEDED',  
                       'ABORTED', 'REJECTED', 'PREEMPTING', 'RECALLING',   
                       'RECALLED', 'LOST']  
  
        # 设定目标位置，使用地图坐标系  
        locations = collections.OrderedDict()  
        #locations['point-1'] = Pose(Point(2.2, -4.6, 0.00), Quaternion(0.000, 0.000, 0.0, 1.0)) 
        #locations['point-2'] = Pose(Point(6.0, -4.7, 0.00), Quaternion(0.000, 0.000, 0.0, 1.0))
        #locations['point-3'] = Pose(Point(10.4, -4.75, 0.00), Quaternion(0.000, 0.000, 0.0, 1.0))
        #locations['point-4'] = Pose(Point(14.4, -4.8, 0.00), Quaternion(0.000, 0.000, 0.0, 1.0))
        locations['point-1'] = Pose(Point(7.48589, 0.85311, 0.00), Quaternion(0.000, 0.000, 0.999874, -0.0158627)) 
        locations['point-2'] = Pose(Point(6.0451, 0.680222, 0.00), Quaternion(0.000, 0.000, 0.999308, -0.037205))
        locations['point-3'] = Pose(Point(4.8602, 0.520906, 0.00), Quaternion(0.000, 0.000, 0.998462, -0.0554456))
        locations['point-4'] = Pose(Point(3.47891, 0.467565, 0.00), Quaternion(0.000, 0.000, 0.99999, -0.0046))
        locations['point-5'] = Pose(Point(8.7856, 0.78669, 0.00), Quaternion(0.000, 0.000, 0.049717, 0.99876))
        # 发布控制机器人移动的指令
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)  
  
        # 订阅move_base动作服务器  
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)  
        rospy.loginfo("Waiting for move_base action server...")  
        self.move_base.wait_for_server(rospy.Duration(60))  
        rospy.loginfo("Connected to move base server")  

        # 初始化IMU和里程计数据
        self.imu_data = None
        self.odom_data = None
        rospy.Subscriber('imu', Imu, self.update_imu)
        rospy.Subscriber('odom', Odometry, self.update_odom)
          
        # 用于用户在RViz中设置初始位置的变量  
        initial_pose = PoseWithCovarianceStamped()  
        # 变量用于跟踪成功率、运行时间和行驶距离  
        n_locations = len(locations)  
        n_goals = 0  
        n_successes = 0  
        i = 0  
        distance_traveled = 0  
        start_time = rospy.Time.now()  
        running_time = 0  
        location = ""  
        last_location = ""  
        # 获取用户设置的初始位置  
        rospy.loginfo("Click on the map in RViz to set the initial pose...")  
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)  
        self.last_location = Pose()  
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose) 
 
        keyinput = int(input("Input 0 to continue,or reget the initialpose!\n"))
        while keyinput != 0:
            rospy.loginfo("Click on the map in RViz to set the initial pose...")  
            rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)  
            rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose) 
            rospy.loginfo("Press y to continue,or reget the initialpose!")
            keyinput = int(input("Input 0 to continue,or reget the initialpose!"))
 
        # 确保我们得到了初始位置  
        while initial_pose.header.stamp == "":  
            rospy.sleep(1)  
        rospy.loginfo("Starting navigation test")  
  
        # 开始主循环，遍历一系列位置  
        for location in locations.keys():  
            rospy.loginfo("Updating current pose.")  
            distance = self.calculate_distance(initial_pose.pose.pose, locations[location])  
            initial_pose.header.stamp = ""  
  
            # 存储上一个位置用于距离计算  
            last_location = location  
  
            # 计数器递增  
            i += 1  
            n_goals += 1  
  
            # 设置下一个目标位置  
            self.goal = MoveBaseGoal()  
            self.goal.target_pose.pose = locations[location]  
            self.goal.target_pose.header.frame_id = 'map'  
            self.goal.target_pose.header.stamp = rospy.Time.now()  
  
            # 告知用户机器人下一个目标位置  
            rospy.loginfo("Going to: " + str(location))  
            # 向目标位置移动  
            self.move_base.send_goal(self.goal)  
  
            # 允许5分钟到达目标  
            finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))  
  
            # 检查成功或失败  
            if not finished_within_time:  
                self.move_base.cancel_goal()  
                rospy.loginfo("Timed out achieving goal")  
            else:  
                state = self.move_base.get_state()  
                if state == GoalStatus.SUCCEEDED:  
                    rospy.loginfo("Goal succeeded!")  
                    n_successes += 1  
                    distance_traveled += distance  
                else:  
                    rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))  
  
            # 计算运行时间  
            running_time = rospy.Time.now() - start_time  
            running_time = running_time.secs / 60.0  
  
            # 打印成功率、距离和时间总结  
            rospy.loginfo("Success so far: " + str(n_successes) + "/" +  
                          str(n_goals) + " = " + str(100 * n_successes/n_goals) + "%")  
            rospy.loginfo("Running time: " + str(self.trunc(running_time, 1)) +  
                          " min Distance: " + str(self.trunc(distance_traveled, 1)) + " m")  
            rospy.sleep(self.rest_time)  

    def update_initial_pose(self, initial_pose):  
        self.initial_pose = initial_pose  

    def update_imu(self, data):
        self.imu_data = data
    
    def update_odom(self, data):
        self.odom_data = data

    def calculate_distance(self, pose1, pose2):
        return sqrt(pow(pose1.position.x - pose2.position.x, 2) + 
                    pow(pose1.position.y - pose2.position.y, 2))

    def shutdown(self):  
        rospy.loginfo("Stopping the robot...")  
        self.move_base.cancel_goal()  
        rospy.sleep(2)  
        self.cmd_vel_pub.publish(Twist())  
        rospy.sleep(1)  

    def trunc(self, f, n):  
        # 截断浮点数到n位小数而不进行四舍五入
        slen = len('%.*f' % (n, f))  
        return float(str(f)[:slen])  
  
if __name__ == '__main__':  
    try:  
        MultiNav()  
        rospy.spin()  
    except rospy.ROSInterruptException:  
        rospy.loginfo("AMCL navigation test finished.") 
