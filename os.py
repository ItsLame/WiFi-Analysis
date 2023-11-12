import pandas as pd

df = pd.DataFrame()
df = pd.read_csv("merged_released.csv")

analysis_columns = ["os", "rssi", "network delay (ms)", "noise level"]
df_analysis = df[analysis_columns]

analysis_by_os = (
    df_analysis.groupby("os")
    .agg(
        {
            "rssi": ["mean", "std"],
            "network delay (ms)": ["mean", "std"],
            "noise level": ["mean", "std"],
        }
    )
    .reset_index()
)

analysis_by_os.columns = [
    "OS",
    "RSSI Mean",
    "RSSI Std",
    "Network Delay Mean",
    "Network Delay Std",
    "Noise Level Mean",
    "Noise Level Std",
]

print(analysis_by_os)
