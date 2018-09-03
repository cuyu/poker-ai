#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from src.landlord import Game, Player
from src.poker import Card


def test_simple_game():
    game = Game()
    game.players = OrderedDict({
        'player1': Player([Card('4d'), Card('5c'), Card('5s'), Card('Ah')]),
        'player2': Player([Card('2h'), Card('2d')]),
        'player3': Player([Card('9d')]),
    })
    game.start()
    assert game.winner == 'player2'


def test_only_straight_win():
    game = Game()
    game.players = OrderedDict({
        'player1': Player([Card('4d'), Card('5c'), Card('6s'), Card('7h'), Card('8d')]),
        'player2': Player([Card('2h'), Card('2d')]),
        'player3': Player([Card('9d')]),
    })
    game.start()
    if game.winner == 'player1':
        # The winning way is the straight
        assert len(game.history[0][1]) == 5
    else:
        assert game.winner == 'player2'
