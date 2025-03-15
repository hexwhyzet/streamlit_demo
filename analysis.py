import pandas as pd


def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=["timestamp"])
    df.sort_values("timestamp", inplace=True)
    df.drop_duplicates(subset=["timestamp"], keep="first", inplace=True)
    return df


def compute_rolling_stats(df, window_size=30):
    df["rolling_mean"] = df.groupby("city")["temperature"].transform(
        lambda x: x.rolling(window=window_size, min_periods=1).mean())
    df["rolling_std"] = df.groupby("city")["temperature"].transform(
        lambda x: x.rolling(window=window_size, min_periods=1).std())
    return df


def detect_anomalies(df, threshold=2):
    df["upper_bound"] = df["rolling_mean"] + threshold * df["rolling_std"]
    df["lower_bound"] = df["rolling_mean"] - threshold * df["rolling_std"]
    df["anomaly"] = (df["temperature"] > df["upper_bound"]) | (df["temperature"] < df["lower_bound"])
    return df


def calculate_seasonal_stats(df):
    seasonal_stats = df.groupby(["city", "season"]).agg(
        mean_temperature=("temperature", "mean"),
        std_temperature=("temperature", "std")
    ).reset_index()
    return seasonal_stats


def sequential_calculations(df):
    df = compute_rolling_stats(df)
    df = detect_anomalies(df)
    seasonal_stats = calculate_seasonal_stats(df)
    return seasonal_stats, df


if __name__ == '__main__':
    file_path = "temperature_data.csv"

    seasonal_stats, df = sequential_calculations(load_data(file_path))
    seasonal_stats.head(10)
