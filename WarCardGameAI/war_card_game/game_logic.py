import random
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
        return None

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
        self.current_war_cards = None
        self.round = 0
        self.alert = ""
        self.winner = None

    def play_round(self):
        self.alert = ""
        self.round += 1

        player_card = self.player.play_card()
        opponent_card = self.opponent.play_card()
        if self.check_if_the_game_has_ended(player_card, opponent_card):
            return

        if player_card.power > opponent_card.power:
            self.alert = "Player WON!"
            self.player.win_cards([player_card, opponent_card])
            return "normal_player_win"
        elif player_card.power < opponent_card.power:
            self.alert = "Opponent WON!"
            self.opponent.win_cards([player_card, opponent_card])
            return "normal_opponent_win"
        else:
            self.alert = "WAR!"
            self.current_war_cards = [player_card, opponent_card]
            return "war_trigger"

    def war_step(self, step):
        if step == 1:
            # Place the bonus cards
            player_bonus_card = self.player.play_card()
            opponent_bonus_card = self.opponent.play_card()
            if self.check_if_the_game_has_ended(player_bonus_card, opponent_bonus_card):
                return
            self.current_war_cards += [player_bonus_card, opponent_bonus_card]
            return "war_bonus_applied"
        elif step == 2:
            # Determine the winner
            player_deciding_card = self.player.play_card()
            opponent_deciding_card = self.opponent.play_card()
            if self.check_if_the_game_has_ended(player_deciding_card, opponent_deciding_card):
                return
            self.player.active_card = player_deciding_card
            self.opponent.active_card = opponent_deciding_card
            self.current_war_cards += [player_deciding_card, opponent_deciding_card]

            if player_deciding_card.power > opponent_deciding_card.power:
                self.player.win_cards(self.current_war_cards)
                return "war_player_win"
            elif opponent_deciding_card.power > player_deciding_card.power:
                self.opponent.win_cards(self.current_war_cards)
                return "war_opponent_win"
            else:
                # Potentially trigger another war
                #return "war_tie"
                self.player.win_cards(self.current_war_cards)
                return "war_player_win"

    def check_if_the_game_has_ended(self, player_card, opponent_card):
        if player_card is None:
            self.alert = "Opponent WINS the game!"
            self.winner = "Opponent"
            return True
        if opponent_card is None:
            self.alert = "Player WINS the game!"
            self.winner = "Player"
            return True
