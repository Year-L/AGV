#!/usr/bin/env python3
# coding:utf-8
import numpy as np
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
lower_red = np.array([0, 150, 150])
higher_red = np.array([10, 255, 255])
lower_green = np.array([35, 110, 106])  # 绿色阈值下界
higher_green = np.array([77, 255, 255])  # 绿色阈值上界
lower_black = np.array([0, 0, 0])
higher_black = np.array([25, 35, 46])
lower_blue = np.array([110, 100, 100])
higher_blue = np.array([130, 255, 255])
lower_white = np.array([0, 0, 221])
higher_white = np.array([180, 30, 255])
cap = cv2.VideoCapture(0)  # 打开电脑内置摄像头
red,green,black,blue,white = 0,0,0,0,0

if cap.isOpened():
    while 1:
        ret, frame = cap.read()  # 按帧读取，这是读取一帧
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_red = cv2.inRange(img_hsv, lower_red, higher_red)  # 可以认为是过滤出红色部分，获得红色的掩膜,去掉背景
        mask_red = cv2.medianBlur(mask_red, 7)  # 中值滤波(把数字图像中的一点的值用该点的邻域各点的中值代替，让 周围像素值接近真实值，从而消除孤立的噪声点)
        mask_green = cv2.inRange(img_hsv, lower_green, higher_green)  # 获得绿色部分掩膜
        mask_green = cv2.medianBlur(mask_green, 7)  # 中值滤波
        mask_black = cv2.inRange(img_hsv, lower_black, higher_black)  # 获得绿色部分掩膜
        mask_black = cv2.medianBlur(mask_black, 7)  # 中值滤波
        mask_blue = cv2.inRange(img_hsv, lower_blue, higher_blue)  # 获得绿色部分掩膜
        mask_blue = cv2.medianBlur(mask_blue, 7)
        mask_white = cv2.inRange(img_hsv, lower_white, higher_white)  # 获得绿色部分掩膜
        mask_white = cv2.medianBlur(mask_white, 7)

        # mask = cv2.bitwise_or(mask_red, mask_red)  # 三部分掩膜进行按位或运算

        cnts1, hierarchy1 = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 轮廓检测
        cnts2, hierarchy2 = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts3, hierarchy3 = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts4, hierarchy4 = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts5, hierarchy5 = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in cnts1:
            (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
            cv2.rectangle(frame, (x, y - 20), (x + w, y + h), (0, 0, 255), 2)  # 将检测到的颜色框起来
            cv2.putText(frame, 'red', (x, y - 20), font, 0.7, (0, 0, 255), 2)
            red =1

        for cnt in cnts2:
            (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)  # 将检测到的颜色框起来
            cv2.putText(frame, 'black', (x, y - 1), font, 0.7, (0, 0, 0), 2)
            black = 1

        for cnt in cnts3:
            (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
            cv2.rectangle(frame, (x, y - 50), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的颜色框起来
            cv2.putText(frame, 'green', (x, y - 50), font, 0.7, (0, 255, 0), 2)
            green = 1

        for cnt in cnts4:
            (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
            cv2.rectangle(frame, (x, y - 30), (x + w, y + h), (255, 0, 0), 2)  # 将检测到的颜色框起来
            cv2.putText(frame, 'blue', (x, y - 30), font, 0.7, (255, 0, 0), 2)
            blue = 1

        for cnt in cnts5:
            (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
            cv2.rectangle(frame, (x, y - 30), (x + w, y + h), (255, 255, 255), 2)  # 将检测到的颜色框起来
            cv2.putText(frame, 'white', (x, y - 30), font, 0.7, (255, 255, 255), 2)
            white = 1

        cv2.imshow('frame', frame)
        k = cv2.waitKey(20) & 0xFF  # 引用&0xff，为了只取按键对应的ASCII值后8位来排除不同按键的干扰进行判断按键是什么

        if k == 27:
            break
print(red,white)
cv2.waitKey(0)  # time.sleep()
cv2.destroyAllWindows()
