#!/usr/bin/env python
# -*- coding: utf-8 -*-



if __name__ == '__main__':
    from poker import Deck, Card

    deck = Deck()
    player1_hand = deck.draw(52)
    Card.print_pretty_cards(player1_hand)
    # player2_hand = deck.draw(2)
    # player3_hand = deck.draw(2)
