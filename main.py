import pandas as pd 
import requests 
import json
from datetime import datetime 

city_name = "London"
base_url = "https://api.openweathermap.org/data/2.5/weather?q="

with open("credentials.txt", 'r') as f:
    api_key = f.read()

full_url = base_url + city_name + "&appid=" + api_key 

def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit


def etl_weather_data(full_url):
    r = requests.get(full_url) 

    data = r.json()

    city = data["name"]
    weather_description = data["weather"][0]["description"]
    temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp"])
    feels_like_farenheit = kelvin_to_fahrenheit(data["main"]["feels_like"])
    min_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
    max_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    transformed_data = {"City": city,
                        "Description": weather_description,
                        "Temperature (F)": temp_farenheit,
                        "Feels like (F)": feels_like_farenheit,
                        "Minimum Temp (F)": min_temp_farenheit,
                        "Maximum Temp (F)": max_temp_farenheit,
                        "Pressure": pressure,
                        "Humidity": humidity,
                        "Wind Speed": wind_speed,
                        "Time of Record": time_of_record,
                        "Sunrise (Local Time)": sunrise_time,
                        "Sunset (Local Time)": sunset_time
                    
                    }
    transformed_data_list = [transformed_data]
    df = pd.DataFrame(transformed_data_list)

    df.to_csv("current_weather_data_London.csv", index = False)

etl_weather_data(full_url)

