/*********************************
 * 串口节点，订阅cmd_vel话题并发布odometry话题
 * 从cmd_vel话题中分解出速度值通过串口送到移动底盘
 * 从底盘串口接收里程消息整合到odometry话题用于发布
 *
 * @StevenShi
 * *******************************/
#include <ros/ros.h>
#include <serial/serial.h>
#include <std_msgs/String.h>
#include <std_msgs/Empty.h>
#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include <tf/transform_broadcaster.h>
#include <math.h>
#include <my_serial_node/Agv.h>
#include <my_serial_node/Balance.h>
 

#define sBUFFERSIZE 10				 // send buffer size 串口发送缓存长度
#define rBUFFERSIZE 23				 // receive buffer size 串口接收缓存长度
#define PI 3.141593
#define RATIO 1.0/(3072) //编码器分辨率500，电机减速比24，4倍频
#define RADIUS 0.0508 //车轮半径

#define ENTF 1

unsigned char s_buffer[sBUFFERSIZE]; //发送缓存
unsigned char r_buffer[10000]; //接收缓存
uint8_t buff[rBUFFERSIZE]; //接收缓存，用于数据对齐
uint8_t key = 0;

/************************************
 * 串口数据发送格式共15字节
 * head head type linear_v_x  linear_v_y angular_v  CRC
 * 0xff 0xff 0x01 short       short      short      u8
 * **********************************/
/************************************
* 串口数据接收格式共20字节
* head head type 左前轮       右前轮       左后轮       右后轮       CRC(异或校验)
* 0xff 0xff 0x02 int         int         int         int         u8
* e.g. ff ff 02 /1f 07 00 00/1f 07 00 00/1f 07 00 00/1f 07 00 00/02
* **********************************/

//联合体，用于short与16进制的快速转换
typedef union
{
	unsigned char cvalue[2];
	short svalue;
} short_union;

typedef union 
{
	unsigned char cvalue[4];
	int ivalue;
} int_union;
typedef union
{
	unsigned char cvalue;
	short ivalue;
} short_int_union;

serial::Serial ser;

/**********************************************************
 * 数据打包，将获取的cmd_vel信息打包并通过串口发送
 * ********************************************************/
void data_pack(const geometry_msgs::Twist &cmd_vel)
{
	// unsigned char i;
	short_union Vx, Vy, Ang_v;
	Vx.svalue = short(cmd_vel.linear.x*10000);
	Vy.svalue = -short(cmd_vel.linear.y*10000);
	Ang_v.svalue = short(cmd_vel.angular.z*10000);

	memset(s_buffer, 0, sizeof(s_buffer));
	//数据打包
	s_buffer[0] = 0xff;
	s_buffer[1] = 0xff;

	s_buffer[2] = 0x03;
	// Vx
	s_buffer[5] = Vx.cvalue[0];
	s_buffer[6] = Vx.cvalue[1];

	// Vy
	s_buffer[3] = Vy.cvalue[0];
	s_buffer[4] = Vy.cvalue[1];
	
	// Ang_v
	s_buffer[7] = Ang_v.cvalue[0];
	s_buffer[8] = Ang_v.cvalue[1];
	
	// CRC
	s_buffer[9] = s_buffer[0] ^ s_buffer[1] ^ s_buffer[2] ^ s_buffer[3] ^ s_buffer[4] ^ 
				   s_buffer[5] ^s_buffer[6] ^ s_buffer[7] ^ s_buffer[8];
	
	// for(int i=0;i<10;i++){
	// 	ROS_INFO("0x%02x",s_buffer[i]);
	// }
	
	ser.write(s_buffer, sBUFFERSIZE);
}
//接收数据分析与校验0
unsigned char data_analysis(unsigned char *buffer)
{
	unsigned char ret = 0, csum;
	// int i;
	if ((buffer[0] == 0xff) && (buffer[1] == 0xff))
	{
		csum = buffer[0] ^ buffer[1] ^ buffer[2] ^ buffer[3] ^ buffer[4] ^ buffer[5] ^
			   buffer[6] ^ buffer[7] ^ buffer[8] ^ buffer[9] ^ buffer[10] ^ buffer[11] ^ buffer[12] ^ buffer[13] ^ buffer[14] ^ buffer[15] ^ buffer[16] ^ buffer[17] ^ buffer[18] ^ buffer[19] ^ buffer[20] ^ buffer[21];
		//ROS_INFO("check sum:0x%02x",csum);
		/*for(int i=0;i<23;i++){
	ROS_INFO("0x%02x",buffer[i]);
	 }*/
		if (csum == buffer[22])
		{
			ret = 1; //校验通过，数据包正确
		}
		else
			ret = 0; //校验失败，丢弃数据包
	}
	
	// for(int i=0;i<rBUFFERSIZE;i++)
	   //ROS_INFO("Data Analysis");
	// ROS_INFO("%d",ret);
	// ROS_INFO("\n");
	
	return ret;
}

