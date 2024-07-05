import openai
from openai import OpenAI

userInput = "Wiedźmin"

# Read API key form file
with open('ApiKey.txt', 'r') as file:
    openai.api_key = file.read().strip()

client = OpenAI(api_key=openai.api_key)

#Generate Cards based on given theme
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "{\n  \"prompt\": \"Generate 30 unique game cards based on the theme given by user. Cards have to include iconic characters for that theme. Each card should include the following details: name, power in scale 1 to 10 based on importance of that character in that theme, and a detailed description of the card's appearance to help visualize it. The output should be in JSON format. Below is the structure for each card:\\n\\nCard Template:\\n{\\n  \\\"name\\\": \\\"<Name of the Card>\\\",\\n  \\\"power\\\": \\\"<Power of the Card in scale 1 to 10>\\\",\\n  \\\"description\\\": \\\"<Detailed description of what is depicted on the card>\\\"\\n}\\n\\nPlease generate the cards accordingly.\",\n  \"examples\": [\n    {\n      \"name\": \"Flame Dragon\",\n      \"power\": \"4\",\n      \"description\": \"A majestic dragon with scales of red and gold, breathing intense flames, with a background of a burning forest.\"\n    },\n    {\n      \"name\": \"Water Nymph\",\n      \"power\": \"7\",\n      \"description\": \"A serene nymph surrounded by swirling water, with a shimmering blue aura and a backdrop of a tranquil lake.\"\n    },\n    {\n      \"name\": \"Forest Guardian\",\n      \"power\": \"1\",\n      \"description\": \"A towering tree creature with vines and leaves, standing in a dense forest, exuding a protective and powerful presence.\"\n    }\n  ]\n}\n\n"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": f"{userInput}"
        }
      ]
    },
    ],
    temperature=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

Cards = response.choices[0].message.content
print(Cards)

#Generate Images to each card

