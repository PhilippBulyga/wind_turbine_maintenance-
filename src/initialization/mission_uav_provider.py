def get_uav_data() -> dict:
    return {
        "model_id": "UAV_X100",
        "flight_time_min": 40,
        "max_range_km": 12.5,
        "cruise_speed_mps": 12.0,
        "payload_capacity_kg": 1.5,
        "camera": {
            "model": "Sony Alpha 7R IV",
            "fov_deg": 78,
            "resolution": "9504x6336",
            "sensor_size_mm": [35.9, 24.0],
            "zoom": "fixed"
        }
    }

def get_mission_data() -> dict:
    return {
        "mission_id": "M_001",
        "type": "full_inspection",
        "constraints": {
            "max_duration_min": 30,
            "weather_thresholds": {
                "wind_speed_max": 15,
                "precipitation_max": 2.0,
                "temperature_min": -5,
                "temperature_max": 35
            }
        }
    }
