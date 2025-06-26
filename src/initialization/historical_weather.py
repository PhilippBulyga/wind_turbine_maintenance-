import requests
import numpy as np
import json
from datetime import datetime, timedelta

def fetch_historical_weather(lat, lon, api_key, days=15):
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"http://api.weatherapi.com/v1/history.json?key={api_key}&q={lat},{lon}&dt={start_date}&end_dt={end_date}&lang=ru"
    try:
        with requests.get(url, timeout=10, stream=True) as response:
            response.raise_for_status()
            data = response.json()
        hourly_data = np.array([[h["wind_kph"] / 3.6, h["wind_degree"], h.get("gust_kph", h["wind_kph"]) / 3.6,
                                h["precip_mm"], h["temp_c"], h["humidity"], h["pressure_mb"], h["cloud"], h["uv"]]
                               for day in data["forecast"]["forecastday"] for h in day["hour"]])
        stats = {k: {"mean": float(np.mean(hourly_data[:, i])), "std": float(np.std(hourly_data[:, i]))}
                 for i, k in enumerate(["wind_speed", "wind_direction", "wind_gust", "precipitation",
                                        "temperature", "humidity", "pressure", "cloud_cover", "uv_index"])}
        with open("weather_stats.json", "w", encoding="utf-8") as f:
            json.dump(stats, f)
        return stats
    except requests.RequestException:
        return None