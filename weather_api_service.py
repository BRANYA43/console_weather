from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import json
from json.decoder import JSONDecodeError
import ssl
from typing import Literal
import urllib.request
from urllib.error import URLError
from coordinates import Coordinates
import config
from exceptions import ApiServiceError

Celsius = int


class WeatherType(str, Enum):
    if config.LANG == 'en':
        THUNDERSTORM = 'Thunderstorm'
        DRIZZLE = 'Drizzle'
        RAIN = 'Rain'
        SNOW = 'Snow'
        CLEAR = 'Clear'
        FOG = 'Fog'
        CLOUDS = 'Clouds'
    elif config.LANG == 'ua':
        THUNDERSTORM = 'Блискавка'
        DRIZZLE = 'Мороз'
        RAIN = 'Дощ'
        SNOW = 'Сніг'
        CLEAR = 'Ясно'
        FOG = 'Туман'
        CLOUDS = 'Хмарно'


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(coordinates)
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(coordinates: Coordinates) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(latitude=coordinates.latitude, longitude=coordinates.longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_response = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(openweather_response),
        weather_type=_parse_weather_type(openweather_response),
        sunrise=_parse_sun_time(openweather_response, 'sunrise'),
        sunset=_parse_sun_time(openweather_response, 'sunset'),
        city=_parse_city(openweather_response),
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict['main']['temp'])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (IndexError, KeyError):
        raise ApiServiceError

    weather_type = {
        '1': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.FOG,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS,
    }
    for _id, _weather_type in weather_type.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_sun_time(openweather_dict: dict, time: Literal['sunrise'] | Literal['sunset']) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict['name']


if __name__ == '__main__':
    print(get_weather(Coordinates(latitude=49.9, longitude=36.2)))
