import os
import sys
import requests
from urllib.parse import quote as url_encode
from dotenv import load_dotenv
import tkinter as tk
import tkinter.messagebox


IMG_LOCATION = "lib"
IMG_BASE_NAME = "img_base.jpg"
IMG_CLEAN_NAME = "img_clean.jpg"


def get_api_key() -> str:
    """Gets api key from local environmental variables"""
    load_dotenv(os.path.join("lib", ".env"))
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        _invalid_api_key()
    return f'&key={API_KEY}'


def _invalid_api_key() -> None:
    """Handles invalid api key."""
    root = tk.Tk()
    root.withdraw()
    tkinter.messagebox.showerror(
        title="API Key NOT FOUND!",
        message="Cannot use google maps functionality. Follow instructions on github for using dotenv."
    )
    sys.exit()


def get_img_base(loc) -> bytes:
    """Gets the img with all the labels and markets to initially show"""

    base_url = 'https://maps.googleapis.com/maps/api/staticmap?'
    center = 'center='
    params = '&zoom=13&size=400x400&scale=2'
    KEY = get_api_key()
    url = base_url + center + loc + params + KEY
    img = requests.get(url).content

    return img


def write_img_base(img) -> None:
    """Saves image as file"""

    with open(os.path.join(IMG_LOCATION, IMG_BASE_NAME), 'wb') as \
            img_file:
        img_file.write(img)


def get_img_clean(loc) -> bytes:
    """Gets the cleaned up image for pygame insertion from the specified url"""

    base_url = 'https://maps.googleapis.com/maps/api/staticmap?'
    center = 'center='
    params = '&zoom=13&size=400x400&scale=2'
    style = '&style=feature:landscape|color:0x000000' \
            '&style=feature:poi|visibility:off' \
            '&style=feature:administrative|visibility:off' \
            '&style=feature:water|visibility:off' \
            '&style=feature:transit|visibility:off' \
            '&style=feature:road|element:labels|visibility:off'
    KEY = get_api_key()
    url = base_url + center + loc + params + url_encode(style, safe='/:&=') + KEY
    img = requests.get(url).content

    return img


def write_img_clean(img) -> None:
    """Saves image as file"""

    with open(os.path.join(IMG_LOCATION, IMG_CLEAN_NAME), 'wb') as img_file:
        img_file.write(img)


if __name__ == '__main__':
    b = get_img_base('Berkeley,CA')
    write_img_base(b)

    c = get_img_clean('Berkeley,CA')
    write_img_clean(c)
