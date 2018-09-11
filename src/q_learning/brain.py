#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import numpy as np
import pandas as pd

from src.poker import Card


def cards_string(cards):
    return ','.join([str(c.rank) for c in cards])


class RL(object):
    def __init__(self, action_space, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = [cards_string(cards) for cards in action_space] + ['']  # a list
        self.actions = list(set(self.actions))
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy

        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def choose_action(self, observation, ai_player):
        self.check_state_exist(observation.state)
        # possible actions
        possible_actions = ai_player.possibilities(observation.desk_pool)
        possible_actions_string = [cards_string(c) for c in possible_actions]
        # action selection
        if np.random.rand() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation.state, :]
            # some actions may have the same value, randomly choose on in these actions
            # if no available actions, then pick the second highest values and so on..
            state_values = list(set(state_action.values))
            state_values.sort(reverse=True)
            for value in state_values:
                available_actions = list(set((state_action[state_action == value].index)).intersection(
                    set(possible_actions_string)))
                if available_actions:
                    action = random.choice(available_actions)
                    break
            else:
                action = ''
        else:
            # choose random action
            if possible_actions_string:
                action = random.choice(possible_actions_string)
            else:
                action = ''
        ai_player.choose_next_action(action)
        return action

    def learn(self, *args):
        pass


# off-policy
class QLearningTable(RL):
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        """
        :param actions: A list of `action`, `action` could be a string or anything that can be used as a dict key
        :param learning_rate:
        :param reward_decay:
        :param e_greedy:
        """
        super(QLearningTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        # if s_ != 'terminal':
        if r == 0:
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update


# on-policy
class SarsaTable(RL):

    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        super(SarsaTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, a_]  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update
