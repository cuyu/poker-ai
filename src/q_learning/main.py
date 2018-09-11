#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from src.poker import Card
from src.q_learning.brain import QLearningTable
from src.rule.landlord import Game, Player, AIPlayer


def train(players, desk_pool, rounds=100, replay_game=True):
    """
    :param players: A OrderedDict of players, the first player should be <AIPlayer>
    :param desk_pool: A list of <Card>
    :param rounds: How many rounds of games for training
    """
    for p in players:
        ai_name = p
        break
    RL = QLearningTable(actions=players[ai_name].possibilities([]))
    ai_win = 0
    win_rate_frequency = 100
    for episode in range(rounds):
        # initial observation
        _players = {}
        for name in players:
            if name == ai_name:
                _players[name] = AIPlayer(list(players[name].cards))
            else:
                _players[name] = Player(list(players[name].cards))
        ai_player = _players[ai_name]
        observation = Game(OrderedDict(_players), desk_pool=desk_pool)

        # RL choose action based on game history and cards on desk
        action = RL.choose_action(observation, ai_player)

        game_progress = observation.start_by_step()
        previous_state = observation.state

        for player_name, choice in game_progress:
            if observation.winner is None:
                reward = 0
            else:
                if observation.winner == ai_name:
                    reward = 1
                else:
                    reward = -1
            # RL choose action based on next observation
            action_ = RL.choose_action(observation, ai_player)

            # RL learn from this transition (s, a, r, s, a) ==> Sarsa
            RL.learn(previous_state, action, reward, observation.state, action_)

            # swap observation and action
            previous_state = observation.state
            action = action_

        if replay_game:
            observation.replay()

        if observation.winner == ai_name:
            ai_win += 1

        if episode > 0 and (episode + 1) % win_rate_frequency == 0:
            print('AI win rate for last {0} rounds: {1}'.format(win_rate_frequency,
                                                                float(ai_win) / float(win_rate_frequency)))
            ai_win = 0

    # end of game
    print('game over')


if __name__ == "__main__":
    # players = OrderedDict({
    #     'player1': AIPlayer([Card('2s'), Card('3d'), Card('3h'), Card('3c'), Card('4d')]),
    #     'player2': Player([Card('As'), Card('2d'), Card('5h')]),
    #     'player3': Player([Card('Ks'), Card('6d'), Card('6h'), Card('6s')]),
    # })
    # train(players, desk_pool=[])
    p1 = '3s,3d,5s,5h,6s,6d,6h,2s,2d,2h,4s'
    p2 = 'Ks,Kd,Kc,9s,9d,Vv'
    p3 = 'Jc,Jd,Jh,2c'
    train(OrderedDict({
        'p1': AIPlayer([Card(s) for s in p1.split(',')]),
        'p2': Player([Card(s) for s in p2.split(',')]),
        'p3': Player([Card(s) for s in p3.split(',')]),
    }), desk_pool=[], rounds=5500, replay_game=False)
