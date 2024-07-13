import json


class Card:
    def __init__(self, id, name, power, description):
        self.id = id
        self.name = name
        self.power = power
        self.description = description

    def __str__(self):
        return f"Card(id={self.id}, name={self.name}, power={self.power}, description={self.description})"


def json_to_cards(json_data):
    cards_data = json.loads(json_data)
    cards = [Card(card["id"], card["name"], card["power"], card["description"]) for card in cards_data]

    return cards
