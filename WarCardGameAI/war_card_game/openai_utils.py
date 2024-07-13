import os

import openai
from openai import OpenAI
import urllib.request
from war_card_game.card import json_to_cards

themeGivenByUser = "Apocalyptic World"

# Read API key form file
with open('ApiKey.txt', 'r') as file:
    openai.api_key = file.read().strip()

# Read CardGeneratingPrompt from file
with open('CardsGeneratingPrompt.txt', 'r') as file:
    CardGeneratingPrompt = file.read().strip()

client = OpenAI(api_key=openai.api_key)

def GenerateCardsBasedOnGivenTheme(theme):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"{CardGeneratingPrompt}"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{theme}"
                    }
                ]
            },
        ],
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content


def GenerateImagesToEachCard(Cards):
    # Define the path to the card_images folder
    card_images_folder = os.path.join('assets', 'card_images')

    # Ensure the card_images folder exists
    os.makedirs(card_images_folder, exist_ok=True)

    for card in Cards:
        # Create a prompt for each card
        prompt = f"Create a {card.name} in the style of {themeGivenByUser}."
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Save the image
        image_url = response.data[0].url
        file_path = os.path.join(card_images_folder, f"{card.id}.jpg")
        urllib.request.urlretrieve(image_url, file_path)
        print(f"{card.id}. {card.name} generated and saved to {file_path}")
        print(f"Power: {card.power}, Description: {card.description}")


Cards = json_to_cards(GenerateCardsBasedOnGivenTheme(themeGivenByUser))
GenerateImagesToEachCard(Cards)
