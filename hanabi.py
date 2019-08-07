import random

# Two player hanabi

# Raw data should be attributes
# Anything that can be determined from raw data should be a method
# However methods are calculated every time they are called
# Wheras attributes are computed every time there is an update


class Blueprints(object):
    def __init__(self):
        self.colours = ["white", "green", "yellow", "red", "blue"]
        self.digits = {1: 3, 2: 2, 3: 2, 4: 2, 5: 1}

        self.unique_cards_complete = []  # List of unique cards in a complete deck
        self.cards_complete = []  # Ordered list of cards in a complete deck

        for colour in self.colours:
            for i in self.digits.keys():
                card = (colour, i)

                self.unique_cards_complete.append(card)
                self.cards_complete += self.digits[i] * [card]


class Deck(object):
    def __init__(self, blueprints):
        """A complete and shuffled deck"""
        self.blueprints = blueprints
        self.cards = self.blueprints.cards_complete.copy()
        random.shuffle(self.cards)

        print("Cards shuffled, bottom card: ", self.cards[-1])

        self.most_recently_drawn_card = None

    def draw(self):
        self.most_recently_drawn_card = self.cards.pop()

    def size(self):
        return len(self.cards)


class Brain(object):
    def __init__(self, blueprints):
        """An empty brain"""

        # Cards either in the deck, or in my hand
        self.cards_in_deck_or_my_hand = blueprints.cards_complete.copy()

        self.my_hand = [
            {"candidates": blueprints.cards_complete.copy(), "age": None}
            for i in range(5)
        ]

        self.your_hand = [{"i_know": None, "you_know": None, "playable": None}]

        self.other_player_just_drew_a_card = False

        # And yes there's more but let's stop here

    def update_on_new_card(self, card):

        if card not in self.cards_in_deck_or_my_hand:
            raise Exception(
                "A newly dealt card was not considered possible, "
                + "i.e. in [cards_in_deck_or_my_hand]"
            )

        assert self.cards_in_deck_or_my_hand.remove(card) is None

        for i in range(5):
            self.my_hand[i]["i_know"] = [
                card
                for card in self.my_hand[i]["candidates"]
                if card in self.cards_in_deck_or_my_hand
            ]

    def i_have_playable_cards(self, table):
        is_card_playable = [
            all(
                [
                    card in table.playable_cards()
                    for card in self.my_hand[i]["candidates"]
                ]
            )
            for i in range(5)
        ]

        return any(is_card_playable)

    def random_helpful_piece_of_information(self):
        raise Exception("Implement me")

    def next_action(self, table):
        if self.other_player_just_drew_a_card:
            raise Exception("Not yet have I programmed this")
        elif self.i_have_playable_cards(table):
            raise Exception("Not yet have I programmed this")
        else:
            self.random_helpful_piece_of_information()


class Player(object):
    def __init__(self, name, blueprints):
        """A player with no hand and no knowledge"""

        self.name = name
        self.hand = 5 * [None]
        self.hand_age = 5 * [None]
        self.brain = Brain(blueprints)


class Table(object):
    def __init__(self, blueprints):
        """A table with no played or discarded cards on it yet"""
        self.blueprints = blueprints
        self.played = {colour: 0 for colour in self.blueprints.colours}
        self.discarded = []

    def playable_cards(self):

        playable_cards = []

        for colour in self.blueprints.colours:
            i = self.played[colour]

            if i == 5:
                continue
            else:
                playable_cards.append((colour, i + 1))

        return playable_cards


class Game(object):
    def __init__(self):
        self.blueprints = Blueprints()
        self.deck = Deck(self.blueprints)
        self.table = Table(self.blueprints)

        self.players = [
            Player("Maria", self.blueprints),
            Player("Harry", self.blueprints),
        ]

        self.n_turns = 0
        self.game_over = False

    def other_player(self, player):
        assert player in self.players

        if player == self.players[0]:
            return self.players[1]
        elif player == self.players[1]:
            return self.players[0]
        else:
            raise Exception("Unreachable else")

    def print_state(self, print_brains=False):
        for player in self.players:
            print(player.name)
            print(player.hand)

            if print_brains:
                print(player.brain.what_i_know_of_my_hand)
                print(player.brain.what_i_know_you_know_of_your_hand)
                print(player.brain.what_you_know_i_know_of_my_hand)

            print()

        print(self.deck.cards)

    def deal_cards(self):

        # Draw the opening hand
        for player in self.players:
            for i in range(5):
                assert self.deck.draw() is None
                card = self.deck.most_recently_drawn_card
                player.hand[i] = card
                player.hand_age[i] = 0
                self.other_player(player).brain.update_on_new_card(card)

    def play(self):
        self.deal_cards()
        self.print_state()

        while not self.game_over:

            for player in self.players:
                player_action = player.brain.next_action(self.table)
                print(player_action)


if __name__ == "__main__":
    game1 = Game()
    game1.play()
