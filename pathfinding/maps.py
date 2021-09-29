import os
import requests
from urllib.parse import quote as url_encode
from dotenv import load_dotenv


def get_api_key() -> str:
    """Gets api key from local environmental variables"""
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    return f'&key={API_KEY}'


def get_address_from_user() -> str:
    """Sets the address from user input"""
    address = input().strip()
    address = ', '.join(address.split())

    return address


def get_img_base() -> bytes:
    """Gets the img with all the labels and markets to initially show"""

    base_url = 'https://maps.googleapis.com/maps/api/staticmap?'
    loc = 'center=Berkeley,CA'
    params = '&zoom=13&size=400x400&scale=2'
    KEY = get_api_key()
    url = base_url + loc + params + KEY
    img = requests.get(url).content

    return img


def write_img_base(img) -> None:
    """Saves image as file"""

    with open('img_base.jpg', 'wb') as img_file:
        img_file.write(img)


def get_img_clean() -> bytes:
    """Gets the cleaned up image for pygame insertion from the specified url"""

    base_url = 'https://maps.googleapis.com/maps/api/staticmap?'
    loc = 'center=Berkeley,CA'
    params = '&zoom=13&size=400x400&scale=2'
    style = '&style=feature:landscape|color:0x000000' \
            '&style=feature:poi|visibility:off' \
            '&style=feature:administrative|visibility:off' \
            '&style=feature:water|visibility:off' \
            '&style=feature:transit|visibility:off' \
            '&style=feature:road|element:labels|visibility:off'
    KEY = get_api_key()
    url = base_url + loc + params + url_encode(style, safe='/:&=') + KEY
    img = requests.get(url).content

    return img


def write_img_clean(img) -> None:
    """Saves image as file"""

    with open('img_clean.jpg', 'wb') as img_file:
        img_file.write(img)


if __name__ == '__main__':
    b = get_img_base()
    write_img_base(b)

    c = get_img_clean()
    write_img_clean(c)
