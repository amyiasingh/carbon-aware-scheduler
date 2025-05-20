import requests
import time
import subprocess
import csv
from datetime import datetime

# config
CARBON_THRESHOLD = 300          # gCO2eq/kWh 
CHECK_INTERVAL = 300            # in seconds (5 minutes)
ZONE = "CN"                     # Electricity Maps zone
API_KEY = "7Tjv9CWxujQ4UjYrI8RD"  # your API key
LOG_FILE = "carbon_log.csv"     # log file for all data
ESTIMATED_WATTS = 40            # simulated power usage of your ML job

# funcs

def get_carbon_intensity():
    url = f"https://api.electricitymap.org/v3/carbon-intensity/latest?zone={ZONE}"
    headers = {"auth-token": API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()["carbonIntensity"]
    else:
        print("Error getting carbon intensity:", r.text)
        return None

def log_to_csv(data):
    with open(LOG_FILE, "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)

def estimate_emissions(watts, duration_sec, carbon_intensity):
    energy_kwh = (watts * duration_sec) / 3600000  # W → kWh
    emissions_grams = energy_kwh * carbon_intensity
    return energy_kwh, emissions_grams

# main loop

try:
    ran_job = False  # track if the job is ran

    while True:
        print("\n🌀 Scheduler running...")

        intensity = get_carbon_intensity()
        if intensity is not None:
            print(f"Carbon intensity now: {intensity} gCO₂eq/kWh (threshold = {CARBON_THRESHOLD})")
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_to_csv([timestamp, intensity])

            # show last 3 logs
            try:
                with open(LOG_FILE, "r") as f:
                    lines = f.readlines()[-3:]
                    print("Last 3 log entries:")
                    for l in lines:
                        print("   " + l.strip())
            except Exception as e:
                print("Error reading log:", e)

            if intensity < CARBON_THRESHOLD:
                print("Intensity is low enough — running AI job...")

                start = time.time()
                subprocess.run(["python3", "ml_job.py"])
                end = time.time()
                duration = end - start

                energy_kwh, emissions = estimate_emissions(ESTIMATED_WATTS, duration, intensity)

                print(f"Energy used: {round(energy_kwh, 5)} kWh")
                print(f"Emissions: {round(emissions, 2)} gCO₂eq")

                log_to_csv(["--- Job Run ---", f"{duration:.2f}s", f"{energy_kwh:.5f} kWh", f"{emissions:.2f} g"])
                ran_job = True
                break  # exit loop after job runs

            else:
                print("Carbon too high — retrying in 5 mins...")

        else:
            print("Could not retrieve carbon data")

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n Scheduler manually stopped.")
finally:
    print("\n Generating carbon intensity graph before exit...")
    subprocess.run(["python3", "plot_carbon_log.py"])
