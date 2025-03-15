import asyncio
import os

import aiohttp
import requests

API_KEY = os.getenv('API_KEY')


def get_url(city):
    return f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('API_KEY')}&units=metric"


def get_temperature_sync(city):
    response = requests.get(get_url(city))
    if response.status_code == 200:
        data = response.json()
        return data["main"]["temp"]
    else:
        raise Exception(f"Ошибка запроса: {response.status_code}")


async def get_temperature_async(city):
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url(city)) as response:
            if response.status == 200:
                data = await response.json()
                return data["main"]["temp"]
            else:
                raise Exception(f"Ошибка запроса: {response.status}")


def is_temperature_normal(city, temperature, season, seasonal_stats):
    stat_row = seasonal_stats[(seasonal_stats['city'] == city) & (seasonal_stats['season'] == season)].iloc[0]
    mean_temperature = stat_row['mean_temperature']
    std_temperature = stat_row['std_temperature']

    return mean_temperature - 2 * std_temperature < temperature < mean_temperature + 2 * std_temperature


async def check_city(city, current_season, request_mode, seasonal_stats):
    if request_mode == "sync":
        temp = get_temperature_sync(city)
    elif request_mode == "async":
        temp = asyncio.run(get_temperature_async(city))
    else:
        print("Неверный режим. Используйте 'sync' или 'async'.")
        exit(1)

    print(f"Текущая температура в {city}: {temp}°C")
    if is_temperature_normal(city, temp, current_season, seasonal_stats):
        print("Температура в норме.")
    else:
        print("Аномальная температура!")
