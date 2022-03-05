import pandas as pd
import configuration
import csv
from haversine import haversine

tel_info = pd.read_csv(configuration.TEL_INFO, encoding='utf-8').values.tolist()
node_info_list = pd.read_csv(configuration.NODE_INFO, encoding='utf-8').values.tolist()
with open(configuration.PATH, 'r') as f:
    write_f = open(configuration.ROAD_TEL, 'w')
    writer = csv.writer(write_f)
    for line in f:
        path = line.strip('\n').strip('[').strip(']').strip(' ').split(',')
        server_start_state = 0
        server_end_state = 0
        for tels in tel_info:
            if tels[0] == int(path[0]):
                dis = 100000
                for j in range(1, 5):
                    # 获得距离最短的基站
                    tel = tels[j].strip(' ').strip('[').strip(']').split(',')
                    if int(tel[1]) < dis:
                        dis = int(tel[1])
                        server_start_state = int(tel[0])
            elif tels[0] == int(path[len(path) - 1]):
                dis = 100000
                for j in range(1, 5):
                    # 获得距离最短的基站
                    tel = tels[j].strip(' ').strip('[').strip(']').split(',')
                    if int(tel[1]) < dis:
                        dis = int(tel[1])
                        server_end_state = int(tel[0])
        # 最大跳数 最小跳数
        max_hoc = len(path)
        min_hoc = 0
        # 最大物理距离 最小物理距离
        # lonA = node_info_list[int(path[0])][1]
        # latA = node_info_list[int(path[0])][2]
        # latA = node_info_list[int(c)][2]
        # lonB = node_info_list[int(path[len(path)-1])][1]
        # latB = node_info_list[int(path[len(path)-1])][2]
        max_dis = round(haversine((node_info_list[int(path[0])][1], node_info_list[int(path[0])][2]),
                        (node_info_list[int(path[len(path)-1])][1], node_info_list[int(path[len(path)-1])][2]))*1000, 2)
        min_dis = 99999
        for i in range(len(path)-2):
            temp_dis = round(haversine((node_info_list[int(path[i])][1], node_info_list[int(path[i])][2]),
                                   (node_info_list[int(path[i+1])][1], node_info_list[int(path[i+1])][2]))*1000, 2)
            if min_dis > temp_dis:
                min_dis = temp_dis

        temp = [int(path[0]), int(path[len(path) - 1]), server_start_state+1, server_end_state+1, max_hoc, min_hoc,
                max_dis, min_dis]
        writer.writerow(temp)
        print(temp)
    write_f.close()
f.close()
