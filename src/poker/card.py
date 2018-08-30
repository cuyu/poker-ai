#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .cardFactory import CardFactory


class Card(object):
    def __init__(self, card_string):
        self.card_int = CardFactory.new(card_string)

    def __str__(self):
        return CardFactory.int_to_pretty_str(self.card_int)

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return self.card_int

    def __lt__(self, other):
        return self.rank < other.rank

    @property
    def suit(self):
        suit_int = CardFactory.get_suit_int(self.card_int)
        # todo: return sth more readable?
        return suit_int

    @property
    def rank(self):
        return CardFactory.get_rank_int(self.card_int)
