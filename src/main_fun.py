import pandas as pd
import configuration

from service_migration import Migration

from warnings import simplefilter

simplefilter(action="ignore", category=FutureWarning)

ACTIONS = [0, 1, 2, 3, 4]

if __name__ == "__main__":

    error_list = [512, 609, 162, 5, 778, 428, 306, 626, 345, 380]

    node_info_list = pd.read_csv(configuration.NODE_INFO, encoding='utf-8').values.tolist()

    # 基站信息
    tel_info = pd.read_csv(configuration.TEL_INFO, encoding='utf-8', header=None).values.tolist()
    # 路线信息
    paths = []
    with open(configuration.PATH, 'r') as f:
        for line in f:
            paths.append(list(line.strip('\n').strip('[').strip(']').split(',')))

    node_tel = pd.read_csv(configuration.ROAD_TEL, encoding='utf-8', header=None).values.tolist()


    # TODO Loop paths
    mg = Migration(ACTIONS, tel_info, paths[0], node_info_list, int(node_tel[0][0]), int(node_tel[0][1]), int(node_tel[0][2]),
                   int(node_tel[0][3]), node_tel[0][4], node_tel[0][5], node_tel[0][6], node_tel[0][7])
    q_table = Migration.migrate(mg)


