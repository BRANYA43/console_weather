#!/usr/bin/env python3.10
from pathlib import Path

from coordinates import get_gps_coordinates
from exceptions import CantGetCoordinates, ApiServiceError
from history import save_weather, PlainFileWeatherStorage, JSONFileWeatherStorage
from weather_api_service import get_weather
from weather_formatter import format_weather


def main():
    try:
        coordinates = get_gps_coordinates()
    except CantGetCoordinates:
        print('Do not get GPS coordinates.')
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print('Do not get weather from weather service API.')
        exit(1)
    save_weather(
        weather,
        JSONFileWeatherStorage(Path.cwd() / 'history.json')
    )
    print(format_weather(weather))


if __name__ == '__main__':
    main()
