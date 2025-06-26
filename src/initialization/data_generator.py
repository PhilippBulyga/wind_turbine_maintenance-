import numpy as np
import json
import requests
from .weather_api import fetch_weather
from .historical_weather import fetch_historical_weather

def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=1)
        return True
    except requests.RequestException:
        return False

def generate_turbine_coordinates():
    center_lat, center_lon = 48.182975, 40.324120
    step_m, deviation_m = 700, 50
    step_lat = step_m / 111000
    step_lon = step_m / (111000 * np.cos(np.radians(center_lat)))
    deviation_lat, deviation_lon = deviation_m / 111000, deviation_m / (111000 * np.cos(np.radians(center_lat)))
    turbines = [dict(id=i+1, x=round(center_lon + (j-(9)/2)*step_lon + np.random.normal(0, deviation_lon/2), 6),
                     y=round(center_lat + (i-(5)/2)*step_lat + np.random.normal(0, deviation_lat/2), 6), z=z)
                for i in range(6) for j in range(10) for z in [87.0, 130.0]]
    return turbines

def generate_drone_params():
    return {
        "flight_time": round(np.random.uniform(20, 60), 1),
        "max_distance": round(np.random.uniform(5, 20), 1),
        "speed": round(np.random.uniform(5, 15), 1)
    }

def generate_priorities(turbine_count):
    priorities = [dict(id=i+1, priority=round(np.clip(np.random.normal(0.5, 0.2), 0, 1), 1))
                  for i in range(turbine_count)]
    for p in priorities:
        if p["id"] % 2 == 0:  # Лопасти имеют более высокий приоритет
            p["priority"] = min(p["priority"] + 0.3, 1.0)
    return priorities

def generate_weather_rostov_historical(stats=None):
    if stats is None:
        stats = {"wind_speed": {"mean": 6, "std": 2.5}, "wind_direction": {"mean": 180, "std": 90},
                 "wind_gust": {"mean": 8, "std": 3}, "precipitation": {"mean": 0.5, "std": 0.8},
                 "temperature": {"mean": 15, "std": 8}, "humidity": {"mean": 60, "std": 15},
                 "pressure": {"mean": 1000, "std": 10}, "cloud_cover": {"mean": 50, "std": 25},
                 "uv_index": {"mean": 4, "std": 2}}
    wind_speed = np.clip(np.random.normal(stats["wind_speed"]["mean"], stats["wind_speed"]["std"]), 0, 15)
    wind_gust = np.clip(np.random.normal(stats["wind_gust"]["mean"], stats["wind_gust"]["std"]), wind_speed, 20)
    return {
        "wind_speed": round(wind_speed, 1),
        "wind_direction": round(np.random.uniform(0, 360), 1),
        "wind_gust": round(wind_gust, 1),
        "precipitation": round(np.clip(np.random.normal(stats["precipitation"]["mean"], stats["precipitation"]["std"]), 0, 3), 1),
        "temperature": round(np.clip(np.random.normal(stats["temperature"]["mean"], stats["temperature"]["std"]), -10, 35), 1),
        "humidity": round(np.clip(np.random.normal(stats["humidity"]["mean"], stats["humidity"]["std"]), 30, 90), 1),
        "pressure": round(np.clip(np.random.normal(stats["pressure"]["mean"], stats["pressure"]["std"]), 980, 1020), 1),
        "cloud_cover": round(np.random.uniform(0, 100), 1),
        "uv_index": round(np.clip(np.random.normal(stats["uv_index"]["mean"], stats["uv_index"]["std"]), 0, 10), 1)
    }

def generate_input_data(lat=48.153877407374345, lon=40.275458225930116, api_key=None):
    online = check_internet_connection()
    weather = (fetch_historical_weather(lat, lon, api_key, 7) and generate_weather_rostov_historical(fetch_historical_weather(lat, lon, api_key, 7))) if online and api_key else generate_weather_rostov_historical()
    if online and api_key:
        weather = fetch_weather(lat, lon, api_key) or weather
    turbines = generate_turbine_coordinates()
    drone_params = generate_drone_params()
    priorities = generate_priorities(len(turbines) // 2)
    data = {"weather": weather, "turbines": turbines, "drone_params": drone_params, "priorities": priorities}
    with open("input_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return data

if __name__ == "__main__":
    lat, lon = 48.153877407374345, 40.275458225930116
    api_key = "c8c007f36b6c4e5d99e92230252606"
    input_data = generate_input_data(lat, lon, api_key)
    print(json.dumps(input_data, indent=4))