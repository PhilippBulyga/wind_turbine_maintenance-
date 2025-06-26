import json
import numpy as np
from scipy.spatial.distance import cdist
import os
import logging

logging.basicConfig(level=logging.INFO)

def calculate_distance_matrix(turbines, weather):
    coords = np.array([[t["x"], t["y"]] for t in turbines])
    distances = cdist(coords, coords, metric='euclidean')
    distances = np.where(distances < 1e-10, 1e-10, distances)  # Избежание деления на ноль
    wind_impact = np.cos(np.radians(weather.get("wind_direction", 0))) * weather.get("wind_speed", 0) / 10
    return distances * (1 + wind_impact)

def ant_colony_optimization(turbines, priorities, drone_speed, n_ants=20, n_iterations=50, alpha=1.0, beta=2.0, rho=0.1):
    n_points = len(turbines)
    if n_points < 2:
        raise ValueError("Insufficient number of points for routing")
    weather = next((t for t in turbines if "wind_direction" in t), {"wind_direction": 0, "wind_speed": 0})
    distances = calculate_distance_matrix(turbines, weather)
    tau = np.ones((n_points, n_points)) / n_points  # Инициализация феромонов
    best_path, best_distance = None, float('inf')

    for _ in range(n_iterations):
        paths = []
        for _ in range(n_ants):
            visited = np.zeros(n_points, dtype=bool)
            path = [np.random.randint(0, n_points)]
            visited[path[0]] = True
            while not visited.all():
                current = path[-1]
                probs = (tau[current] ** alpha) * ((1.0 / distances[current]) ** beta) * np.array([priorities.get(i+1, 0.5) if not visited[i] else 0 for i in range(n_points)])
                probs = np.where(probs == 0, 1e-10, probs)
                if probs.sum() == 0:
                    break
                next_point = np.random.choice(n_points, p=probs / probs.sum())
                path.append(next_point)
                visited[next_point] = True
            paths.append(path)

        for path in paths:
            distance = np.sum([distances[path[i], path[(i+1) % n_points]] for i in range(len(path))])
            if distance < best_distance:
                best_distance = distance
                best_path = path

        tau *= (1 - rho)  # Испарение феромонов
        for path in paths:
            distance = np.sum([distances[path[i], path[(i+1) % n_points]] for i in range(len(path))])
            contribution = 1.0 / distance if distance > 0 else 0
            for i in range(len(path)):
                tau[path[i], path[(i+1) % n_points]] += contribution

    if best_path is None:
        raise RuntimeError("No valid path found")
    route = [turbines[i] | {"priority": priorities.get(i+1, 0.5), "time": f"2025-06-26T{17+i//2:02d}:00:00Z"} for i in best_path] + [turbines[best_path[0]]]
    return {"route": route, "metrics": {"length": best_distance, "time": best_distance / drone_speed, "coverage": 1.0}}

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    input_path = os.path.join(project_root, "assets", "configs", "input_data.json")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input data file not found at {input_path}")
    logging.info(f"Loading input data from: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)
    priorities = {p["id"]: p["priority"] for p in input_data["priorities"]}
    drone_speed = input_data["drone_params"]["speed"]
    weather = input_data["weather"] if input_data.get("weather") else {}
    route = ant_colony_optimization(input_data["turbines"], priorities, drone_speed)
    output_path = os.path.join(project_root, "assets", "configs", "route.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(route, f, indent=4)
    logging.info("Route calculated: %s", route["metrics"])
    print(json.dumps(route, indent=4))