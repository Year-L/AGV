#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
import random

import rospy
# from std_msgs import Int16MultiArray

def pso(order_st,order_ed):
    max_iter = 100
    c1 = 1.5
    c2 = 1.5
    alpha = 0.3
    beta = 0.1
    w = 0.9
    N_p = 30  # 种群数量为20
    time_iter = np.zeros([max_iter]) # 记录每一轮的最优解
    K = 10 # the number of orders = 10
    # 设置四个工位的起始点和终止点坐标
    st_loc = np.array([[5.08,2.5],[5.08,-2.5], [20.32,2.5], [20.32,-2.5]])
    ed_loc = np.array([[10.16,2.5],[10.16,-2.5],[15.24,2.5],[15.24,-2.5]])
    st_sites = st_loc.shape[0]
    ed_sites = ed_loc.shape[0]
    init_loc = np.array([7.62,5.9]) # AGV的初始位置
    def distance_compute(st, ed):
        return np.sqrt(np.sum(np.square(ed - st)))

    x = np.array(range(K))
    random.shuffle(x)

    def initial(order_st,order_ed):

        """ plt.scatter(st_loc[:,0], st_loc[:,1], c='r') # 红色为起点
        plt.scatter(ed_loc[:,0], ed_loc[:,1], c='b') # 蓝色为终点
        plt.show() """
        # Generating orders 生成订单
        """ a = input("订单任务起始点").split()
        order_st = [int(a[i]) for i in range(len(a))]
        order_st = np.array([order_st])
        b = input("订单任务终止点").split()
        order_ed = [int(b[i]) for i in range(len(a))]
        order_ed = np.array([order_ed]) """
        order_st_ed = np.concatenate([order_st, order_ed])
        return order_st_ed
    def regularize(prob):
    # 将一群prob用softmax修复至概率归一化的形式，可以写循环，但以下是用矩阵进行的向量化操作，效率更高
        y =  np.exp(prob - np.expand_dims(np.max(prob, axis=2), axis=2))
        f_x = y/np.expand_dims(np.sum(y, axis=2), axis=2)
        return f_x

    def solu_decode(prob):
        N, K, _ = prob.shape
        p_new = np.zeros([N, K])
        # 首先对N个解做循环
        for i in range(N):
            # 按照订单执行顺序做循环
            for j in range(K):
                p_new[i, j] = np.where(prob[i, j, :] == np.max(prob[i, j, :]))[0][0]  # 将概率结果转化为可匹配出来的结果
            # p_new即为解码结果，每步选取的订单为当步概率最大的订单
            # 下面做解的合规性检验，如果对解码结果从小到大排序和[0, ..., 9]不一样，即出现重复元素
            if np.sum(np.abs(np.sort(p_new[i, :]) - np.array(range(K)))) != 0:  # 如果非0说明解有问题，需要修正解
                duplicate = np.array([])  # 被选种多次的任务
                excluded = np.array([])  # 没有被选中的任务
                for j in range(K):
                    # 对这组解从0到9挨个找它们出现的位置
                    index = np.where(p_new[i, :]==j)[0] # 
                    if index.size==0:  # 如果某个数字没出现过，则在excluded中记录
                        excluded = np.append(excluded, [j])
                    if index.size > 1:  # 如果有重复，则随机从中选出重复需要矫正的点位
                        select_loc = np.array(range(index.size))
                        random.shuffle(select_loc)
                        select_loc = select_loc[:(index.size-1)]
                        duplicate = np.append(duplicate, index[select_loc])
                random.shuffle(excluded) 
                excluded = excluded.astype(np.int64)
                p_new[i, duplicate.astype(np.int64)] = excluded # 将重复的那些位置分别替换为没出现过的元素
        return p_new

    def prob_compute(p_all, N_p, K):
        prob = np.zeros([N_p, K, K])  # prob应该对每个解是个K*K的矩阵，所以对全部解就是N_p*K*K 的矩阵
        for i in range(N_p):
            for j in range(K):
                prob[i, j, p_all[i, j]] = 1
        return prob

    def all_agv_time(p_all, order_st_ed, init_loc, st_loc, ed_loc):
        # 在给定一组解的时候，计算每个解的总时间及时间节点
        t = np.zeros([p_all.shape[0]]) # 记录每个解所得的最长时间
        N_task = p_all.shape[1]   
        timestamp_start_all = np.zeros(p_all.shape)
        timestamp_finish_all = np.zeros(p_all.shape)
        # 计算一组解的时间
        for i in range(p_all.shape[0]):
            t_tmp, timestamps = single_agv_time(p_all[i,:], order_st_ed, init_loc, st_loc, ed_loc)
            t[i] = t_tmp
            timestamp_start_all[i, :] = timestamps[0]
            timestamp_finish_all[i, :] = timestamps[1]
        return t, [timestamp_start_all, timestamp_finish_all]
    def single_agv_time(x, order_st_ed, init_loc, st_loc, ed_loc):
        order_content = order_st_ed[:, x]
        N_task = order_content.shape[1]
        t = 0
        timestamp_start = np.zeros([N_task])
        timestamp_finish = np.zeros([N_task])
        for j in range(N_task):
            if j==0:
                dist_single = distance_compute(init_loc, st_loc[order_content[0, j], :])  # 初始位置去第一个任务起点
            else:
                dist_single = distance_compute(ed_loc[order_content[1, j-1]  ,:], st_loc[order_content[0, j], :])  # 上一个任务终点去下一个起点
            t = t + dist_single
            timestamp_start[j] = t

            dist_single = distance_compute(st_loc[order_content[0, j], :], ed_loc[order_content[1, j], :])  # 起点去终点
            t = t + dist_single
            timestamp_finish[j] = t
        return t, [timestamp_start, timestamp_finish]




    order_st_ed = initial(order_st,order_ed)
    p_all = np.random.rand(N_p, K).argsort(axis=1)
    prob = prob_compute(p_all, N_p, K)
    for i in range(max_iter):
        if i == 0:
            v = np.random.rand(*prob.shape)/5 - 0.1  # 初始化速度，设为-0.05~0.05之间的值
            prob = regularize(prob+v) # x <- x + v 的更新方法，但需要保证概率解的归一化性质
            p_all = solu_decode(prob).astype(np.int64)   # 从概率的形式里解码出一组解，将解转化为整数型数组
            t_all, _ =  all_agv_time(p_all, order_st_ed, init_loc, st_loc, ed_loc) 
            
            # 以下进行全局最优和个体最优的计算与记录
            fitness_value = 1/t_all # 适应度函数，如果是第一轮则直接计算，时间越长则适应度越小所以取了倒数
            local_f = fitness_value # 初始化各粒子历史最优解的适应度值
            local_prob = prob  # 初始化各粒子历史最优解
            glob_f = np.max(local_f)  # 初始化全局最优解的适应度值
            glob_index = np.where(glob_f == local_f)[0][0]  # 找到哪个解是全局最优解
            glob_prob = prob[glob_index, :, :]  # 记录全局最优解
            glob_p = p_all[glob_index, :]  # 解码全局最优解
        else:
            v = w*v + c1*alpha*(local_prob - prob) + c2*beta*(glob_prob-prob) # 更新速度
            prob = regularize(prob+v)
            p_all = solu_decode(prob).astype(np.int64)        
            t_all, _ =  all_agv_time(p_all, order_st_ed, init_loc, st_loc, ed_loc)
            # print(p_all[0, :])
            
            fitness_value = 1/t_all
            this_local_f = fitness_value
            update_index = np.where(this_local_f >= local_f)[0]  # 找到这一轮里面各粒子适应度值优于其之前的解
            local_f[update_index] = this_local_f[update_index] # 更新各粒子历史最优适应度值
            local_prob[update_index, :, :] = prob[update_index, :, :]  # 更新各粒子历史最优解
            this_glob_f = np.max(local_f)  # 找出当前这轮解的最佳适应度值
            
            if this_glob_f > glob_f:  # 如果当前最优解好过全局历史最优解
                glob_f = this_glob_f   # 更新历史全局最优适应度值
                glob_index = np.where(local_f == this_glob_f)[0][0]  # 找出新的全局最优解
                glob_prob = prob[glob_index, :, :]  # 更新全局历史最优的概率解
                glob_p = p_all[glob_index, :]  # 更新全局历史最优解
        time_iter[i] = 1/glob_f
        result_convert = order_st_ed[:,glob_p]
        result = np.zeros((20,),dtype=int)
        m = 0 
        for j in range(result_convert.shape[1]):
            for i in range(result_convert.shape[0]):
                if i == 1:
                    result[m] = result_convert[i,j]+4
                else:
                    result[m] = result_convert[i,j]
                m = m+1
    return glob_p,result

order_st = [[0,1,2,0,3,0,2,0,2,1]]
order_ed = [[3,2,1,2,1,0,2,3,1,1]]

glob_p,result = pso(order_st,order_ed)
# print(glob_p)
# print(result)
        














