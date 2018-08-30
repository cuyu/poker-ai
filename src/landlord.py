#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BasicRule(object):
    def __int__(self):
        pass


class LandloardRule(BasicRule):
    def __int__(self):
        pass

    @staticmethod
    def higher(card1, card2):
        if card1.suit >= 16 or card2.suit >= 16:
            # If any of the card is joker, big joker get the highest, then the small joker
            return card1.suit > card2.suit
        else:
            # 2 is higher than A
            if card1.rank == 0:
                return True
            elif card2.rank == 0:
                return False
            else:
                return card1.rank > card2.rank

    def possibilities(self, desk_cards, hand_cards):
        """
        :param desk: a list of Card
        :param hand: a list of Card
        :return: a list of set of Card
        """
        result = []
        if len(desk_cards) == 1:
            for card in hand_cards:
                if self.higher(card, desk_cards[0]):
                    result.append({card})
        elif len(desk_cards) == 2:
            assert desk_cards[0].rank == desk_cards[1].rank
            for card in hand_cards:
                if self.higher(card, desk_cards[0]):
                    for card2 in hand_cards:
                        if card2.rank == card.rank and card2 != card:
                            result.append({card, card2})

        return result


if __name__ == '__main__':
    from poker import Deck, Card

    deck = Deck(has_jokers=True)
    player1_hand = deck.draw(17)
    for card in player1_hand:
        print(card)
    player2_hand = deck.draw(17)
    player3_hand = deck.draw(17)
