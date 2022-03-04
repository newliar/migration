import os
import pandas as pd
import configuration

car_paths = []
with open(configuration.PATH, 'r') as f:
    for line in f:
        car_paths.append(list(line.strip('\n').strip('[').strip(']').split(',')))


node_tel = pd.read_csv(configuration.NODE_INFO, encoding="utf-8").values.tolist()
migration_file = pd.read_csv(configuration.MIGRATION_RESULT_PATH+"/725_1056_q_table.csv", index_col=0, encoding="utf-8")
car_path = car_paths[0]

server_state = 1
next_server_state = server_state

car_ending = 1056

count = 0
for node in car_path:
    if int(node) == car_ending:
        break
    car_state = node.strip(' ')
    server_state = next_server_state
    state = car_state+'_'+str(server_state)
    action_list = migration_file.loc[state]
    print(action_list.astype(float))
    action = action_list.astype(float).idxmax()
    if int(action) == 0:
        print(car_state, "迁移策略： 不迁移")
    else:
        count += 1
        print(car_state, "迁移策略：", action)
    next_server_state = action
print("迁移次数：", count)


