#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from src.poker import Card
from src.q_learning.brain import QLearningTable
from src.rule.landlord import Game, Player, AIPlayer


def train():
    ai_player = AIPlayer([Card('2s'), Card('3d'), Card('3h'), Card('3c')])
    players = OrderedDict({
        'player1': ai_player,
        'player2': Player([Card('As'), Card('2d'), Card('5h')]),
        'player3': Player([Card('Ks'), Card('6d'), Card('6h')]),
    })
    RL = QLearningTable(actions=ai_player.possibilities([]))
    for episode in range(100):
        # initial observation
        observation = Game(players)

        # RL choose action based on game history and cards on desk
        action = RL.choose_action(observation)

        game_progress = observation.start(step_by_step=True)
        previous_state = observation.state

        for player_name, choice in game_progress:
            if observation.winner is None:
                reward = 0
            else:
                if observation.winner == 'player1':
                    reward = 1
                else:
                    reward = -1
            # RL choose action based on next observation
            action_ = RL.choose_action(observation)

            # RL learn from this transition (s, a, r, s, a) ==> Sarsa
            RL.learn(previous_state, action, reward, observation.state, action_)

            # swap observation and action
            previous_state = observation.state
            action = action_

    # end of game
    print('game over')


if __name__ == "__main__":
    train()