import os
import datetime


def create_project_structure():
    """
    Создание структуры проекта внутри существующего корня wind_turbine_maintenance.
    Выполнено: 26 июня 2025 года, 12:36 PM CEST.
    """
    # Список папок (относительные пути от корня)
    folders = [
        "src/initialization", "src/routing", "src/data_processing", "src/defect_detection",
        "src/failure_prediction", "src/simulation", "src/ui", "src/utils",
        "assets/models", "assets/textures", "assets/configs", "tests", "docs"
    ]

    # Список файлов по модулям
    files = {
        "src/initialization": ["data_generator.py", "weather_api.py", "historical_weather.py", "__init__.py"],
        "src/routing": ["aco_optimizer.py", "ga_optimizer.py", "route_manager.py", "__init__.py"],
        "src/data_processing": ["video_processor.py", "sensor_processor.py", "annotation.py", "__init__.py"],
        "src/defect_detection": ["yolo_detector.py", "resnet_classifier.py", "mask_rcnn.py", "__init__.py"],
        "src/failure_prediction": ["gru_model.py", "deepsurv_model.py", "prediction_manager.py", "__init__.py"],
        "src/simulation": ["unreal_bridge.cpp", "unreal_bridge.py", "visualization.py", "__init__.py"],
        "src/ui": ["main_window.py", "initialization_tab.py", "simulation_tab.py", "__init__.py"],
        "src/utils": ["logging_config.py", "json_utils.py", "__init__.py"],
        "src": ["main.py"],
        "assets/configs": ["weather_stats.json", "input_data.json"],
        "tests": ["test_initialization.py", "test_routing.py", "test_processing.py", "test_detection.py",
                  "test_prediction.py", "test_simulation.py"],
        "docs": ["api.md", "architecture.md", "user_manual.md"],
        ".": ["requirements.txt", "Dockerfile", "CMakeLists.txt", "README.md"]
    }

    # Создание папок
    created_folders = []
    for folder in folders:
        path = os.path.join(".", folder)
        if not os.path.exists(path):
            os.makedirs(path)
            created_folders.append(folder)
        else:
            print(f"Папка {path} уже существует, пропущена.")

    # Создание файлов
    created_files = []
    skipped_files = []
    for directory, file_list in files.items():
        for file_name in file_list:
            path = os.path.join(".", directory, file_name)
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    f.write("")  # Создание пустого файла
                created_files.append(path)
            else:
                skipped_files.append(path)

    # Вывод результатов
    if created_folders or created_files:
        print(f"Создано папок: {len(created_folders)} ({', '.join(created_folders)})")
        print(f"Создано файлов: {len(created_files)} ({', '.join(created_files)})")
    if skipped_files:
        print(f"Пропущено файлов (существуют): {len(skipped_files)} ({', '.join(skipped_files)})")
    print(f"Структура проекта успешно обновлена в {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S CEST')}.")


if __name__ == "__main__":
    create_project_structure()