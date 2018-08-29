#!/usr/bin/env python
# -*- coding: utf-8 -*-



if __name__ == '__main__':
    from poker import Deck, Card

    # card_int = Card.new('2s')
    # Card.print_pretty_card(card_int)
    # card_int = Card.new('K')
    # Card.print_pretty_card(card_int)
    deck = Deck(has_jokers=True)
    player1_hand = deck.draw(54)
    Card.print_pretty_cards(player1_hand)
    # player2_hand = deck.draw(2)
    # player3_hand = deck.draw(2)
