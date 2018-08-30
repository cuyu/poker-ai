from random import shuffle

from src.poker.card import Card
from .cardFactory import CardFactory


class Deck(object):
    """
    Class representing a deck. The first time we create, we seed the static 
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it. 
    """
    _FULL_DECK = []

    def __init__(self, has_jokers=False):
        self.has_jokers = has_jokers
        self.shuffle()

    def shuffle(self):
        # and then shuffle
        self.cards = Deck.GetFullDeck(self.has_jokers)
        shuffle(self.cards)

    def draw(self, n=1):
        if n == 1:
            return self.cards.pop(0)

        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards

    def __str__(self):
        return CardFactory.print_pretty_cards(self.cards)

    @staticmethod
    def GetFullDeck(has_jokers=False):
        if Deck._FULL_DECK:
            return list(Deck._FULL_DECK)

        # create the standard 52 card deck
        for rank in CardFactory.STR_RANKS[:13]:
            for suit in 'shdc':
                Deck._FULL_DECK.append(Card(rank + suit))

        if has_jokers:
            Deck._FULL_DECK.append(Card('Uu'))
            Deck._FULL_DECK.append(Card('Vv'))
        return list(Deck._FULL_DECK)