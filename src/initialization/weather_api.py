import requests
import json

def fetch_weather(lat, lon, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}&lang=ru"
    try:
        with requests.get(url, timeout=5, stream=True) as response:
            response.raise_for_status()
            data = response.json()
        return {
            "wind_speed": round(data["current"]["wind_kph"] / 3.6, 1),
            "wind_direction": round(data["current"]["wind_degree"], 1),
            "wind_gust": round(data["current"].get("gust_kph", data["current"]["wind_kph"]) / 3.6, 1),
            "precipitation": round(data["current"]["precip_mm"], 1),
            "temperature": round(data["current"]["temp_c"], 1),
            "humidity": round(data["current"]["humidity"], 1),
            "pressure": round(data["current"]["pressure_mb"], 1),
            "cloud_cover": round(data["current"]["cloud"], 1),
            "uv_index": round(data["current"]["uv"], 1)
        }
    except requests.RequestException as e:
        return None