import requests
import time

# Read API key form file
with open('ApiKeyLeonardoAi.txt', 'r') as file:
    api_key = file.read().strip()


def generateImagesToEachCardLeonardoAI(cards, theme):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    for card in cards:
        payload = {
            "alchemy": False,
            "height": 960,
            "modelId": "b24e16ff-06e3-43eb-8d33-4416c2d75876",
            "num_images": 1,
            "presetStyle": "CINEMATIC",
            "prompt": f"Create a {card.name} character in the style of {theme}.Use characteristics from this description: {card.description}.",
            "width": 640,
            "contrastRatio": None,
            "highResolution": False
        }

        response = requests.post('https://cloud.leonardo.ai/api/rest/v1/generations', headers=headers, json=payload)
        response_data = response.json()
        generation_id = response_data.get('sdGenerationJob', {}).get('generationId')
        get_url = f'https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}'
        card.image_url = get_url

    time.sleep(10)

    for card in cards:
        get_response = requests.get(card.image_url, headers=headers)
        generation_result = get_response.json()

        generated_images = generation_result.get('generations_by_pk', {}).get('generated_images', [])
        for image in generated_images:
            card.image_url = image.get('url', 'URL not found')
