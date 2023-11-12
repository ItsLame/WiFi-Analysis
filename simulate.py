import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

pd.options.mode.chained_assignment = None

# load the dataset
file_path = "merged_released.csv"
df = pd.read_csv(file_path)
df = df[df["ssid"].str.lower() == "uniwide"]


# analyze RSSI, network delays, etc., to understand network performance
def analyze_network_performance(df):
    # rssi
    plt.figure(figsize=(10, 6))
    plt.hist(df["rssi"], bins=30, color="blue", alpha=0.7)
    plt.title("RSSI Distribution")
    plt.xlabel("RSSI (dBm)")
    plt.ylabel("Frequency")
    plt.show()

    # network delay
    if "network delay (ms)" in df.columns:
        plt.figure(figsize=(10, 6))
        plt.hist(df["network delay (ms)"].dropna(), bins=30, color="green", alpha=0.7)
        plt.title("Network Delay Distribution")
        plt.xlabel("Delay (ms)")
        plt.ylabel("Frequency")
        plt.show()
    else:
        print("No network delay data available.")


# use clustering to identify areas with poor coverage
def identify_coverage_gaps(df):
    if "gps latitude" in df.columns and "gps longitude" in df.columns:
        # filter out invalid coordinates
        valid_locations = df.dropna(subset=["gps latitude", "gps longitude"])
        coordinates = valid_locations[["gps latitude", "gps longitude"]].values

        # KMeans to find clusters
        kmeans = KMeans(n_clusters=5)
        kmeans.fit(coordinates)
        # centroids = kmeans.cluster_centers_

        # plotting the clusters
        plt.figure(figsize=(10, 6))
        plt.scatter(
            coordinates[:, 1],
            coordinates[:, 0],
            c=kmeans.labels_.astype(float),
            s=50,
            alpha=0.5,
        )
        # plt.scatter(
        #     centroids[:, 1],
        #     centroids[:, 0],
        #     c="red",
        #     marker="x",
        #     label="Current AP Location",
        #     s=100,
        # )
        plt.title("Coverage Area Clusters")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()
    else:
        print("No GPS data available.")


# implement the functions
analyze_network_performance(df)
identify_coverage_gaps(df)


# identify and recommend improvements for areas with low RSSI
def improve_low_rssi_areas(df, rssi_threshold=-80):
    low_rssi_areas = df[df["rssi"] < rssi_threshold]
    recommended_improvements = (
        low_rssi_areas.groupby(["gps latitude", "gps longitude"])
        .size()
        .reset_index(name="count")
    )
    recommended_improvements = recommended_improvements.sort_values(
        by="count", ascending=False
    )
    return recommended_improvements


# optimize network deployment based on geographic clustering of usage
def optimize_network_based_on_clusters(df, n_clusters=5):
    valid_locations = df.dropna(subset=["gps latitude", "gps longitude"])
    coordinates = valid_locations[["gps latitude", "gps longitude"]].values
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(coordinates)
    optimal_ap_locations = kmeans.cluster_centers_
    return optimal_ap_locations


# identify areas with low RSSI and suggest improvements
low_rssi_improvements = improve_low_rssi_areas(df)
print("Areas needing improvements based on low RSSI:")
print(low_rssi_improvements.head())  # Display top areas needing improvements

# optimize network deployment based on usage clusters
optimal_ap_locations = optimize_network_based_on_clusters(df)
print("\nOptimal locations for deploying additional Access Points:")
print(optimal_ap_locations)

# area eeding improvements
improvement_areas = low_rssi_improvements[["gps latitude", "gps longitude"]].values

# optimal locations for new APs
optimal_ap_locations = optimize_network_based_on_clusters(df)

# plot areas needing improvements
plt.scatter(
    improvement_areas[:, 1],
    improvement_areas[:, 0],
    c="blue",
    label="Areas Needing Improvements",
    alpha=0.6,
)

# plot optimal locations for new APs
plt.scatter(
    optimal_ap_locations[:, 1],
    optimal_ap_locations[:, 0],
    c="red",
    marker="x",
    label="Optimal AP Locations",
    s=100,
)

# plt.title("Network Improvement Areas")
plt.title("Network Improvement Areas and Optimal AP Locations")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.grid(True)
plt.show()
