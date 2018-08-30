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
            for i in range(len(hand_cards)):
                if self.higher(hand_cards[i], desk_cards[0]):
                    for j in range(i + 1, len(hand_cards)):
                        if hand_cards[i].rank == hand_cards[j].rank:
                            result.append({hand_cards[i], hand_cards[j]})
        elif len(desk_cards) == 3:
            assert desk_cards[0].rank == desk_cards[1].rank == desk_cards[2].rank
            for i in range(len(hand_cards)):
                if self.higher(hand_cards[i], desk_cards[0]):
                    for j in range(i + 1, len(hand_cards)):
                        if hand_cards[i].rank == hand_cards[j].rank:
                            for k in range(j + 1, len(hand_cards)):
                                if hand_cards[k].rank == hand_cards[j].rank:
                                    result.append({hand_cards[i], hand_cards[j], hand_cards[k]})

        return result


if __name__ == '__main__':
    from poker import Deck, Card

    deck = Deck(has_jokers=True)
    player1_hand = deck.draw(17)
    for card in player1_hand:
        print(card)
    player2_hand = deck.draw(17)
    player3_hand = deck.draw(17)
