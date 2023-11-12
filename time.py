import pandas as pd

pd.options.mode.chained_assignment = None

df = pd.read_csv("merged_released.csv")

df["datetime"] = pd.to_datetime(df["time"], unit="s")
df["datetime"] = df["datetime"].dt.tz_localize("UTC").dt.tz_convert("Australia/Sydney")
uniwide_df = df[df["ssid"].str.lower() == "uniwide"]

time_ranges = {
    "6am-11am": [6, 11],
    "12pm-5pm": [12, 17],
    "6pm-11pm": [18, 23],
    "12am-5am": [0, 5],
}

uniwide_df["time_range"] = pd.cut(
    uniwide_df["datetime"].dt.hour,
    bins=[0, 6, 12, 18, 24],
    labels=["12am-5am", "6am-11am", "12pm-5pm", "6pm-11pm"],
    right=False,
)

avg_rssi = (
    uniwide_df.groupby("time_range", observed=True)
    .agg(
        {
            "rssi": ["mean", "std"],
            "noise level": ["mean", "std"],
            "network delay (ms)": ["mean", "std"],
            "bssid": "count",
        }
    )
    .reset_index()
)
print(avg_rssi)
