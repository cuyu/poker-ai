#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.landlord import LandloardRule
from src.poker import Card


def test_single_card_in_desk():
    assert LandloardRule().possibilities([Card('Uu')], [Card('Vv'), Card('5c')]) == [{Card('Vv')}]
    assert LandloardRule().possibilities([Card('Ks')], [Card('2h'), Card('5c')]) == [{Card('2h')}]
    assert LandloardRule().possibilities([Card('Ks')], [Card('Jh'), Card('5c')]) == []


def test_two_same_card_in_desk():
    desk = [Card('Ks'), Card('Kh')]
    hand = [Card('As'), Card('Uu'), Card('5c'), Card('Ac')]
    assert {Card('As'), Card('Ac')} in LandloardRule().possibilities(desk, hand)


def test_three_same_card_in_desk():
    desk = [Card('Js'), Card('Jh'), Card('Jc')]
    hand = [Card('2s'), Card('Uu'), Card('5c'), Card('2c'), Card('2d')]
    assert {Card('2s'), Card('2c'), Card('2d')} in LandloardRule().possibilities(desk, hand)


def test_three_same_card_and_one_single_card_in_desk():
    desk = [Card('Js'), Card('Jh'), Card('Jc'), Card('2s')]
    hand = [Card('Ks'), Card('Kd'), Card('3c'), Card('Kc'), Card('Ad')]
    assert {Card('Ks'), Card('Kd'), Card('Kc')} in LandloardRule().possibilities(desk, hand)


def test_four_same_card_aka_bomb_in_desk():
    pass


def test_full_house_in_desk():
    pass


def test_four_same_card_and_two_card_in_desk():
    pass
