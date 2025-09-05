import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int
    feels_like: int
    humidity: int
    wind_speed: float
    sunrise: str
    sunset: str

@dataclass
class ForecastData:
    date: str
    temperature: int
    description: str
    icon: str


def get_lat_lon(city: str, state: str, country: str, api_key: str):
    """fetch latitude & longitude for city"""
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&appid={api_key}"
    resp = requests.get(url).json()
    if not resp:  # no city found
        return None, None
    loc = resp[0]
    return loc.get("lat"), loc.get("lon")



def get_current_weather(lat: float, lon: float, api_key: str, units: str = "metric") -> WeatherData:
    """fetch current weather"""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}"
    resp = requests.get(url).json()

    return WeatherData(
        main=resp["weather"][0]["main"],
        description=resp["weather"][0]["description"],
        icon=resp["weather"][0]["icon"],
        temperature=round(resp["main"]["temp"]),          # 🔹 round temp
        feels_like=round(resp["main"]["feels_like"]),     # 🔹 round feels_like
        humidity=resp["main"]["humidity"],
        wind_speed=resp["wind"]["speed"],
        sunrise=datetime.fromtimestamp(resp["sys"]["sunrise"]).strftime("%H:%M"),
        sunset=datetime.fromtimestamp(resp["sys"]["sunset"]).strftime("%H:%M"),
    )


def get_forecast(lat: float, lon: float, api_key: str, units: str = "metric"):
    """fetch 5-day forecast (daily at 12:00)"""
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units={units}"
    resp = requests.get(url).json()

    forecast_list = []
    for item in resp.get("list", []):
        if "12:00:00" in item["dt_txt"]:  # pick midday entries
            forecast_list.append(
                ForecastData(
                    date=item["dt_txt"].split()[0],
                    temperature=round(item["main"]["temp"]),  # 🔹 round forecast temp
                    description=item["weather"][0]["description"],
                    icon=item["weather"][0]["icon"],
                )
            )
    return forecast_list


def main(city: str, state: str, country: str, units: str = "metric"):
    """main wrapper: returns current + forecast"""
    lat, lon = get_lat_lon(city, state, country, API_KEY)
    if not lat or not lon:
        return None, None
    weather_data = get_current_weather(lat, lon, API_KEY, units)
    forecast_data = get_forecast(lat, lon, API_KEY, units)
    return weather_data, forecast_data
