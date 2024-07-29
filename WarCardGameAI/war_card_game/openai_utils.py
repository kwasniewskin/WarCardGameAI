import openai
from openai import OpenAI
from war_card_game.card import json_to_cards

# Read API key form file
with open('ApiKeyOpenAi.txt', 'r') as file:
    openai.api_key = file.read().strip()

# Read CardGeneratingPrompt from file
with open('CardsGeneratingPrompt.txt', 'r') as file:
    CardGeneratingPrompt = file.read().strip()

client = OpenAI(api_key=openai.api_key)


# Generate card details based on the given theme using the gpt-4o-mini model and convert the response to card objects
def generateCardsBasedOnGivenTheme(theme):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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

    return json_to_cards(response.choices[0].message.content)


# Generate image for each card in the specified theme and update the card's imageUrl attribute
def generateImagesToEachCardOpenAi(cards, theme):
    for card in cards:
        prompt = f"Create a {card.name} character in the style of {theme}.Use this characteristics from description: {card.description}. Keep image in photorealistic style."
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        card.image_url = response.data[0].url
