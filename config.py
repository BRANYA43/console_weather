USE_ROUNDED_COORDS = True
LANG = 'ua'  # en, ua
OPENWEATHER_API_KEY = 'f18df0c691d5f84c88ba3d8e2c1765c4'
OPENWEATHER_URL = (
    'https://api.openweathermap.org/data/2.5/weather?'
    'lat={latitude}&lon={longitude}'
    '&appid=' + OPENWEATHER_API_KEY + f'&lang={LANG}'
    'units=metric'
)
