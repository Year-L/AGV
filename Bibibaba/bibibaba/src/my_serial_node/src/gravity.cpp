#include <ros/ros.h>
#include <serial/serial.h>
#include <std_msgs/String.h>
#include <std_msgs/Empty.h>
#include <my_serial_node/Balance.h>

#define sBUFFERSIZE 10				 // send buffer size 串口发送缓存长度
#define rBUFFERSIZE 20				 // receive buffer size 串口接收缓存长度

unsigned char s_buffer[sBUFFERSIZE]; //发送缓存
unsigned char r_buffer[10000]; //接收缓存
uint8_t buff[rBUFFERSIZE]; //接收缓存，用于数据对齐
uint8_t key = 0;

serial::Serial ser;

// ros:Publisher g_pub;

//接收数据分析与校验0
unsigned char data_analysis(unsigned char *buffer)
{
	unsigned char ret = 0, csum;
	// int i;
	if ((buffer[0] == 0xff) && (buffer[1] == 0xff))
	{
		csum = buffer[0] ^ buffer[1] ^ buffer[2] ^ buffer[3] ^ buffer[4] ^ buffer[5] ^
			   buffer[6] ^ buffer[7] ^ buffer[8] ^ buffer[9] ^ buffer[10] ^ buffer[11] ^
			   buffer[12] ^ buffer[13] ^ buffer[14] ^ buffer[15] ^ buffer[16] ^ buffer[17] ^
			   buffer[18];
		// ROS_INFO("check sum:0x%02x",csum);
		if (csum == buffer[19])
		{
			ret = 1; //校验通过，数据包正确
		}
		else
			ret = 0; //校验失败，丢弃数据包
	}
	
	// for(int i=0;i<rBUFFERSIZE;i++)
	//   ROS_INFO("0x%02x",buffer[i]);
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
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "my_serial_node");
	ros::NodeHandle nh;
    //  ros::Publisher g_pub = nh.advertise<>("gravity",1000);
    
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
		ROS_INFO_STREAM("Serial gravity Port initialized");
	}
	else
	{
		return -1;
	}
	s_buffer[0] = 0xff;
	s_buffer[1] = 0xff;
	s_buffer[2] = 0x09;
	s_buffer[5] = 0x00;
	s_buffer[6] = 0x00;
	s_buffer[3] = 0x00;
	s_buffer[4] = 0x00;
	s_buffer[7] = 0x00;
	s_buffer[8] = 0x00;
	s_buffer[9] = 0x09;
	while (ros::ok())
	{
		ser.write(s_buffer, sBUFFERSIZE);
		sleep(1);
	}
	
}
