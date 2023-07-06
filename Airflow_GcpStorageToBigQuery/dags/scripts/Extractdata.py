
import requests


def getdata():
    
    url='https://creativecommons.tankerkoenig.de/api/v4/stations/search?apikey=cffa4fb8-7a16-cd85-7946-263722530f15&lat=48.8&lng=9.24&rad=25'
    response = requests.get(url).json()
    return response