import requests

headers = {
    "auth-token": "7Tjv9CWxujQ4UjYrI8RD"
}

url = "https://api.electricitymap.org/v3/carbon-intensity/latest?zone=CN"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    intensity = data["carbonIntensity"]
    print(f"Carbon intensity in China (CN): {intensity} gCO₂eq/kWh")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print(response.text)
