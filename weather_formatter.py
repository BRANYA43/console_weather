import config
from weather_api_service import Weather

formatted_molds = {
    'en': ('{city}, {temperature}°C, {type}\n'
           'Sunrise: {sunrise}\n'
           'Sunset: {sunset}\n'),
    'ua': ('{city}, {temperature}°C, {type}\n'
           'Схід сонця: {sunrise}\n'
           'Захід сонця: {sunset}\n'),
}


def format_weather(weather: Weather):
    """Formats weather data in string"""
    ret = formatted_molds[config.LANG]
    ret = ret.format(
        city=weather.city,
        temperature=weather.temperature,
        type=weather.weather_type,
        sunrise=weather.sunrise.strftime('%H:%M'),
        sunset=weather.sunset.strftime('%H:%M'),
    )
    return ret


if __name__ == '__main__':
    from datetime import datetime
    from weather_api_service import WeatherType

    print(format_weather(Weather(
        temperature=25,
        weather_type=WeatherType.CLEAR,
        sunrise=datetime.fromisoformat('2022-05-03 04:00:00'),
        sunset=datetime.fromisoformat('2022-05-03 20:25:00'),
        city='Kharkov'
    )))
