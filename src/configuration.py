import os

NODE_INFO = os.path.dirname(os.getcwd()) + "/dataset/node_info.csv"

TEL_INFO = os.path.dirname(os.getcwd()) + "/dataset/tel.csv"

PATH = os.path.dirname(os.getcwd()) + "/dataset/path.txt"

ROAD_TEL = os.path.dirname(os.getcwd()) + "/dataset/road_tel.csv"

RESULT_PATH = os.path.dirname(os.getcwd()) + "/result/"

MIGRATION_RESULT_PATH = RESULT_PATH + "migration_result/"

FINAL_REWARD = 1

REWARD_OMEGA = 0.9

EPISODE = 1000

OMEGA_LIST = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85,
              0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1]
