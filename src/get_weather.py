import os
import requests
from dotenv import load_dotenv


load_dotenv(dotenv_path='api_key.env')

API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise ValueError("API_KEY not found in the environment variables.")


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return {
            "city_name": city_name,
            "temperature": temperature,
            "weather_description": weather_description,
            "humidity": humidity,
            "wind_speed": wind_speed
        }
    else:
        return None