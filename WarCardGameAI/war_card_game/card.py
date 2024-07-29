import json


class Card:
    def __init__(self, id, name, power, description, image_url):
        self.id = id
        self.name = name
        self.power = int(power)  # Ensure power is an integer
        self.description = description
        self.image_url = image_url

    def __str__(self):
        return f"Card(id={self.id}, name={self.name}, power={self.power}, description={self.description}, image_url={self.image_url})"


def json_to_cards(json_data):
    cards_data = json.loads(json_data)
    cards = [Card(card["id"], card["name"], int(card["power"]), card["description"], card["image_url"]) for card in
             cards_data]

    return cards