void handleSerialData(uint8_t rawData){
	buff[key] = rawData;
	key++;

	if (buff[0] != 0xff){
		key = 0;
		return;
	}
	if(key > 1 && buff[1] != 0xff){
		key = 0;
		return;
	}
	if (key < 20){
		return;
	}
	
	//ROS_INFO("Handle Data");
}

//订阅/cmd_vel话题的回调函数，用于显示速度以及角速度
void cmd_vel_callback(const geometry_msgs::Twist &cmd_vel)
{
	// ROS_INFO("I heard linear velocity: x-[%f],y-[%f],", cmd_vel.linear.x, cmd_vel.linear.y);
	// ROS_INFO("I heard angular velocity: [%f]", cmd_vel.angular.z);
	// std::cout << "Twist Received" << std::endl;
	data_pack(cmd_vel);
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "my_serial_node");
	ros::NodeHandle nh;

	//订阅/cmd_vel话题用于测试 $ rosrun turtlesim turtle_teleop_key
	ros::Subscriber write_sub = nh.subscribe("/cmd_vel", 1000, cmd_vel_callback);
	//发布里程计话题 odom
	ros::Publisher read_pub = nh.advertise<nav_msgs::Odometry>("odom", 100);//wheel_odom
	ros::Publisher v_pub = nh.advertise<my_serial_node::Agv>("power",100);
	ros::Publisher weight_pub = nh.advertise<my_serial_node::Balance>("weight",100);

	my_serial_node::Agv agv;
	my_serial_node::Balance balance;

	try
	{
		ser.setPort("/dev/stm32");
		ser.setBaudrate(115200);
		serial::Timeout to = serial::Timeout::simpleTimeout(50);
		ser.setTimeout(to);
		ser.open();
	}
	catch (serial::IOException &e)
	{
		ROS_ERROR_STREAM("Unable to open port ");
		return -1;
	}

	if (ser.isOpen())
	{
		ROS_INFO_STREAM("Serial Port initialized");
	}
	else
	{
		return -1;
	}
	
	//开启编码器消息
	s_buffer[0] = 0xff;
	s_buffer[1] = 0xff;
	s_buffer[2] = 0x05;
	s_buffer[5] = 0x00;
	s_buffer[6] = 0x00;
	s_buffer[3] = 0x00;
	s_buffer[4] = 0x00;
	s_buffer[7] = 0x00;
	s_buffer[8] = 0x00;
	s_buffer[9] = 0x05;
	ser.write(s_buffer, sBUFFERSIZE);
	memset( s_buffer,0,sBUFFERSIZE);	
	s_buffer[0] = 0xff;
	s_buffer[1] = 0xff;
	s_buffer[2] = 0x06;
	s_buffer[5] = 0x00;
	s_buffer[6] = 0x00;
	s_buffer[3] = 0x00;
	s_buffer[4] = 0x00;
	s_buffer[7] = 0x00;
	s_buffer[8] = 0x00;
	s_buffer[9] = 0x06;
	ser.write(s_buffer, sBUFFERSIZE);

	//定义tf 对象
	static tf::TransformBroadcaster odom_broadcaster;
	#if ENTF
	//定义tf发布时需要的类型消息
	geometry_msgs::TransformStamped odom_trans;
	#endif
	//定义里程计消息对象
	nav_msgs::Odometry odom;
	//定义四元数变量
	geometry_msgs::Quaternion odom_quat;
	//编码器原始数据 位置 速度 角速度(单位rad/s)
	int_union bm1,bm2,bm3,bm4,bm1_last,bm2_last,bm3_last,bm4_last;
	short_union weight;
	short_int_union voltage;
	
	float posx, posy, vx, vy, va, yaw, dx, dy, dz;
	float ODOM_POSE_COVARIANCE[36] = {1e-3, 0, 0, 0, 0, 0, 
                        0, 1e-3, 0, 0, 0, 0,
                        0, 0, 1e6, 0, 0, 0,
                        0, 0, 0, 1e6, 0, 0,
                        0, 0, 0, 0, 1e6, 0,
                        0, 0, 0, 0, 0, 1e3};
	float ODOM_POSE_COVARIANCE2[36] = {1e-9, 0, 0, 0, 0, 0, 
                         0, 1e-3, 1e-9, 0, 0, 0,
                         0, 0, 1e6, 0, 0, 0,
                         0, 0, 0, 1e6, 0, 0,
                         0, 0, 0, 0, 1e6, 0,
                         0, 0, 0, 0, 0, 1e-9};
 
	float ODOM_TWIST_COVARIANCE[36] = {1e-3, 0, 0, 0, 0, 0, 
                         0, 1e-3, 0, 0, 0, 0,
                         0, 0, 1e6, 0, 0, 0,
                         0, 0, 0, 1e6, 0, 0,
                         0, 0, 0, 0, 1e6, 0,
                         0, 0, 0, 0, 0, 1e3};
	float ODOM_TWIST_COVARIANCE2[36] = {1e-9, 0, 0, 0, 0, 0, 
                          0, 1e-3, 1e-9, 0, 0, 0,
                          0, 0, 1e6, 0, 0, 0,
                          0, 0, 0, 1e6, 0, 0,
                          0, 0, 0, 0, 1e6, 0,
                          0, 0, 0, 0, 0, 1e-9};

	//定义时间
	ros::Time current_time, last_time;
	// ros::Duration dt_Duration;
	// current_time = last_time = ros::Time::now();
	// 初始化
	posx = posy = 0.0; // xy 坐标
	yaw = 0.0;
	bm1.ivalue = bm2.ivalue = bm3.ivalue = bm4.ivalue = 0;
	bm1_last.ivalue = bm2_last.ivalue = bm3_last.ivalue = bm4_last.ivalue = 0;
	//ROS_INFO("%f %f",posx,posy);
	// vx.svalue = vy.svalue = va.svalue = 0; // 速度、角速度
	// dx.svalue = dy.svalue = dz.svalue = yaw.svalue = 0;
	// 10hz频率执行
	ros::Rate loop_rate(30);

	uint8_t flag = 0; //是否首次进入循环

	ser.flush();
	
	float weight_middle1 = 0;
	float weight_middle2 = 0;
	float weight_val = 0;
	int q = 0;
	while (ros::ok())
	{

		ros::spinOnce();

		int buffer_count = ser.available();
		// ROS_INFO("%d",buffer_count);
		if (ser.available())
		{
			// ROS_INFO_STREAM("Reading from serial port");
			
			try
			{
				ser.read(r_buffer, buffer_count);

			}
			catch(const std::exception& e)
			{
				std::cerr << e.what() << '\n';
			}
			int i;
			/*for(i=0;i<rBUFFERSIZE;i++)
				ROS_INFO("[0x%02x]",r_buffer[i]);*/
			//ROS_INFO_STREAM("End reading from serial port");
			
			//ROS_INFO("Data Received");

			for(int i=0;i<buffer_count;i++){
				handleSerialData(r_buffer[i]);
			}

			if (data_analysis(buff) != 0)
			{
				//先用现有下位机代码进行数据处理...
				//ROS_INFO("Data Correct");
				
				
				
				
				
				//数据处理
				 ROS_INFO("hh");
				switch (buff[2])
				{
				/*case 0x0a:
				{
					for(int j = 0; j < 4; j++){
						weight.cvalue[j] = buff[6+j];
						weight.cvalue[j] = buff[5+j];
						weight.cvalue[j] = buff[4+j];
						weight.cvalue[j] = buff[3+j];
					}
					balance.weight = weight.ivalue;
					memset(buff,0,rBUFFERSIZE);		
					key = 0;
					weight_pub.publish(balance);
					break;
				case 0x08:
				{
					for(int j = 0; j < 4; j++){
						voltage.cvalue[j] = buff[6+j];
						voltage.cvalue[j] = buff[5+j];
						voltage.cvalue[j] = buff[4+j];
						voltage.cvalue[j] = buff[3+j];
					}
					memset(buff,0,rBUFFERSIZE);		
					key = 0;
					agv.volt= voltage.ivalue/1000;
					if (voltage.ivalue >= 12.24) {
						agv.power = 90.0;
					} else if (agv.volt >= 12) {
						agv.power = 80.0;
					} else if (agv.volt >= 11.79) {
						agv.power = 70.0;
					} else if (agv.volt >= 11.61) {
						agv.power = 60.0;
					} else if (agv.volt >= 11.46) {
						agv.power = 50.0;
					} else if (agv.volt >= 11.37) {
						agv.power = 40.0;
					} else if (agv.volt >= 11.31) {
						agv.power = 30.0;
					} else if (agv.volt >= 11.19) {
						agv.power = 20.0;
					} else if (agv.volt >= 11.1) {
						agv.power = 10.0;
					} else if (agv.volt >= 11.04) {
						agv.power = 5.0;
					} else {
						agv.power = 0.0;
					}
					v_pub.publish(agv);
					// ROS_INFO("%02x",voltage.cvalue[0]);
					// ROS_INFO("%02x",voltage.cvalue[1]);
					// ROS_INFO("%02x",voltage.cvalue[2]);
					// ROS_INFO("%02x",voltage.cvalue[3]);
					// ROS_INFO("over");
					break;
				}*/
				case 0x02:
				{
					for(int i = 0;i < 2;i++){
					weight.cvalue[i] = buff[20+i];
				}
				
				weight_val = weight.svalue-400-(weight.svalue-400)/50*4;
				if(q == 1){
				weight_middle1 = weight_val;
				weight_middle2 = weight_val;
				balance.weight = 0;  
				ROS_INFO("%f",weight_middle2);
				}
				//ROS_INFO("middle1=%f",weight_middle1);
				//ROS_INFO("middle2=%f",weight_middle2);
				//ROS_INFO("q=%d",q);
				if(weight_middle1 >= weight_val && weight_middle1 - weight_val >= 10){
					balance.weight = weight_middle1 - weight_val;
					weight_middle1 = weight_val;
					weight_middle2 = weight_middle1;
				}else if(weight_val> weight_middle2 && weight_val - weight_middle2 >= 10){
					balance.weight = weight_val - weight_middle2;
					weight_middle2 = weight_val;
					weight_middle1 = weight_middle2;
				}						
				weight_pub.publish(balance);
				
				
				voltage.cvalue = buff[19];
				agv.power= voltage.cvalue;
				
				ROS_INFO("%d",voltage.cvalue);
				//ROS_INFO("%d\n",voltage.ivalue);
					
					if (flag)
					{
						for(int j = 0; j < 4; j++){
							bm1_last.cvalue[j] = buff[3+j];
							bm2_last.cvalue[j] = buff[7+j];
							bm3_last.cvalue[j] = buff[11+j];
							bm4_last.cvalue[j] = buff[15+j];
						}
						memset(buff,0,rBUFFERSIZE);
						key = 0;
						flag = 0;
						continue;
					}
					
					int j;
					for(j = 0; j < 4; j++){
			                		bm1.cvalue[j] = buff[3+j];
						bm2.cvalue[j] = buff[7+j];
						bm3.cvalue[j] = buff[11+j];
						bm4.cvalue[j] = buff[15+j];
						
						
					}
					
					bm1.ivalue = bm1.ivalue;
					bm2.ivalue = bm2.ivalue;
					bm3.ivalue = bm3.ivalue;
					bm4.ivalue = bm4.ivalue;

					memset(buff,0,rBUFFERSIZE);
					key = 0;

					//weight_pub.publish(balance);
					v_pub.publish(agv);
					
					int i;
					float v1,v2,v3,v4;
					v1 = (bm1.ivalue-bm1_last.ivalue)*2*PI*RADIUS*RATIO*20;
					v2 = (bm2.ivalue-bm2_last.ivalue)*2*PI*RADIUS*RATIO*20;
					v3 = (bm3.ivalue-bm3_last.ivalue)*2*PI*RADIUS*RATIO*20;
					v4 = (bm4.ivalue-bm4_last.ivalue)*2*PI*RADIUS*RATIO*20;

					bm1_last.ivalue = bm1.ivalue;
					bm2_last.ivalue = bm2.ivalue;
					bm3_last.ivalue = bm3.ivalue;
					bm4_last.ivalue = bm4.ivalue;

					if (abs(v1)>5.0||abs(v2)>5.0||abs(v3)>5.0||abs(v4)>5.0){
						continue;
					}

					 //ROS_INFO("%f %f %f %f",v1,v2,v3,v4);
					// ROS_INFO("%d",bm1.ivalue);

					vx = 0.25*v1+0.25*v2+0.25*v3+0.25*v4;
					vy = -0.25*v1+0.25*v2+0.25*v3-0.25*v4;
					va = (0.923*v1+0.923*v2+0.923*v3+0.923*v4);
					// 0.79064

					// ROS_INFO("%f %f %f",vx,vy,va);

					//计算时间间隔并转化为秒
					current_time=ros::Time::now();
					// dt_Duration=current_time-last_time;
					// last_time=current_time;
					// double dt=dt_Duration.toSec();
					
					dx = vx*0.05;
					dy = vy*0.05;
					dz = va*0.05;

					yaw += dz;
					yaw = (yaw > PI) ? (yaw - 2*PI) : ((yaw < -PI) ? (yaw + 2*PI) : yaw);

					posx += dx*cos(yaw)+dy*sin(yaw);
					posy += -dx*sin(yaw)+dy*cos(yaw);
					
					 //ROS_INFO("%f %f",posx,posy);

					if (v1<=0.001&&v2<=0.001&&v3<=0.001&&v4<=0.001&&dx<=0.001&&dy<=0.001)
					{
						for(int i = 0; i < 36; i++){
							odom.pose.covariance[i] = ODOM_POSE_COVARIANCE2[i];
							odom.twist.covariance[i] = ODOM_TWIST_COVARIANCE2[i];
						}
					} else {
						for(int i = 0; i < 36; i++){
							odom.pose.covariance[i] = ODOM_POSE_COVARIANCE[i];
							odom.twist.covariance[i] = ODOM_TWIST_COVARIANCE[i];
						}
					}

					//将偏航角转换成四元数才能发布
					odom_quat = tf::createQuaternionMsgFromYaw(yaw);
					//发布坐标变换父子坐标系
					#if ENTF
					odom_trans.header.stamp = current_time;
					odom_trans.header.frame_id = "odom";
					odom_trans.child_frame_id = "base_footprint";
					//填充获取的数据
					odom_trans.transform.translation.x = posy; // x坐标
					odom_trans.transform.translation.y = posx; // y坐标
					odom_trans.transform.translation.z = 0;			  // z坐标
					odom_trans.transform.rotation = odom_quat;		  //偏航角
					//发布tf坐标变换
					odom_broadcaster.sendTransform(odom_trans);
					#endif
					//载入里程计时间戳
					odom.header.stamp = current_time;
					//里程计父子坐标系
					odom.header.frame_id = "odom";//wheel_odom
					odom.child_frame_id = "base_footprint";
					//里程计位置数据
					odom.pose.pose.position.x = posy;
					odom.pose.pose.position.y = posx;
					odom.pose.pose.position.z = 0;
					odom.pose.pose.orientation = odom_quat;
					//载入线速度和角速度
					odom.twist.twist.linear.x = vy;
					odom.twist.twist.linear.y = vx;
					odom.twist.twist.angular.z = va;
					//发布里程计消息
					read_pub.publish(odom);
					ROS_INFO("publish odometry\n");
					break;
				}
				}
			}
			memset(r_buffer, 0, rBUFFERSIZE);
		}
		loop_rate.sleep();
		q++;
	}
}

