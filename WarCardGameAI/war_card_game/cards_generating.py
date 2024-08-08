import os
import urllib.request
from war_card_game.custom_messagebox import show_custom_messagebox_with_retry
from war_card_game.leonardoai_utils import generateImagesToEachCardLeonardoAI
from war_card_game.openai_utils import generateCardsBasedOnGivenTheme
import sys


def generateCards(theme):
    try:
        Cards = generateCardsBasedOnGivenTheme(theme)
    except Exception as e:
        raise  # Propagate exception

    try:
        # generateImagesToEachCardOpenAi(Cards, theme)
        generateImagesToEachCardLeonardoAI(Cards, theme)
    except Exception as e:
        raise  # Propagate exception

    try:
        saveCardsImagesToAssets(Cards)
    except Exception as e:
        raise  # Propagate exception

    return Cards


def saveCardsImagesToAssets(cards):
    # Define the path to the card_images folder
    card_images_folder = os.path.join('assets', 'card_images')

    # Ensure the card_images folder exists
    try:
        os.makedirs(card_images_folder, exist_ok=True)
    except Exception as e:
        raise  # Propagate exception

    for card in cards:
        try:
            image_url = card.image_url
            file_path = os.path.join(card_images_folder, f"{card.id}.png")
            urllib.request.urlretrieve(image_url, file_path)
            print(f"{card.id}. {card.name} generated and saved to {file_path}")
            print(f"Power: {card.power}, Description: {card.description}")
        except Exception as e:
            raise  # Propagate exception
