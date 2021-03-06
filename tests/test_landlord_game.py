#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from src.rule.landlord import Game, Player
from src.poker import Card


def test_simple_game():
    game = Game(OrderedDict({
        'player1': Player([Card('4d'), Card('5c'), Card('5s'), Card('Ah')]),
        'player2': Player([Card('2h'), Card('2d')]),
        'player3': Player([Card('9d')]),
    }), desk_pool=[])
    game.start()
    assert game.winner == 'player2'


def test_only_straight_win():
    game = Game(OrderedDict({
        'player1': Player([Card('4d'), Card('5c'), Card('6s'), Card('7h'), Card('8d')]),
        'player2': Player([Card('2h'), Card('2d')]),
        'player3': Player([Card('9d')]),
    }), desk_pool=[])
    game.start()
    if game.winner == 'player1':
        # The winning way is the straight
        assert len(game.history[0][1]) == 5
    else:
        assert game.winner == 'player2'


def test_player_should_skip():
    game = Game(OrderedDict({
        'player1': Player([Card('4d')]),
        'player2': Player([Card('2h')]),
        'player3': Player([Card('9d')]),
    }), desk_pool=[Card('9s'), Card('Kc'), Card('Ks'), Card('Kh')])
    game.start()
    assert game.winner == 'player3'
