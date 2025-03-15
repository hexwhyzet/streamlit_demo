import matplotlib.pyplot as plt


def plot_temperature(df, city=None, year=None, show=True):
    plt.figure(figsize=(12, 6))

    if city is not None:
        df = df[df['city'] == city]

    if year is not None:
        df = df[df['year'] == year]

    plt.plot(df["timestamp"], df["temperature"], label="Temperature", alpha=0.5)
    plt.plot(df["timestamp"], df["rolling_mean"], label="Rolling Mean", color='red', linewidth=2)
    plt.fill_between(df["timestamp"], df["lower_bound"], df["upper_bound"], color='gray', alpha=0.2)
    plt.scatter(df["timestamp"], df["temperature"], c=df["anomaly"].map({True: 'red', False: 'blue'}),
                label="Is Anomaly (Red=Yes, Blue=No)")
    plt.xlabel("Date")
    plt.ylabel("Temperature (Celsius)")
    plt.title(f"Temperature Trends and Anomalies{(' in ' + city) if city is not None else ''}")
    plt.legend()

    if show:
        plt.show()
