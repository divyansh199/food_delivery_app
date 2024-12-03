import numpy as np
import pandas as pd
import requests

class DistanceToDeliver:

    api_key = "a49a10237ef844f6b5e4cda2aa2bb9ee"

    def __init__(self, address):
        self.address = address

    def build_url(self):

        url = f"https://api.opencagedata.com/geocode/v1/json?q={self.address}&key={self.api_key}"
        return url

    def scrape(self):
        url = self.build_url()
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                latitude = data['results'][0]['geometry']['lat']
                longitude = data['results'][0]['geometry']['lng']
                return latitude, longitude
            else:
                return None,None
        else:
            return None,None

if __name__ == "__main__":
    client = DistanceToDeliver("PADMAVATI COMPLEX, Pune - Alandi Rd, Wadmukhwadi, Charholi Budruk, Pune, Maharashtra 412105")
    print(client._scrape())