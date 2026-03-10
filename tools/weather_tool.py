import requests

def weather_tool(city):

    url = f"https://wttr.in/{city}?format=3"

    response = requests.get(url)

    return response.text