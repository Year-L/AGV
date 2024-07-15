#!/usr/bin/env python3
# coding:utf-8
import serial
import cv2
import pyzbar.pyzbar as pyzbar
from time import sleep
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
        print("发送成功", send_data_hex)
    else:
        print("发送失败！")


if __name__ == '__main__':
    serial = serial.Serial('/dev/jxb', 115200, timeout=0.5)
    if serial.isOpen():
        print("open success")
    else:
        print("open failed")

    # 打开摄像头
    camera = cv2.VideoCapture(0)

    while True:
        # 读取摄像头帧
        ret, frame = camera.read()

        # 检测二维码
        barcodes = pyzbar.decode(frame)

        # 显示检测结果
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            print("二维码内容:", barcode_data)

            # 发送二维码内容给STM32芯片
            send(barcode_data)
            sleep(0.5)  # 起到一个延时的效果
            data = recv(serial)
            if data != '':
                print("接收到的回复消息:", data)
                if data == 'x':
                    print("exit")
                    break

        # 显示摄像头画面
        cv2.imshow("Camera", frame)

        # 按下 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头和关闭串口
    camera.release()
    cv2.destroyAllWindows()
