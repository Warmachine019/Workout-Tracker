import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = "69"
HEIGHT_CM = "180"
AGE = "19"

APP_ID = os.environ.get("NUTRI_APP_ID")
API_KEY = os.environ.get("NUTRI_API_KEY")
SHEETY_AUTHORISATION = os.environ.get("SHEETY_AUTH_KEY")

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ.get("SHEETY_END_POINT")

exercise_text = input("What did you do today: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=nutritionix_endpoint, json=params, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d-%m-%Y")
now_time = datetime.now().strftime("%X")

sheety_headers = {
    "Authorization" : SHEETY_AUTHORISATION,
}

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    sheet_input = requests.post(url=sheety_endpoint, json=sheet_inputs, headers=sheety_headers)
    print(sheet_input.text)
