import requests
from pprint import pprint

API_Key = ''
city = input("Enter your city: ")
base_url = ""
weather_data = requests.get(base_url).json()
pprint(weather_data)