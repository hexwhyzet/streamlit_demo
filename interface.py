import asyncio
import os

import matplotlib.pyplot as plt
import streamlit as st

from analysis import sequential_calculations, load_data
from graph import plot_temperature
from weather_api import get_temperature_async


@st.cache_data
def cached_load_data(file):
    df = load_data(file)
    return df


st.title("Мониторинг температуры с аномалиями")

uploaded_file = st.file_uploader("Загрузите CSV-файл с историческими данными", type=["csv"])

if uploaded_file:
    seasonal_stats, df = sequential_calculations(cached_load_data(uploaded_file))
    st.write("Исторические данные загружены")

    cities = df["city"].unique()
    selected_city = st.selectbox("Выберите город", cities)

    city_data = df[df["city"] == selected_city]
    st.write("Описательная статистика:")
    st.write(city_data.describe())

    ALL_YEARS = "Все годы"
    df["year"] = df["timestamp"].dt.year
    years = sorted(df["year"].unique())
    selected_year = st.selectbox("Выберите год", [ALL_YEARS] + list(years))

    st.write("График температур")
    plot_temperature(df, selected_city, selected_year if selected_year != ALL_YEARS else None, show=False)
    st.pyplot(plt)

    api_key = st.text_input("Введите API-ключ OpenWeatherMap", type="password")

    if api_key:
        try:
            os.environ["API_KEY"] = api_key
            current_temp = asyncio.run(get_temperature_async(selected_city))

            st.write(f"Текущая температура в {selected_city}: {current_temp}°C")

            season = st.selectbox("Выберите сезон", city_data["season"].unique())
            season_data = seasonal_stats[(seasonal_stats["season"] == season) & (seasonal_stats["city"] == selected_city)]
            mean_temp = season_data["mean_temperature"].mean()
            std_temp = season_data["std_temperature"].mean()

            lower_bound = mean_temp - 2 * std_temp
            upper_bound = mean_temp + 2 * std_temp

            st.write(f"Средняя температура в {season}: {mean_temp:.2f}°C")
            st.write(f"Стандартное отклонение в {season}: {std_temp:.2f}°C")

            st.write(f"2 отклонения: от {lower_bound:.2f}°C до {upper_bound:.2f}°C")

            if lower_bound <= current_temp <= upper_bound:
                st.success(f"{current_temp}°C - Температура в пределах нормы.")
            else:
                st.error(f"{current_temp}°C - Аномальная температура!")
        except Exception as e:
            st.error(f"Ошибка при получении данных: {e}")
