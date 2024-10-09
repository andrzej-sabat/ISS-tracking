import time

import requests
from datetime import datetime

MY_LAT = 50.041187
MY_LNG = 21.999121

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}
response = requests.get("http://api.open-notify.org/iss-now.json")
response2 = requests.get("https://api.sunrise-sunset.org/json", params=parameters)


def is_within_range(range_val=5):
    global MY_LAT, MY_LNG
    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])
    lat_in_range = abs(latitude - MY_LAT) <= range_val
    lng_in_range = abs(longitude - MY_LNG) <= range_val

    return lat_in_range and lng_in_range


def is_it_dark():
    response2.raise_for_status()
    data2 = response2.json()
    sunrise = int(data2["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data2["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()

    return sunset < time_now.hour < sunrise


while True:
    result = is_within_range() and is_it_dark()
    if result:
        print("True")

    else:
        print("FALSE")
    time.sleep(60)
