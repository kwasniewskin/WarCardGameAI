import openai

# Read API key form file
with open('war_card_game/ApiKey.txt', 'r') as file:
    openai.api_key = file.read().strip()
