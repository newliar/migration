import os

NODE_INFO = os.path.dirname(os.getcwd()) + "/dataset/node_info.csv"

TEL_INFO = os.path.dirname(os.getcwd()) + "/dataset/tel.csv"

PATH = os.path.dirname(os.getcwd()) + "/dataset/path.txt"

ROAD_TEL = os.path.dirname(os.getcwd()) + "/dataset/road_tel.csv"

RESULT_PATH = os.path.dirname(os.getcwd()) + "/result/"

MIGRATION_RESULT_PATH = RESULT_PATH + "migration_result/"

FINAL_REWARD = 1

REWARD_OMEGA = 0.2

EPISODE = 1000
