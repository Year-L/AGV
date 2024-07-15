#!/usr/bin/env python3
# coding:utf-8

import serial
import paho.mqtt.client as mqtt
from time import sleep

# 初始化串口
serial_port = '/dev/jxb'
baud_rate = 115200

def recv(serial):
    while True:
        data = serial.read_all().hex()
        if data == '':
            continue
        else:
            break
        sleep(0.02)
    return data

def send(send_data):
    send_data_hex = bytes.fromhex(send_data)
    if serial.isOpen():
        serial.write(send_data_hex)  # 编码
        print("send success!", send_data_hex)
    else:
        print("send failed！")

# MQTT 回调函数
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/qr_codes")

def on_message(client, userdata, msg):
    barcode_data = msg.payload.decode("utf-8")
    print("二维码内容:", barcode_data)

    # 发送二维码内容给STM32芯片
    send(barcode_data)
    sleep(0.5)  # 起到一个延时的效果
    data = recv(serial)
    if data != '':
        print("接收到的回复消息:", data)
        print("receive success！")
        if data == 'x':
            print("exit")
            client.disconnect()

if __name__ == '__main__':
    # 初始化串口
    serial = serial.Serial(serial_port, baud_rate, timeout=0.5)
    if serial.isOpen():
        print("open success")
    else:
        print("open failed")

    # 初始化MQTT客户端
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # 连接MQTT服务器（请根据您的MQTT服务器地址进行修改）
    client.connect("mqtt_server_address", 1883, 60)

    # 阻塞运行，等待消息
    client.loop_forever()
