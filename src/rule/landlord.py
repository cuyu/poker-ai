#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from collections import OrderedDict

from src.poker import Deck, Card


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
            if card1.rank == 0 and card2.rank != 0:
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

    def _possibilities_of_straight(self, hand_cards, target_start_card, length):
        def _find_rank_in_hands(hand_cards, rank):
            result = []
            for card in hand_cards:
                if card.rank == rank:
                    result.append(card)
            return result

        assert length >= 5
        result = []
        i = 0
        while i < len(hand_cards) - (length - 1):
            if self.higher(hand_cards[i], target_start_card):
                is_straight = True
                possible = {hand_cards[i]}
                for j in range(1, length):
                    next_cards = _find_rank_in_hands(hand_cards, hand_cards[i].rank + j)
                    if not next_cards:
                        is_straight = False
                        break
                    else:
                        possible.add(next_cards[0])
                if is_straight:
                    result.append(possible)
            i += 1

        return result

    def _possibilities_of_bomb(self, hand_cards, target_cards):
        result = []
        if len(target_cards) == 4 and target_cards[0].rank == target_cards[1].rank == target_cards[2].rank == \
                target_cards[3].rank:
            result += self._possibilities_of_same_rank(hand_cards, target_cards[0], 4)
        else:
            result += self._possibilities_of_same_rank(hand_cards, Card(rank=-1), 4)
        if Card('Uu') in hand_cards and Card('Vv') in hand_cards:
            result.append({Card('Uu'), Card('Vv')})
        return result

    def all_possibilities(self, hand_cards):
        """
        List all the possibilities according the cards in hands (assuming the desk is empty).
        :param hand_cards: a list of Card
        :return: a list of set of Card
        """
        result = []
        # Todo: add more kinds of desk cards
        # Possibilities without straight
        assume_desk_cards = [
            [Card(rank=-1)],
            [Card(rank=-1), Card(rank=-1)],
            [Card(rank=-1), Card(rank=-1), Card(rank=-1)],
            [Card(rank=-1), Card(rank=-1), Card(rank=-1), Card(rank=-1)],
            [Card(rank=-1), Card(rank=-1), Card(rank=-1), Card(rank=-2)],
            [Card(rank=-1), Card(rank=-1), Card(rank=-1), Card(rank=-2), Card(rank=-2)],
        ]
        for desk_cards in assume_desk_cards:
            result += self.possibilities(desk_cards, hand_cards)

        # Possibilities with straight
        has_straight = True
        length = 5
        while has_straight and length <= len(hand_cards):
            straight_result = self._possibilities_of_straight(hand_cards, Card(rank=-1), length=length)
            if not straight_result:
                break
            result += straight_result
            length += 1

        return result

    def possibilities(self, desk_cards, hand_cards):
        """
        List possibilities according to the cards in desk and cards in hands
        :param desk: a list of Card
        :param hand: a list of Card
        :return: a list of set of Card
        """
        desk_cards.sort()
        hand_cards.sort()
        # No one is higher than the super bomb
        if Card('Vv') in desk_cards and Card('Uu') in desk_cards:
            return []
        result = self._possibilities_of_bomb(hand_cards, desk_cards)
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
                # This is a bomb, we have got all the possible bombs, so we just do nothing here
                pass
            else:
                # Three same cards with one single card
                # Pick the second card as target card, as the type could be AAAB or ABBB
                three_same = self._possibilities_of_same_rank(hand_cards, desk_cards[1], 3)
                for possibility in three_same:
                    for card in hand_cards:
                        if card not in possibility:
                            result.append({*possibility, card})
        elif len(desk_cards) == 5:
            if desk_cards[0].rank == desk_cards[1].rank:
                # Full house
                # Pick the third card as target card, as the type could be AABBB or AAABB
                three_same = self._possibilities_of_same_rank(hand_cards, desk_cards[2], 3)
                two_same = self._possibilities_of_same_rank(hand_cards, Card(rank=-1), 2)
                for p in three_same:
                    for q in two_same:
                        if next(iter(p)).rank != next(iter(q)).rank:
                            result.append({*p, *q})
            else:
                # Straight
                result += self._possibilities_of_straight(hand_cards, desk_cards[0], length=5)

        else:
            result += self._possibilities_of_straight(hand_cards, desk_cards[0], length=len(desk_cards))
        return result


