import os
import requests
from dotenv import load_dotenv


def get_api_key() -> str:
    """Gets api key from local environmental variables"""
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    return f'&key={API_KEY}'


def get_img() -> bytes:
    """Gets the images from the specified url"""

    base_url = 'https://maps.googleapis.com/maps/api/staticmap?'
    params = 'center=Berkeley,CA&zoom=14&size=400x400'
    KEY = get_api_key()
    url = base_url + params + KEY

    img = requests.get(url).content

    return img


def write_img(img) -> None:
    """Saves image as file"""

    with open('img.jpg', 'wb') as img_file:
        img_file.write(img)
