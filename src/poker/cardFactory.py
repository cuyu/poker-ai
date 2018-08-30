class CardFactory(object):
    """
    Static class that handles cards. We represent cards as 32-bit integers, so 
    there is no object instantiation - they are just ints. Most of the bits are 
    used, and have a specific meaning. See below: 

                                    Card:

                          bitrank     suit rank   prime
                    +--------+--------+--------+--------+
                    |xxxbbbbb|bbbbbbbb|vucdhsrr|rrpppppp|
                    +--------+--------+--------+--------+

        1) p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
        2) r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
        3) vucdhs = suit of card (bit turned on based on suit of card)
        4) b = bit turned on depending on rank of card
        5) x = unused

    This representation will allow us to do very important things like:
    - Make a unique prime prodcut for each hand
    - Detect flushes
    - Detect straights

    and is also quite performant.
    """

    # the basics
    STR_RANKS = '23456789TJQKAXUV'
    INT_RANKS = range(16)
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    # converstion from string => int
    CHAR_RANK_TO_INT_RANK = dict(zip(list(STR_RANKS), INT_RANKS))
    CHAR_SUIT_TO_INT_SUIT = {
        's': 1,  # spades
        'h': 2,  # hearts
        'd': 4,  # diamonds
        'c': 8,  # clubs
        'u': 16,  # small joker
        'v': 32,  # big joker
    }
    INT_SUIT_TO_CHAR_SUIT = 'xshxdxxxc'

    # for pretty printing
    PRETTY_SUITS = {
        1: u"\u2660".encode('utf-8'),  # spades
        2: u"\u2764".encode('utf-8'),  # hearts
        4: u"\u2666".encode('utf-8'),  # diamonds
        8: u"\u2663".encode('utf-8'),  # clubs
        16: u"\u263e".encode('utf-8'),  # small joker
        32: u"\u2600".encode('utf-8'),  # big joker
    }

    # hearts and diamonds
    PRETTY_REDS = [2, 4, 32]

    @staticmethod
    def new(string):
        """
        Converts Card string to binary integer representation of card, inspired by:
        
        http://www.suffecool.net/poker/evaluator.html
        """

        rank_char = string[0]
        suit_char = string[1]
        if suit_char in {'u', 'v'}:
            assert suit_char == rank_char.lower()

        rank_int = CardFactory.CHAR_RANK_TO_INT_RANK[rank_char]
        suit_int = CardFactory.CHAR_SUIT_TO_INT_SUIT[suit_char]
        rank_prime = CardFactory.PRIMES[rank_int] if rank_char not in 'UV' else CardFactory.PRIMES[0]

        bitrank = 1 << rank_int << 16
        suit = suit_int << 10
        rank = rank_int << 6

        return bitrank | suit | rank | rank_prime

    @staticmethod
    def int_to_str(card_int):
        rank_int = CardFactory.get_rank_int(card_int)
        suit_int = CardFactory.get_suit_int(card_int)
        return CardFactory.STR_RANKS[rank_int] + CardFactory.INT_SUIT_TO_CHAR_SUIT[suit_int]

    @staticmethod
    def get_rank_int(card_int):
        return (card_int >> 6) & 0xF

    @staticmethod
    def get_suit_int(card_int):
        return (card_int >> 10) & 0x3F

    @staticmethod
    def get_bitrank_int(card_int):
        return (card_int >> 16) & 0x1FFF

    @staticmethod
    def get_prime(card_int):
        return card_int & 0x3F

    @staticmethod
    def hand_to_binary(card_strs):
        """
        Expects a list of cards as strings and returns a list
        of integers of same length corresponding to those strings. 
        """
        bhand = []
        for c in card_strs:
            bhand.append(CardFactory.new(c))
        return bhand

    @staticmethod
    def prime_product_from_hand(card_ints):
        """
        Expects a list of cards in integer form. 
        """

        product = 1
        for c in card_ints:
            product *= (c & 0xFF)

        return product

    @staticmethod
    def prime_product_from_rankbits(rankbits):
        """
        Returns the prime product using the bitrank (b)
        bits of the hand. Each 1 in the sequence is converted
        to the correct prime and multiplied in.

        Params:
            rankbits = a single 32-bit (only 13-bits set) integer representing 
                    the ranks of 5 _different_ ranked cards 
                    (5 of 13 bits are set)

        Primarily used for evaulating flushes and straights, 
        two occasions where we know the ranks are *ALL* different.

        Assumes that the input is in form (set bits):

                              rankbits     
                        +--------+--------+
                        |xxxbbbbb|bbbbbbbb|
                        +--------+--------+

        """
        product = 1
        for i in CardFactory.INT_RANKS:
            # if the ith bit is set
            if rankbits & (1 << i):
                product *= CardFactory.PRIMES[i]

        return product

    @staticmethod
    def int_to_binary(card_int):
        """
        For debugging purposes. Displays the binary number as a 
        human readable string in groups of four digits. 
        """
        bstr = bin(card_int)[2:][::-1]  # chop off the 0b and THEN reverse string
        output = list("".join(["0000" + "\t"] * 7) + "0000")

        for i in range(len(bstr)):
            output[i + int(i / 4)] = bstr[i]

        # output the string to console
        output.reverse()
        return "".join(output)

    @staticmethod
    def int_to_pretty_str(card_int):
        """
        Prints a single card 
        """

        color = False
        try:
            from termcolor import colored
            ### for mac, linux: http://pypi.python.org/pypi/termcolor
            ### can use for windows: http://pypi.python.org/pypi/colorama
            color = True
        except ImportError:
            pass

        # suit and rank
        suit_int = CardFactory.get_suit_int(card_int)
        rank_int = CardFactory.get_rank_int(card_int)

        # if we need to color red
        s = CardFactory.PRETTY_SUITS[suit_int].decode('utf-8')
        if color and suit_int in CardFactory.PRETTY_REDS:
            s = colored(s, "red")

        r = CardFactory.STR_RANKS[rank_int]

        if suit_int < 16:
            return " [ " + r + " " + str(s) + " ] "
        else:
            return " [ " + str(s) + " ] "

    @staticmethod
    def print_pretty_card(card_int):
        """
        Expects a single integer as input
        """
        print(CardFactory.int_to_pretty_str(card_int))

    @staticmethod
    def print_pretty_cards(card_ints):
        """
        Expects a list of cards in integer form.
        """
        output = " "
        for i in range(len(card_ints)):
            c = card_ints[i]
            if i != len(card_ints) - 1:
                output += CardFactory.int_to_pretty_str(c) + ","
            else:
                output += CardFactory.int_to_pretty_str(c) + " "

        print(output)
