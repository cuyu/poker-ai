#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.landlord import LandloardRule
from src.poker import Card


def test_single_card_in_desk():
    assert LandloardRule().possibilities([Card('2u')], [Card('2v'), Card('5c')]) == [Card('2v')]
    assert LandloardRule().possibilities([Card('Ks')], [Card('2h'), Card('5c')]) == [Card('2h')]
