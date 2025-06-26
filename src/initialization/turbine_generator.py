import random
import math


def generate_turbines(center_lat: float, center_lon: float,
                      rows: int = 6, cols: int = 10,
                      step_m: int = 700, deviation_m: int = 50) -> list:
    lat_step = step_m / 111000
    lon_step = step_m / (111000 * abs(math.cos(math.radians(center_lat))))
    deviation_lat = deviation_m / 111000
    deviation_lon = deviation_m / (111000 * abs(math.cos(math.radians(center_lat))))

    turbines = []
    for i in range(rows):
        for j in range(cols):
            lat = center_lat + (i - rows // 2) * lat_step + random.uniform(-deviation_lat, deviation_lat)
            lon = center_lon + (j - cols // 2) * lon_step + random.uniform(-deviation_lon, deviation_lon)

            idx = i * cols + j + 1
            tid = f"WT_{idx:03d}"
            turbines.append({
                "id": tid,
                "location": {"latitude": round(lat, 7), "longitude": round(lon, 7)},
                "priority": random.randint(1, 3),
                "safe_distance_m": 20,
                "geometry": {
                    "tower_height_m": 80,
                    "blade_length_m": 45,
                    "hub_height_m": 90
                },
                "inspection_points": [
                    {
                        "point_id": f"{tid}_HUB",
                        "relative_position": "hub",
                        "offset_m": [0, 0, 90]
                    },
                    {
                        "point_id": f"{tid}_BLADE_TIP",
                        "relative_position": "blade_tip",
                        "offset_m": [0, 45, 90]
                    }
                ]
            })
    return turbines
