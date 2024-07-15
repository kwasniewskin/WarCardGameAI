import os
import urllib.request

from war_card_game.leonardoai_utils import generateImagesToEachCardLeonardoAI
from war_card_game.openai_utils import generateCardsBasedOnGivenTheme, generateImagesToEachCardOpenAi

themeGivenByUser = "Wiedzmin"


# Generate cards based on the given theme, create images for them, and save the images to the assets folder.
def generateCards(theme):
    Cards = generateCardsBasedOnGivenTheme(theme)
    #generateImagesToEachCardOpenAi(Cards, theme)
    generateImagesToEachCardLeonardoAI(Cards, theme)
    saveCardsImagesToAssets(Cards)
    return Cards


# Save card images to the assets/card_images folder.
def saveCardsImagesToAssets(cards):
    # Define the path to the card_images folder
    card_images_folder = os.path.join('assets', 'card_images')

    # Ensure the card_images folder exists
    os.makedirs(card_images_folder, exist_ok=True)

    for card in cards:
        image_url = card.image_url
        file_path = os.path.join(card_images_folder, f"{card.id}.png")
        urllib.request.urlretrieve(image_url, file_path)
        print(f"{card.id}. {card.name} generated and saved to {file_path}")
        print(f"Power: {card.power}, Description: {card.description}")


cards = generateCards(themeGivenByUser)
#print(cards)

