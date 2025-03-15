import multiprocessing as mp
from multiprocessing.dummy import Pool as ThreadPool

import pandas as pd

from analysis import compute_rolling_stats, detect_anomalies, calculate_seasonal_stats, load_data


def process_city(city_df):
    city_df = compute_rolling_stats(city_df)
    city_df = detect_anomalies(city_df)
    return city_df


def parallel_process_calculations(df, num_workers=4):
    cities = df["city"].unique()
    city_dfs = [df[df["city"] == city].copy() for city in cities]

    with mp.Pool(processes=num_workers) as pool:
        results = pool.map(process_city, city_dfs)

    final_df = pd.concat(results, ignore_index=True)
    return calculate_seasonal_stats(final_df), final_df


def parallel_thread_calculations(df, num_workers=4):
    cities = df["city"].unique()
    city_dfs = [df[df["city"] == city].copy() for city in cities]

    with ThreadPool(num_workers) as pool:
        results = pool.map(process_city, city_dfs)

    final_df = pd.concat(results, ignore_index=True)
    return calculate_seasonal_stats(final_df), final_df


if __name__ == '__main__':
    file_path = "temperature_data.csv"

    seasonal_stats, df = parallel_thread_calculations(load_data(file_path))
    print(seasonal_stats.head(10))
