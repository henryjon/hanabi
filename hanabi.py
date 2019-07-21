import random

# We make many assumptions that this is a two player game.

# Raw data should be attributes
# Anything that can be determined from raw data should be a method
# However methods are calculated every time they are called
# Wheras attributes are computed every time there is an update


class Deck(object):
    def __init__(self):
        """A complete deck"""
        self.colours = ["white", "green", "yellow", "red", "blue"]
        self.digits = {1: 3, 2: 2, 3: 2, 4: 2, 5: 1}

        self.unique_cards_complete = []  # List of unique cards in a complete deck
        self.cards_complete = []  # Ordered list of cards in a complete deck

        for colour in self.colours:
            for i in self.digits.keys():
                card = (colour, i)

                self.unique_cards_complete.append(card)
                self.cards_complete += self.digits[i] * [card]

        self.cards = self.cards_complete.copy()  # Ordered list of cards in this deck

        # Shuffle the cards
        random.shuffle(self.cards)

        print("Cards shuffled, bottom card: ", self.cards[-1])

    def draw(self):
        card = self.cards.pop()
        return card

    def size(self):
        return len(self.cards)


class Brain(object):
    def __init__(self, deck):
        """An empty brain"""

        # Cards either in the deck, or in my hand
        self.deck_or_mine = deck.cards_complete.copy()

        # What I know about my cards
        self.i_know = [deck.unique_cards_complete.copy() for i in range(5)]

        # What I know you know about your cards
        self.you_know = [deck.unique_cards_complete.copy() for i in range(5)]

        # What I know you know that I know about my cards
        self.you_know_i_know = [deck.unique_cards_complete.copy() for i in range(5)]

        # And yes there's more but let's stop here

    def update_on(self, evidence_type, evidence):

        if evidence_type == "opening_hands":
            self.update_on_opening_hands(evidence)
        else:
            raise Exception("Evidence type not recognised")

    def update_on_opening_hands(self, your_opening_hand):

        # I see your cards. I remove them from 'deck_or_mine'
        # And if saturated I also remove them as candidates for my cards

        for card in your_opening_hand:
            if card not in self.deck_or_mine:
                raise Exception(
                    "A freshly dealt card was not considered possible, "
                    + "i.e. in [deck_or_mine]"
                )

            self.deck_or_mine.remove(card)

        for i in range(5):
            self.i_know[i] = [
                card for card in self.i_know[i] if card in self.deck_or_mine
            ]


class Player(object):
    def __init__(self, name, deck):
        """A player with no hand and no knowledge"""

        self.name = name
        self.hand = 5 * [None]
        self.hand_age = 5 * [None]
        self.brain = Brain(deck)


class State(object):
    def __init__(self, deck, players):
        """Generate an initial game state"""

        self.deck = deck
        self.players = players

        self.discarded = {card: 0 for card in self.deck.unique_cards_complete}
        self.played = {card: False for card in self.deck.unique_cards_complete}

    def print_state(self):

        print("N turns: ", self.n_turns)
        print("Information: ", self.information_tokens, "/ 8")
        print("Lives: ", self.lives, "/ 3")
        print("")

        for player in self.players:
            print("Player ", player)
            for card in self.hand[player].values():
                print(card)
            print("")

        for card in self.deck.unique_cards_complete:
            print("Card: ", card)
            print("Disc: ", self.discarded[card])
            print("Play: ", self.played[card])
            print("")


class Game(object):
    def __init__(self):
        self.deck = Deck()
        self.players = [Player("Maria", self.deck), Player("Harry", self.deck)]
        self.state = State(self.deck, self.players)

    def deal_out(self):

        # Draw the opening hand
        for player in self.players:
            for i in range(5):
                player.hand[i] = self.deck.draw()

        # Update knowledge based on this
        for player, other_player in [self.players, self.players[::-1]]:
            player.brain.update_on("opening_hands", other_player.hand)

    def play(self):
        self.deal_out()
