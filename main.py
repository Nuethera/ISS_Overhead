import time
import requests
from datetime import datetime
import smtplib
import os

MY_LONGITUDE = os.environ['LON']
MY_LATITUDE = os.environ['LAT']
EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASS']
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

em = os.environ['em']

parameter = {
    "lat": MY_LATITUDE,
    "lng": MY_LONGITUDE,
    "formatted": 0

}
response = requests.get("https://api.sunrise-sunset.org/json", params=parameter)
response.raise_for_status()
data = response.json()["results"]
sunrise = int(data["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["sunset"].split("T")[1].split(":")[0])
now = datetime.utcnow()

# If the ISS is close to my current position
while True:
    if now.hour > sunset or now.hour < sunrise:
        if (MY_LONGITUDE - 5) <= iss_longitude <= (MY_LONGITUDE + 5) and (MY_LATITUDE - 5) <= iss_latitude <= (
                MY_LATITUDE + 5):
            with smtplib.SMTP("smtp.gmail.com") as connectio:
                connection = smtplib.SMTP("smtp.gmail.com")
                connection.starttls()
                connection.login(user=EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=EMAIL, to_addrs=em,
                                    msg=f"subject: ISS OVER HEAD\n\nLook Up, ISS is over your head.")

    time.sleep(60)
