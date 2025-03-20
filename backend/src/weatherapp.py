from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load API key from .env file
load_dotenv("api_key.env")
API_KEY = os.getenv("API_KEY")  # Read API_KEY from env file


def get_weather(city):
    """Fetches weather data from OpenWeather API for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature_celsius": data["main"]["temp"],
            "temperature_fahrenheit": (data["main"]["temp"] * 9 / 5) + 32,
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    else:
        return None


@app.route('/')
def home():
    """Serve the HTML page with the form."""
    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def weather_api():
    """API endpoint to get weather data. Usage: /weather?city=London"""
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is missing"}), 400

    weather_data = get_weather(city)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "City not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)  # Run Flask in debug mode