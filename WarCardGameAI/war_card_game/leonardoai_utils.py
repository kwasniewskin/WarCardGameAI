import requests
import time

# Read API key from file
with open('ApiKeyLeonardoAi.txt', 'r') as file:
    api_key = file.read().strip()


def generateImagesToEachCardLeonardoAI(cards, theme):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    def generate_image(card):
        payload = {
            "alchemy": False,
            "height": 960,
            "modelId": "b24e16ff-06e3-43eb-8d33-4416c2d75876",
            "num_images": 1,
            "presetStyle": "CINEMATIC",
            "prompt": f"Create a {card.name} character in the style of {theme}. Use characteristics from this description: {card.description}.",
            "width": 640,
            "contrastRatio": None,
            "highResolution": False
        }

        response = requests.post('https://cloud.leonardo.ai/api/rest/v1/generations', headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        generation_id = response_data.get('sdGenerationJob', {}).get('generationId')

        if not generation_id:
            raise ValueError(f"Failed to get generation ID for card {card.name}")

        card.image_url = f'https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}'

    def fetch_image(card):
        if not card.image_url:
            raise ValueError(f"No image URL available for card {card.name}")

        get_response = requests.get(card.image_url, headers=headers)
        get_response.raise_for_status()
        generation_result = get_response.json()
        generated_images = generation_result.get('generations_by_pk', {}).get('generated_images', [])

        if not generated_images:
            raise ValueError(f"No images generated for card {card.name}")

        card.image_url = generated_images[0].get('url', 'URL not found')

    for card in cards:
        try:
            generate_image(card)
        except Exception as e:
            print(f"First attempt failed for {card.name}: {e}")
            try:
                print(f"Retrying image generation for {card.name}...")
                generate_image(card)
            except Exception as retry_e:
                print(f"Second attempt failed for {card.name}: {retry_e}")
                raise

    time.sleep(10)  # Wait for images to be generated

    for card in cards:
        try:
            fetch_image(card)
        except Exception as e:
            print(f"Failed to fetch image for {card.name}: {e}")
            raise
