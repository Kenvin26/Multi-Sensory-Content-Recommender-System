import requests
from datetime import datetime

# Get weather data from OpenWeatherMap

def get_weather(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather = {
                "main": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
            }
            return weather
        else:
            return {"error": data.get("message", "Failed to get weather")}
    except Exception as e:
        return {"error": str(e)}

# Get current local time (server time)
def get_local_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S") 