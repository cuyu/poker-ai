#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.rule.landlord import LandlordRule
from src.poker import Card


def test_single_card_in_desk():
    assert LandlordRule().possibilities([Card('Uu')], [Card('Vv'), Card('5c')]) == [{Card('Vv')}]
    assert LandlordRule().possibilities([Card('Ks')], [Card('2h'), Card('5c')]) == [{Card('2h')}]
    assert LandlordRule().possibilities([Card('2s')], [Card('2h'), Card('5c')]) == []
    assert LandlordRule().possibilities([Card('Ks')], [Card('Jh'), Card('5c')]) == []


def test_two_same_card_in_desk():
    desk = [Card('Ks'), Card('Kh')]
    hand = [Card('As'), Card('Uu'), Card('5c'), Card('Ac')]
    assert {Card('As'), Card('Ac')} in LandlordRule().possibilities(desk, hand)


def test_three_same_card_in_desk():
    desk = [Card('Js'), Card('Jh'), Card('Jc')]
    hand = [Card('2s'), Card('Uu'), Card('5c'), Card('2c'), Card('2d')]
    assert {Card('2s'), Card('2c'), Card('2d')} in LandlordRule().possibilities(desk, hand)


def test_three_same_card_and_one_single_card_in_desk():
    # todo: can the single card be joker?
    desk = [Card('Js'), Card('Jh'), Card('Jc'), Card('As')]
    hand = [Card('Ks'), Card('Kd'), Card('3c'), Card('Kc'), Card('2d')]
    assert {Card('Ks'), Card('Kd'), Card('Kc'), Card('3c')} in LandlordRule().possibilities(desk, hand)
    assert {Card('Ks'), Card('Kd'), Card('Kc'), Card('2d')} in LandlordRule().possibilities(desk, hand)
    desk = [Card('7d'), Card('Kh'), Card('Kd'), Card('Ks')]
    hand = [Card('9s'), Card('Ad'), Card('9h'), Card('9c'), Card('Jd')]
    assert [] == LandlordRule().possibilities(desk, hand)


def test_four_same_card_aka_bomb_in_desk():
    desk = [Card('Js'), Card('Jh'), Card('Jc'), Card('Jd')]
    hand = [Card('2s'), Card('Uu'), Card('5c'), Card('2c'), Card('2d'), Card('2h')]
    assert {Card('2s'), Card('2c'), Card('2d'), Card('2h')} in LandlordRule().possibilities(desk, hand)
    desk = [Card('Js'), Card('Jh'), Card('Jc'), Card('Jd')]
    hand = [Card('2s'), Card('Uu'), Card('5c'), Card('Ac'), Card('2d'), Card('2h')]
    assert [] == LandlordRule().possibilities(desk, hand)


def test_full_house_in_desk():
    desk = [Card('Js'), Card('Jh'), Card('Jc'), Card('Kd'), Card('Ks')]
    hand = [Card('As'), Card('Uu'), Card('5c'), Card('Ac'), Card('Ad'), Card('2h'), Card('5h')]
    assert {Card('As'), Card('Ac'), Card('Ad'), Card('5h'), Card('5c')} in LandlordRule().possibilities(desk, hand)
    desk = [Card('Js'), Card('Jh'), Card('Jc'), Card('Kd'), Card('Ks')]
    hand = [Card('5s'), Card('Uu'), Card('5c'), Card('Ac'), Card('Ad'), Card('2h'), Card('5h')]
    assert [] == LandlordRule().possibilities(desk, hand)


def test_four_same_card_and_two_single_card_in_desk():
    pass


def test_five_card_straight_in_desk():
    desk = [Card('5s'), Card('6h'), Card('7c'), Card('8d'), Card('9s')]
    hand = [Card('Js'), Card('Tc'), Card('9c'), Card('Qc'), Card('Ad'), Card('Kh'), Card('2h')]
    assert {Card('Tc'), Card('Js'), Card('Qc'), Card('Kh'), Card('Ad')} in LandlordRule().possibilities(desk, hand)


def test_long_straight_in_desk():
    pass


def test_three_pairs_in_desk():
    pass


def test_four_same_card_in_hand():
    desk = [Card('As'), Card('Ah'), Card('Ac'), Card('2d'), Card('2c')]
    hand = [Card('9d'), Card('9h'), Card('9c'), Card('Uu'), Card('Ad'), Card('9s'), Card('2h')]
    assert [{Card('9d'), Card('9h'), Card('9c'), Card('9s')}] == LandlordRule().possibilities(desk, hand)


def test_super_bomb_in_hand():
    desk = [Card('As'), Card('Ah'), Card('Ac'), Card('Ad')]
    hand = [Card('Vv'), Card('Tc'), Card('9c'), Card('Uu'), Card('Ad'), Card('Kh'), Card('2h')]
    assert [{Card('Vv'), Card('Uu')}] == LandlordRule().possibilities(desk, hand)


def test_all_possibilities():
    hand = [Card('As'), Card('Uu'), Card('5c'), Card('Ac'), Card('Ad'), Card('2h'), Card('5h')]
    assert {Card('As'), Card('Ac'), Card('Ad'), Card('2h')} in LandlordRule().all_possibilities(hand)
