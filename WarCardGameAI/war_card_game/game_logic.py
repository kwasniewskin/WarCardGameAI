import random
from war_card_game.card import Card
from war_card_game.cards_generating import generateCards


class Player:
    def __init__(self, deck):
        self.deck = deck
        self.active_card = None

    def play_card(self):
        self.active_card = self.deck.deal()
        return self.active_card

    def win_cards(self, cards):
        for card in cards:
            self.deck.addCard(card)
        self.deck.updateNumberOfCards()  # Ensure the number of cards is updated


class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.updateNumberOfCards()

    def isDeckEmpty(self):
        return len(self.cards) == 0

    def deal(self):
        if not self.isDeckEmpty():
            card = self.cards.pop()
            self.updateNumberOfCards()
            return card

    def addCard(self, card):
        self.cards.insert(0, card)
        self.updateNumberOfCards()

    def updateNumberOfCards(self):
        self.number_of_cards = len(self.cards)


class Game:
    def __init__(self, userTheme):
        all_cards = generateCards(userTheme)
        random.shuffle(all_cards)

        half = len(all_cards) // 2
        player_cards = all_cards[:half]
        opponent_cards = all_cards[half:]

        self.all_cards = all_cards
        self.player = Player(Deck(player_cards))
        self.opponent = Player(Deck(opponent_cards))
        self.round = 0
        self.alert = ""
        self.winner = None

    def play_round(self):
        self.alert = ""
        self.round += 1

        if self.check_empty_deck():
            return

        player_card = self.player.play_card()
        opponent_card = self.opponent.play_card()

        if player_card.power > opponent_card.power:
            self.alert = "Player WON!"
            self.player.win_cards([player_card, opponent_card])
        elif player_card.power < opponent_card.power:
            self.alert = "Opponent WON!"
            self.opponent.win_cards([player_card, opponent_card])
        else:
            self.alert = "WAR!"
            self.war(player_card, opponent_card)

        self.player.deck.updateNumberOfCards()
        self.opponent.deck.updateNumberOfCards()

    def war(self, player_first_card, opponent_first_card):
        if self.check_empty_deck():
            return

        player_bonus_card = self.player.play_card()
        opponent_bonus_card = self.opponent.play_card()

        if self.check_empty_deck():
            return

        player_second_card = self.player.play_card()
        opponent_second_card = self.opponent.play_card()

        winner_deck = [
            player_first_card, opponent_first_card,
            player_bonus_card, opponent_bonus_card,
            player_second_card, opponent_second_card
        ]

        if player_second_card.power > opponent_second_card.power:
            self.alert = "Player WON a WAR!"
            self.player.win_cards(winner_deck)
        elif opponent_second_card.power > player_second_card.power:
            self.alert = "Opponent WON a WAR!"
            self.opponent.win_cards(winner_deck)
        else:
            self.alert = "ANOTHER WAR!"
            self.war(player_second_card, opponent_second_card)

    def check_empty_deck(self):
        if self.player.deck.isDeckEmpty():
            self.alert = "Opponent WINS the game!"
            self.winner = "Opponent"
            return True
        if self.opponent.deck.isDeckEmpty():
            self.alert = "Player WINS the game!"
            self.winner = "Player"
            return True
        return False
