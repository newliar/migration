import csv
import random
import os
import configuration

import pandas as pd

tel = []

paths = []
with open(configuration.PATH, 'r') as f:
    for line in f:
        paths.append(list(line.strip('\n').strip('[').strip(']').split(',')))

node_info_list = pd.read_csv(configuration.NODE_INFO, encoding='utf-8').values.tolist()

node_list = []
tel_list = []
for path in paths:
    for node in path:
        if int(node) in node_list:
            continue
        else:
            node_list.append(int(node))
            tels = []
            tel = []
            temp = [int(node)]
            for i in range(4):
                # 服务器id
                id = i
                # 距离
                dis = random.randint(50, 300)
                # 可用容量
                available = random.randint(0, 100)
                # 传输速度
                speed = random.randint(10, 10000)
                # 隐私标记
                private = 1 if random.randint(1, 100) % 100 == 1 else 0
                tel = [id, dis, available, speed, private]
                temp.append(tel)

        tel_list.append(temp)

f = open(configuration.TEL_INFO, 'w')
writer = csv.writer(f)
for i in tel_list:
    writer.writerow(i)
f.close()

for ele in tel_list:
    print(ele)
