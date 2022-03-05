import configuration
from migration_RL import MigrationRL
from mig_env import Migration_env


class Migration:
    def __init__(self, actions, tel_info, path, node_info_list, car_start_state, car_end_state, server_start_state,
                 server_end_state, max_hoc, min_hoc, max_dis, min_dis):
        """
        对象参数定义
        :param actions:                 动作列表
        :param tel_info:                基站信息，包括距离，可用容量，传输速度，隐私标记
        :param path:                    车辆轨迹路线，由点构成
        :param node_info_list:          路径节点信息，包含经纬度
        :param car_start_state:         车辆初始位置
        :param car_end_state:           车辆最终目的地
        :param server_start_state:      初始使用的服务器
        :param server_end_state:        最终状态使用的服务器
        :param max_hoc:                 基站最大跳数，计算迁移代价
        :param min_hoc:                 最小跳数
        :param max_dis:                 最大物理距离，计算时延
        :param min_dis:                 最小物理距离
        """
        self.actions = actions
        self.tel_info = tel_info
        self.path = path
        self.node_info_list = node_info_list
        self.car_start_state = car_start_state
        self.car_end_state = car_end_state
        self.server_start_state = server_start_state
        self.server_end_state = server_end_state
        self.max_hoc = max_hoc
        self.min_hoc = min_hoc
        self.max_dis = max_dis
        self.min_dis = min_dis

    def migrate(self):
        # 设置初始基站服务器
        start_state = str(self.car_start_state) + '_' + str(self.server_start_state)
        end_state = str(self.car_end_state) + '_' + str(self.server_end_state)
        # 初始汽车位置和基站选择
        # print("start_state:  "+start_state)
        # print("ending_state:  "+end_state)

        RL = MigrationRL(self.actions, learning_rate=0.95, reward_decay=0.9, e_greedy=0.9)
        # 任务的车辆位置和服务器位置
        task_car_state = self.car_start_state
        task_server_state = self.server_start_state
        # 初始化环境，传入参数
        env = Migration_env(self.tel_info, self.path, self.actions, self.car_start_state, self.car_end_state,
                            self.server_start_state, task_car_state, task_server_state, self.node_info_list,
                            self.max_hoc, self.min_hoc, self.max_dis, self.min_dis)

        # 迭代100轮
        for episode in range(configuration.EPISODE):
            # 待更新状态，分别是下一状态的车辆位置、服务器位置以及当前任务执行的车辆位置和服务器位置
            observation_car = env.start_car_state
            observation_server = env.start_server_state
            observation_task_car = env.task_car_state
            observation_task_server = env.task_server_state
            # 记录上一状态
            prior_car_state = observation_car
            prior_server_state = observation_server
            while True:
                # print(str(observation_car)+'_'+str(observation_server))
                # 根据强化学习获得动作决策迁移与否
                action = RL.choose_action(observation_car, observation_server, env)
                # 更新下一步迁移位置，和任务执行位置，奖励以及完成标志
                observation_car_, observation_server_, observation_task_car_, observation_task_server_, reward, done \
                    = env.step(observation_car, observation_server, prior_car_state, prior_server_state, task_car_state,
                               task_server_state, action)

                q_table = RL.learn(observation_car, observation_car_, observation_server, observation_server_, action,
                                   reward)
                prior_car_state = observation_car
                prior_server_state = observation_server
                observation_car = observation_car_
                observation_server = observation_server_
                if done:
                    break
            print("=======================" + str(self.car_start_state) + '_' + str(self.car_end_state) + "  " +
                  str(episode) + "th Q-table=======================")
            print(q_table)
            print("================================================================")
        q_table.to_csv(configuration.MIGRATION_RESULT_PATH + str(self.car_start_state) + '_'
                       + str(self.car_end_state) + "_q_table.csv", encoding="utf-8")
        return q_table
