import requests
from datetime import datetime

API_KEY = "c8c007f36b6c4e5d99e92230252606"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def fetch_weather(lat: float, lon: float) -> dict:
    params = {"key": API_KEY, "q": f"{lat},{lon}", "aqi": "no"}
    response = requests.get(BASE_URL, params=params, timeout=5)
    data = response.json()["current"]
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "location": {"latitude": lat, "longitude": lon},
        "parameters": {
            "wind_speed": data["wind_kph"] / 3.6,
            "wind_direction": data["wind_degree"],
            "wind_gust": data.get("gust_kph", 0.0) / 3.6,
            "precipitation": data.get("precip_mm", 0.0),
            "temperature": data["temp_c"],
            "humidity": data["humidity"],
            "pressure": data["pressure_mb"],
            "cloud_cover": data.get("cloud", 0),
            "uv_index": data.get("uv", 0.0),
            "illumination": data.get("uv", 0.0) * 100.0
        },
        "source": "WeatherAPI.com"
    }
