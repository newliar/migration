import os
import pandas as pd
import configuration

# car_paths = []
# with open(configuration.PATH, 'r') as f:
#     for line in f:
#         car_paths.append(list(line.strip('\n').strip('[').strip(']').split(',')))
# 路线信息
paths = []
with open(configuration.PATH, 'r') as f:
    for line in f:
        paths.append(list(line.strip('\n').strip('[').strip(']').split(',')))

node_tel = pd.read_csv(configuration.ROAD_TEL, encoding="utf-8", header=None).values.tolist()

for i in range(len(paths)):
    car_start_state = int(node_tel[i][0])
    car_end_state = int(node_tel[i][1])
    server_start_state = int(node_tel[i][2])
    # print(car_start_state, car_end_state)
    migration_file = pd.read_csv(configuration.MIGRATION_RESULT_PATH + str(car_start_state)+'_'+str(car_end_state) +
                                 "_q_table.csv", index_col=0, encoding="utf-8")
    path = paths[i]

    next_server_state = server_start_state

    mig_count = 0
    no_mig_count = 0
    for node in path:
        if int(node) == car_end_state:
            break
        car_state = node.strip(' ')
        server_state = next_server_state
        state = car_state + '_' + str(server_state)
        action_list = migration_file.loc[state]
        # print(action_list.astype(float))
        action = action_list.astype(float).idxmax()
        if int(action) != 0:

            mig_count += 1
        #     print(car_state, "迁移策略： 不迁移")
        else:
            no_mig_count += 1
        #     print(car_state, "迁移策略：", action)
        # next_server_state = action
    print(car_start_state, '_', car_end_state, "迁移次数：", mig_count)
    print(car_start_state, '_', car_end_state, "不迁移次数：", no_mig_count, '\n')


