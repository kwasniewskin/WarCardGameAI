import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for value in range(1, 14) for suit in ["hearts", "diamonds", "clubs", "spades"]]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class Game:
    def __init__(self):
        self.player_deck = Deck()
        self.ai_deck = Deck()
        self.round = 0

    def play_round(self):
        player_card = self.player_deck.deal()
        ai_card = self.ai_deck.deal()
        self.round += 1

        if player_card.value > ai_card.value:
            return "Player wins this round"
        elif player_card.value < ai_card.value:
            return "AI wins this round"
        else:
            return "War!"
