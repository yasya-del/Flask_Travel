from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

from search_delta import find_delta


def search_for_map(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": find_delta(toponym),
        "apikey": apikey,
        "pt": f'{toponym_longitude},{toponym_lattitude},pm2dom'
    }

    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    with open(f'static/img/{toponym_to_find}_map.png', 'wb') as f:
        f.write(response.content)
    return None