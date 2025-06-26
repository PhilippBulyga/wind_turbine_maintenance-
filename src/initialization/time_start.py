import json
import os

from weather_provider import fetch_weather
from turbine_generator import generate_turbines
from mission_uav_provider import get_uav_data, get_mission_data

def generate_input_payload():
    station_lat = 48.153877407374345
    station_lon = 40.275458225930116
    center_lat = 48.182975
    center_lon = 40.324120

    return {
        "weather": fetch_weather(station_lat, station_lon),
        "uav": get_uav_data(),
        "wind_turbines": generate_turbines(center_lat, center_lon),
        "mission": get_mission_data()
    }

def save_to_file(data: dict):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    output_path = os.path.join(project_root, "assets", "configs", "input_data.json")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.truncate(0)
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    payload = generate_input_payload()
    save_to_file(payload)
