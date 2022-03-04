import pandas as pd
import numpy as np


class MigrationRL:
    def __init__(self, actions, learning_rate, reward_decay, e_greedy):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.q_table_index = []

    # 此处car_state和server_state都是id,而非列表
    def choose_action(self, car_state, server_state, env):

        # 检查当前state是否存在于Q表
        self.check_state_exist(car_state, server_state)

        state = str(car_state)+'_'+str(server_state)
        # 当随机数小于epsilon时按Q表最大值执行，其他情况随机执行
        if np.random.uniform() < self.epsilon:
            q_t = self.q_table
            state_action = self.q_table.loc[state, self.actions]
            # 获得所选action的index
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
            index = self.actions.index(action)
        else:
            action = np.random.choice(self.actions)
            index = self.actions.index(action)
        return index

    def learn(self, car_state, next_car_state, server_state, next_server_state, index, reward):

        current_state = str(car_state)+'_'+str(server_state)
        next_state = str(next_car_state)+'_'+str(next_server_state)

        self.check_state_exist(next_car_state, next_server_state)
        q_predict = self.q_table.loc[current_state, self.actions[index]]
        if next_state != 'ending_ending':
            q_target = reward + self.gamma * self.q_table.loc[next_state, :].max()
        else:
            q_target = reward
        self.q_table.loc[current_state, self.actions[index]] += self.lr * (q_target - q_predict)
        return self.q_table

    # 检查当前state是否存在于Q表
    def check_state_exist(self, car_state, server_state):
        state = str(car_state)+'_'+str(server_state)
        if state not in self.q_table_index:
            self.q_table_index.append(state)
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state
                )
            )
