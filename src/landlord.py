#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .poker.card import Card


class BasicRule(object):
    def __int__(self):
        pass


class LandlordRule(BasicRule):
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

    def _possibilities_of_same_rank(self, hand_cards, target_card, same_number):
        result = []
        i = 0
        while i < len(hand_cards) - (same_number - 1):
            if self.higher(hand_cards[i], target_card):
                if hand_cards[i].rank == hand_cards[i + same_number - 1].rank:
                    result.append({*hand_cards[i:i + same_number]})
                    i += same_number
                else:
                    i += 1
            else:
                i += 1
        return result

    def all_possibilities(self, hand_cards):
        """
        List all the possibilities according the cards in hands (assuming the desk is empty).
        :param hand_cards: a list of Card
        :return: a list of set of Card
        """
        result = []
        # Todo: add more kinds of desk cards
        assume_desk_cards = [
            [Card(rank=-1)],
            [Card(rank=-1), Card(rank=-1)],
            [Card(rank=-1), Card(rank=-1), Card(rank=-1)],
            [Card(rank=-1), Card(rank=-1), Card(rank=-1), Card(rank=-1)],
            [Card(rank=-1), Card(rank=-1), Card(rank=-1), Card(rank=-2)],
            [Card(rank=-1), Card(rank=-1), Card(rank=-1), Card(rank=-2), Card(rank=-2)],
            [Card(rank=-1), Card(rank=-2), Card(rank=-3), Card(rank=-4), Card(rank=-5)],
        ]
        for desk_cards in assume_desk_cards:
            result += self.possibilities(desk_cards, hand_cards)

        return result

    def possibilities(self, desk_cards, hand_cards):
        """
        List possibilities according to the cards in desk and cards in hands
        :param desk: a list of Card
        :param hand: a list of Card
        :return: a list of set of Card
        """
        result = []
        desk_cards.sort()
        hand_cards.sort()
        if len(desk_cards) == 1:
            for card in hand_cards:
                if self.higher(card, desk_cards[0]):
                    result.append({card})
        elif len(desk_cards) == 2:
            assert desk_cards[0].rank == desk_cards[1].rank
            result += self._possibilities_of_same_rank(hand_cards, desk_cards[0], 2)
        elif len(desk_cards) == 3:
            assert desk_cards[0].rank == desk_cards[1].rank == desk_cards[2].rank
            result += self._possibilities_of_same_rank(hand_cards, desk_cards[0], 3)
        elif len(desk_cards) == 4:
            if desk_cards[0].rank == desk_cards[1].rank == desk_cards[2].rank == desk_cards[3].rank:
                result += self._possibilities_of_same_rank(hand_cards, desk_cards[0], 4)
            else:
                # Three same cards with one single card
                three_same = self._possibilities_of_same_rank(hand_cards, desk_cards[0], 3)
                for possibility in three_same:
                    for card in hand_cards:
                        if card not in possibility:
                            result.append({*possibility, card})
        elif len(desk_cards) == 5:
            if desk_cards[0].rank == desk_cards[1].rank:
                # Full house
                three_same = self._possibilities_of_same_rank(hand_cards, desk_cards[0], 3)
                two_same = self._possibilities_of_same_rank(hand_cards, Card(rank=-1), 2)
                for p in three_same:
                    for q in two_same:
                        if next(iter(p)).rank != next(iter(q)).rank:
                            result.append({*p, *q})
            else:
                # Straight
                i = 0
                while i < len(hand_cards) - 4:
                    hand_cards[i].rank
                    i += 1
        return result


if __name__ == '__main__':
    from poker import Deck, Card

    deck = Deck(has_jokers=True)
    player1_hand = deck.draw(17)
    for card in player1_hand:
        print(card)
    player2_hand = deck.draw(17)
    player3_hand = deck.draw(17)
