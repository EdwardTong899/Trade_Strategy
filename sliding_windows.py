# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:39:23 2023

@author: GTong
"""
import numpy as np
import pandas as pd
csv_file_path = 'bidask.txt'
data = pd.read_csv(csv_file_path)


data_time = []
bid_price = []
ask_price = []
trade_price = []
_1min_k = []

# 取出 time, ask_price, bid_price
data_time = []
data = pd.read_csv(csv_file_path)
data_time = data.iloc[:, 2].tolist()
bid_price = data.iloc[:, 5].tolist()
ask_price = data.iloc[:, 8].tolist()

# 將ask_price bid_price的最小值相加/2模擬成交價格
for i in range(len(bid_price)):
    bid_str = bid_price[i]
    ask_str = ask_price[i]
    bid_str = bid_str.strip("{}").split(",")
    ask_str = ask_str.strip("{}").split(",")
    price = (int(bid_str[0]) + int(ask_str[0])) / 2
    price = trade_price[-1] if (price  == 0.0) else trade_price.append(price)
    # trade_price.append((int(bid_str[0]) + int(ask_str[0])) / 2)


print(data_time[0][17:21])

# 計算分鐘K (一分鐘內最大值與最小值) 使用trade_price換算
def cac_Kline():
    Kmax = 0
    Kmin = 100000
    Kline_close_time = ''    
    for i  in range(len(trade_price)):
        if(i == 0):
            print("Start creat 1 min kline")
            print("First time at: "+str(data_time[0][0:16]))
            Kline_close_time = data_time[0][0:16]
        
        elif(Kline_close_time != data_time[i][0:16]):
            k_data = []
            k_data.append(Kline_close_time)
            k_data.append(Kmax)
            k_data.append(Kmin)
            _1min_k.append(k_data)
            Kmax = 0
            Kmin = 100000
            
        Kmax = max(Kmax,trade_price[i])
        Kmin = min(Kmin,trade_price[i])
        Kline_close_time = data_time[i][0:16]
        
    # print(_1min_k)
    # print(data_time)

def trade_index(times):  #輸入目前時間，回傳做多 or 做空
    k1 = []
    k2 = []
    window_dir = 0 # k棒趨勢
    index = 2  # 回傳交易方向 0:做空、1:做多
    upper = 0
    lower = 0
    now_price = trade_price[times]
    for i in range(len(_1min_k)):
        if(data_time[times][0:16] == _1min_k[i][0]): #找到前2mins Kline
            k1 = _1min_k[i-2]
            k2 = _1min_k[i-1]
            if(k2[1] > k1[1] and k2[2] > k1[2]):     # K2最大值大於K1，K2最小值大於K2 (Kline higher hight)上升趨勢
                window_dir = 1 #做多，先買後賣
                upper = (k2[1] - k1[1]) / 600 * float(data_time[times][17:21])*10 + k2[1] 
                lower = (k2[2] - k1[2]) / 600 * float(data_time[times][17:21])*10 + k2[1] 
            elif(k2[1] < k1[1] and k2[2] < k1[2]):   # K2最大值小於K1，K2最小值小於K2 (Kline lower to low)下降趨勢
                window_dir = 0 #做空，先買後賣
                upper = (k2[1] - k1[1]) / 600 * float(data_time[times][17:21])*10 + k2[1] 
                lower = (k2[2] - k1[2]) / 600 * float(data_time[times][17:21])*10 + k2[1]
            
            break 
    if(now_price < lower and window_dir == 1): # 上升趨勢，但價格跌破低點
        # print("做多")
        index = 1
    elif(now_price > upper and window_dir == 0): # 下降趨勢，但價格漲過高點
        # print("做空")
        index = -1
        
    return 2 if(k1 == [] or k2 == []) else index # 回傳交易方向

def backtrace():
    cac_Kline()
    profit = 0
    direction = 1 # -1:作空 1:作多
    open_position_price = 0
    trade_time = 0
    lisa = []
    for times in range(len(trade_price)):
    # for times in range(0,20000):
        now_price = trade_price[times] # 目前價格
        index = trade_index(times) # 回傳交易方向
        lisa.append(index)
        if(open_position_price != 0): # 有開倉
            temp_profit = (now_price - open_position_price) * direction
            if(temp_profit > 12): # 停利
                profit += temp_profit
                open_position_price = 0
                print(profit)
                print(now_price)
                print(data_time[times])
            elif(temp_profit < -20): # 停損
                profit += temp_profit
                open_position_price = 0
                print(profit)
                print(now_price)
                print(data_time[times])
        else:
            if(index == 2):
                continue
            else:
                direction = index
                open_position_price = now_price
                trade_time += 1
    # print(lisa)
    # print(profit)

    print("start date: "+str(data_time[0]))
    print("end date: "+str(data_time[-1]))
    print("開倉次數: "+str(trade_time))
    print("獲利: "+str(profit))











