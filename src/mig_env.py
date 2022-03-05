from haversine import haversine
import numpy as np
import configuration


class Migration_env:
    def __init__(self, tel_info, path, action_list, start_car_state, end_car_state, start_server_state, task_car_state,
                 task_server_state, node_info, max_hoc, min_hoc, max_dis, min_dis):
        """
        对象参数定义
        :param tel_info:                基站信息，包括距离，可用容量，传输速度，隐私标记
        :param path:                    车辆轨迹路线，由点构成
        :param action_list:             动作列表
        :param start_car_state:         车辆初始位置
        :param end_car_state:           车辆最终目的地
        :param start_server_state:      初始使用的服务器
        :param task_car_state:          任务目前所在服务器的车辆位置
        :param task_server_state:       任务目前所在位置的服务器位置
        :param node_info:               路径节点信息，包含经纬度
        :param max_hoc:                 基站最大跳数，计算迁移代价
        :param min_hoc:                 最小跳数
        :param max_dis:                 最大物理距离，计算时延
        :param min_dis:                 最小物理距离
        """
        self.tel_info = tel_info
        self.path = path
        self.action_list = action_list
        self.start_car_state = start_car_state
        self.end_car_state = end_car_state
        self.start_server_state = start_server_state
        self.task_car_state = task_car_state
        self.task_server_state = task_server_state
        self.node_info = node_info
        self.max_hoc = max_hoc
        self.min_hoc = min_hoc
        self.max_dis = max_dis
        self.min_dis = min_dis

    # 返回服务器信息列表,字符串列表
    def get_server_info(self, car_state, server_state):
        server_state_info = []
        for tels in self.tel_info:
            # 如果是当前汽车位置
            if int(tels[0]) == car_state:
                # print(car_state, server_state)
                server_state_info = tels[server_state].strip(' ').strip('[').strip(']').split(',')
                # print(server_state_info)
        return server_state_info

    # 根据当前汽车位置获得下一个位置，返回下一个汽车位置，int类型
    def get_next_car_state(self, car_state):
        next_car_state = 0
        for i in range(len(self.path)):
            # 如果是当前汽车位置
            if int(self.path[i]) == car_state:
                # 获得下一汽车位置
                next_car_state = int(self.path[i + 1])
        return next_car_state

    # 根据动作选择获得下一汽车位置合适的基站信息，返回字符串列表
    def get_next_server_info(self, car_state, index):
        next_car_state = self.get_next_car_state(car_state)
        next_server_info = self.get_server_info(next_car_state, index)
        return next_server_info

    # 获得服务器id，输入为字符串列表，返回int型数值
    def get_server_state(self, car_state, server_state):
        return int(self.get_server_info(car_state, server_state)[0])

    # 获得服务器与车子之间距离，输入为字符串列表，返回int型数值
    def get_distance(self, car_state, server_state):
        # print(car_state, server_state)
        # print(self.get_server_info(car_state, server_state))
        return int(self.get_server_info(car_state, server_state)[1])

    # 获得服务器可用容量，输入为字符串列表，返回int型数值
    def get_available(self, car_state, server_state):
        return int(self.get_server_info(car_state, server_state)[2])

    # 获得服务器网速，输入为字符串列表，返回int型数值
    def get_server_speed(self, car_state, server_state):
        return int(self.get_server_info(car_state, server_state)[3])

    # 获得服务器的隐私标记，0是无隐私冲突，1代表有隐私冲突
    def get_private_flag(self, car_state, server_state):
        return int(self.get_server_info(car_state, server_state)[4])

    # 返回两车之间的距离，单位：米
    def get_geo_distance(self, locA, locB):
        lonA = self.node_info[locA][1]
        latA = self.node_info[locA][2]
        lonB = self.node_info[locB][1]
        latB = self.node_info[locB][2]
        A = (lonA, latA)
        B = (lonB, latB)
        # 计算两点距离，单位：米
        dis = round(haversine(A, B) * 1000, 2)
        return dis

    # 获得迁移代价，模拟网络中的跳数，主要看车子位置隔几个位置
    # 主要顺序，locA是之前位置，locB是当前位置
    def get_migration_cost(self, locA, locB):
        jump = 0
        for node in self.path:
            jump += 1
            if int(node) == locA:
                jump = 0
            if int(node) == locB:
                break
        return jump

    # 此处server_state输入是server_id，而非server信息列表
    def step(self, car_state, server_state, prior_car_state, prior_server_state, task_car_state, task_server_state,
             action):

        # 获得车子的下一个位置
        next_car_state = self.get_next_car_state(car_state)
        mig_cost = float(0)
        private_flag = float(0)
        delay = float(0)
        total_cost = float(0)

        # 进行任务迁移
        if action != 0:
            # 获得待迁移服务器的位置
            next_server_state = action

            # 计算相关指标
            # 获得下一次车子位置与基站之间的距离
            server_dis = self.get_distance(next_car_state, next_server_state)
            # 获得传输速度，范围10~10000 MB/s
            comm_speed = self.get_server_speed(next_car_state, next_server_state)
            # 获得隐私标签
            private_flag = self.get_private_flag(next_car_state, next_server_state)

            # 获得时延，做归一化处理
            max_delay = self.max_dis / 10
            min_delay = self.min_dis / 10000
            delay = server_dis / comm_speed
            normal_delay = delay - min_delay / max_delay - min_delay
            # normal_delay = np.true_divide(delay - min_delay, max_delay-min_delay)

            # 获得迁移代价，跳数，做归一化处理
            mig_cost = self.get_migration_cost(task_car_state, next_car_state)
            max_mig_cost = self.max_hoc
            min_mig_cost = self.min_hoc
            normal_mig_cost = np.true_divide(mig_cost - min_mig_cost, max_mig_cost - min_mig_cost)
            # normal_mig_cost = mig_cost - min_mig_cost/max_mig_cost-min_mig_cost

            # 总cost，在算法中设置为越大越好，时延、迁移代价和隐私的加权和
            total_cost = - configuration.REWARD_OMEGA * normal_mig_cost - (
                        1 - configuration.REWARD_OMEGA) * normal_delay \
                         - float(100 * private_flag)
            # 将任务迁移位置更新,同时更新车辆位置和服务器位置
            task_car_state = next_car_state
            task_server_state = next_server_state
            # print(car_state, task_car_state, next_car_state)
            # print(mig_cost, delay)
        # 不进行任务迁移
        else:
            next_server_state = 0
            # 不进行迁移时，任务的车辆位置和服务器位置不变
            task_car_state = task_car_state
            task_server_state = task_server_state

            # 计算相关指标
            # 获得下个位置车子与上一次卸载时车子位置之间的距离
            car_dis = self.get_geo_distance(next_car_state, int(task_car_state))
            # 获得传输速度
            comm_speed = self.get_server_speed(task_car_state, task_server_state)
            # 设置迁移代价和隐私标签
            mig_cost = 0
            private_flag = 0
            # 获得时延，做归一化处理
            max_delay = self.max_dis / 10
            min_delay = self.min_dis / 10000
            delay = car_dis / comm_speed
            normal_delay = delay - min_delay / max_delay - min_delay
            # 计算通信延迟

            # 总cost，在算法中设置为越大越好，时延、迁移代价和隐私的加权和
            total_cost = configuration.REWARD_OMEGA * mig_cost - (1 - configuration.REWARD_OMEGA) * normal_delay - 100 \
                         * private_flag

        if next_car_state == self.end_car_state:
            reward = configuration.FINAL_REWARD
            done = True
            next_car_state = "ending"
            next_server_state = "ending"
            # print("over")
        else:
            reward = total_cost
            done = False
        return next_car_state, next_server_state, task_car_state, task_server_state, reward, done
