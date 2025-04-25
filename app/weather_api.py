 # Function for fetching weather data

import aiohttp
import asyncio

async def get_coordinates(city_name, api_key):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {'q': city_name, 'limit': 1, 'appid': api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as api_response:
            if api_response.status == 200:
                data = await api_response.json()
                if data:
                    latitude, longitude = data[0]['lat'], data[0]['lon']
                    return latitude, longitude
                else:
                    print("❌ City not found")
                    return None, None
            else:
                print(f"❌ Error {api_response.status}")
                return None, None

import random
from datetime import datetime, timedelta

# Weather code to irradiation score range mapping
irradiation_score_range = {
    # Thunderstorm (very low sunlight)
    200: (50, 70), 201: (45, 65), 202: (40, 60),
    210: (55, 75), 211: (50, 70), 212: (40, 60),
    221: (45, 65), 230: (55, 75), 231: (50, 70), 232: (40, 60),

    # Drizzle (low sunlight)
    300: (90, 110), 301: (80, 100), 302: (70, 90),
    310: (85, 105), 311: (75, 95), 312: (65, 85),
    313: (70, 90), 314: (60, 80), 321: (80, 100),

    # Rain (moderate to low sunlight)
    500: (110, 130), 501: (100, 120), 502: (80, 100),
    503: (70, 90), 504: (60, 80), 511: (50, 70),
    520: (90, 110), 521: (85, 105), 522: (75, 95),
    531: (80, 100),

    # Snow (very low sunlight)
    600: (90, 110), 601: (80, 100), 602: (60, 80),
    611: (75, 95), 612: (70, 90), 613: (65, 85),
    615: (60, 80), 616: (50, 70), 620: (75, 95),
    621: (65, 85), 622: (55, 75),

    # Atmosphere (mist, fog, etc. - very low)
    701: (100, 120), 711: (80, 100), 721: (110, 130),
    731: (85, 105), 741: (90, 110), 751: (80, 100),
    761: (75, 95), 762: (70, 90), 771: (60, 80),
    781: (40, 60),

    # Clear (max sunlight)
    800: (700, 750),

    # Clouds (reduces sunlight based on %)
    801: (550, 650), 802: (450, 550),
    803: (300, 400), 804: (150, 250),
}


async def get_weather_forecast(lat, lon, cnt, api_key):
    forecast_api = "http://api.openweathermap.org/data/2.5/forecast/daily"
    params = {'lat': lat, 'lon': lon, 'cnt': cnt, 'appid': api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(forecast_api, params=params) as api_response:
            if api_response.status == 200:
                data = await api_response.json()
                print("🌦 Weather Forecast Data:")
                parameter_arr = []

                start_date = datetime.now()  # Today's date

                for i, day in enumerate(data.get('list', [])):
                    date_forecast = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")  # Increment by 1 day
                    
                    temp = day['temp']['day']
                    humidity = day['humidity'] * 10
                    air_pressure = day['pressure']
                    windspeed = day['speed']
                    weather_code = day['weather'][0]['id']
                    weather_description = day['weather'][0]['description']

                    # Get irradiation score using the weather code
                    irradiation_range = irradiation_score_range.get(weather_code)
                    if irradiation_range:
                        irradiation = random.randint(*irradiation_range)
                    else:
                        irradiation = 'Unknown'

                    # Append the data
                    parameter_arr.append({
                        'Date': date_forecast,
                        'AirTemperature': temp,
                        'RelativeAirHumidity': humidity,
                        'AirPressure': air_pressure,
                        'WindSpeed': windspeed,
                        'WeatherCode': weather_code,
                        'WeatherDescription': weather_description,
                        'Radiation': irradiation,
                        'Sunshine': 11,  # This can be adjusted if needed
                    })

                return parameter_arr
            else:
                print(f"❌ Error: {api_response.status}")
                return []