class Game(object):
    def __init__(self, players, desk_pool):
        """
        :param players: a OrderedDict, keys are player's names, values are <Player> instance
        :param desk_pool: a list of <Card> instance
        """
        self.players = players
        names = list(self.players.keys())
        self._player_index = {names[idx]: idx for idx in range(len(names))}
        self.desk_pool = desk_pool
        self.history = []
        self.rule = LandlordRule()
        self._winner = None

    def start_by_step(self):
        """
        :return: a generator with player_name and choice of that step
        """
        game_over = False
        player_turn = 0
        players = list(self.players.items())
        continuous_no_choice = 0
        while not game_over:
            player_name, player = players[player_turn % len(players)]
            choice = player.show_card(self.desk_pool)
            if choice:
                self.desk_pool = choice
                continuous_no_choice = 0
            else:
                continuous_no_choice += 1

            self.history.append((player_name, choice,))
            player_turn += 1

            if player.is_empty():
                self._winner = player_name
                game_over = True

            if continuous_no_choice == len(players) - 1:
                # If the other player have no choice, then the player can play any cards
                self.desk_pool = []

            yield (player_name, choice,)

    def start(self):
        steps = self.start_by_step()
        for player_name, choice in steps:
            pass  # Do nothing

    @property
    def winner(self):
        return self._winner

    @property
    def state(self):
        """
        The state of the game, used by reinforcement learning
        The state here only include the history of the game (the history include the history of current cards in desk).

        To make the state friendly to neural network, we will add the player info into card rank, so that the total
        dimension of state will be limited to a fixed value. For example, if player 1 played two cards with rank 6, then
        in state, it will shows [4, 4], if player 2 played that in history, it will be [24, 24], for player 3,
        it will be [44, 44].
        The final state format for specific player should be [cards in hand, history].
        """
        state = []
        for player_name, cards in self.history:
            for c in sorted(cards):
                state.append(c.rank + self._player_index[player_name] * 20)
        return state

    def replay(self):
        for player_name, choice in self.history:
            if choice:
                print("{}'s turn:".format(player_name), *[str(c) for c in choice])
            else:
                print("{}'s turn:  Skip".format(player_name))
        print("----------- final -----------")
        for player_name, player in list(self.players.items()):
            print("{}'s hand:".format(player_name), *[str(c) for c in player.cards])
        print("$$$$$$ {} is the winner $$$$$$".format(self.winner))


class WholeGame(Game):
    def __init__(self):
        self.deck = Deck(has_jokers=True)
        players = OrderedDict({
            'player1': Player(self.deck.draw(20)),
            'player2': Player(self.deck.draw(17)),
            'player3': Player(self.deck.draw(17)),
        })
        super(WholeGame, self).__init__(players, desk_pool=[])


class Player(object):
    def __init__(self, cards):
        """
        :param cards: A list of <Card> instance
        """
        self.cards = cards
        self.cards.sort()

    def show_card(self, desk_cards):
        """
        Show card according to the cards in desk. Return [] means skip the step.
        :param desk_cards: List of <Card>
        :return: List of <Card>
        """
        if desk_cards:
            options = LandlordRule().possibilities(desk_cards, self.cards)
        else:
            options = LandlordRule().all_possibilities(self.cards)
        if options:
            choice = random.choice(options)
            for card in choice:
                self.cards.remove(card)
            return list(choice)
        else:
            return []

    def is_empty(self):
        return len(self.cards) == 0


class AIPlayer(Player):
    def __init__(self, cards):
        super(AIPlayer, self).__init__(cards)
        self._next_action = None

    def possibilities(self, desk_cards):
        """
        Used by reinforcement learning
        """
        if desk_cards:
            options = LandlordRule().possibilities(desk_cards, self.cards)
        else:
            options = LandlordRule().all_possibilities(self.cards)
        return options

    def choose_next_action(self, cards):
        """
        Used by reinforcement learning
        :param cards: a string represent a list of Card
        """
        if cards:
            cards_rank = [int(i) for i in cards.split(',')]
            _cards = []
            for r in cards_rank:
                for c in self.cards:
                    if c.rank == r and c not in _cards:
                        _cards.append(c)
                        break
        else:
            _cards = []
        self._next_action = _cards

    def show_card(self, desk_cards):
        assert self._next_action is not None
        for card in self._next_action:
            self.cards.remove(card)
        return self._next_action


if __name__ == '__main__':
    game1 = WholeGame()
    game1.start()
    game1.replay()
