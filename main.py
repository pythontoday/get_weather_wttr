import requests
from typing import Optional
import argparse
import json


def get_weather(location: str='Новосибирск') -> None:
    """
    Получает данные о погоде для указанного города в формате JSON
    и выводит информацию в терминал
    
    :param location: Название города(по умолчанию: Новосибирск)
    """

    url: str = f"https://wttr.in/{location}?format=j1&lang=ru"

    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()
        data: dict = response.json()

        with open('data.txt', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        current: dict = data['current_condition'][0]

        temperature: str = current['temp_C']
        wind_speed: str = current['windspeedKmph']
        humidity: str = current['humidity']
        pressure: str = current['pressure']
        visibility: str = current['visibility']
        description: str = current['lang_ru'][0]['value']

        print(f"""
        ☁️ Погода в {location.title()}:
        🌡️  Температура: {temperature}°C
        📝 Описание: {description}
        💨 Ветер: {wind_speed} км/ч
        💧 Влажность: {humidity}%
        📈 Давление: {pressure} мбар
        👁️  Видимость: {visibility} км
        """)        

    except requests.RequestException as e:
        print("[X] Ошибка при запросе:", e)
    except KeyError:
        print("[X] Ошибка в формате данных:", e)


def save_weather_image(location: str, filename: Optional[str] = None) -> None:
    """
    Сохраняет PNG-картинку с погодой из сервиса wttr.in
    
    :param location: Город
    :param filename: Имя выходного файла (если не задано - по умолчанию <город>.png)
    """

    encoded_location: str = location.replace(" ", "+")
    url: str = f"https://wttr.in/{encoded_location}.png?lang=ru"
    filename = filename or f"{location}.png"

    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()

        with open(filename, 'wb') as file:
            file.write(response.content)

        print(f'[+] Картинка сохранена как "{filename}"')
    except requests.RequestException as e:
        print("[X] Ошибка при загрузке изображения:", e)


def main() -> None:
    """Основная точка входа в программу с поддержкой аргументов командной строки."""

    parser = argparse.ArgumentParser(
        description="🛰 Утилита для получения прогноза погоды с wttr.in"
    )
    parser.add_argument(
        "-c", "--city",
        type=str,
        default="Новосибирск",
        help="Город, для которого нужно узнать погоду(по умолчанию: Новосибирск)"
    )
    parser.add_argument(
        "--image",
        action="store_true",
        help="Сохранять изображение с погодой в PNG"
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="Имя файла для сохранения картинки (по умолчанию: <city>.png)"
    )
    
    args = parser.parse_args()
    get_weather(args.city)

    if args.image:
        save_weather_image(args.city, args.filename)


if __name__ == "__main__":
    main()
