import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# load log file
log_file = "carbon_log.csv"

# read and clean the data
timestamps = []
intensities = []

with open(log_file, "r") as f:
    for line in f:
        if line.startswith("--- Job Run ---"):
            continue  # skip job run entries
        try:
            time_str, intensity_str = line.strip().split(",")
            timestamps.append(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
            intensities.append(int(intensity_str))
        except ValueError:
            continue

# plot
plt.figure(figsize=(10, 5))
plt.plot(timestamps, intensities, marker='o', linestyle='-')
plt.axhline(y=300, color='red', linestyle='--', label='Threshold (300 gCO₂eq/kWh)')
plt.title("Carbon Intensity Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Carbon Intensity (gCO₂eq/kWh)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("carbon_plot.png")
print("✅ Plot saved as carbon_plot.png")

