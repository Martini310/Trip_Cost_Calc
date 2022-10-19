# import kivy
from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.textinput import TextInput
# import random
# from kivy.lang import Builder
# from kivy.properties import ObjectProperty, StringProperty
from backend import *

# Builder.load_file('tripcostcalc.kv')

# kivy.require('1.9.0')


class MyRoot(BoxLayout):

    def __init__(self):
        super(MyRoot, self).__init__()
        self.paliwo = ""

    def press(self):
        start = self.ids.start.text
        meta = self.ids.meta.text
        paliwo = self.paliwo

        wynik = TripCost(start, meta, paliwo, 6.5)
        print(f'Koszt przejazdu z {start} do {meta} wynosi {round(wynik.trip_cost, 2)}zł. Potrwa {wynik.duration} i '
              f'wyniesie {wynik.distance / 1000}km. Koszt {paliwo} to {wynik.price}zł/l.')


class TripCostCalcApp(App):

    def build(self):
        return MyRoot()


if __name__ == "__main__":
    TripCostCalc = TripCostCalcApp()
    TripCostCalc.run()

"""from os import environ
from requests import get, post
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
api_key = environ.get('API_KEY')
url = "https://maps.googleapis.com/maps/api/distancematrix/json"
url_petrol = "https://www.autocentrum.pl/paliwa/ceny-paliw/"

# Petrol prices
r = get(url_petrol, headers={'user-agent': 'Martin.pl'})
soup = BeautifulSoup(r.text, "lxml")  # obiekt strony interpretowany przez lxml
body = soup.body  # ograniczenie do znacznika body
div = body.find_all('div', {'class': 'price'})  # wyszukanie wszystkich znaczników div z atrybutem class='price'
prices = []
for e in div:
    e.span.extract()
    a = e.text
    prices.append(float(a.strip().replace(',', '.')))

print(prices)
petrols = {'PB95': 0, 'PB98': 1, 'ON': 2, 'ON+': 3, 'LPG': 4}

soup2 = BeautifulSoup(r.text, 'lxml')
table = soup2.tbody
text = table.text
ceny = []
for cena in text.split():
    ceny.append(cena.strip())
woj_ceny = {}
start = 1
end = 6
for e in ceny[::6]:
    woj_ceny[ceny.pop(ceny.index(e))] = [c.replace(',', '.') for c in ceny[start:end]]
    start += 5
    end += 5

print(woj_ceny)

# Location coordinates
location = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + api_key
response_location = post(location)
body_location = response_location.json()
lat = body_location['location']['lat']
lng = body_location['location']['lng']
print(lat, lng)
# print(body_location)

# Location address url_address = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},
{lng}&location=pl&result_type=street_address|postal_code|administrative_area_level_1&location_type=ROOFTOP&key={
api_key}' response_address = get(url_address) body_address = response_address.json() print(body_address) 

starts_address = body_address['results'][0]['formatted_address']
wojewodztwo = body_address['results'][0]['address_components'][5]['long_name']

print(wojewodztwo.lower())

print(starts_address)

# Distance
# origin = input('Gdzie rozpoczyna się podróż?')
destination = input('Dokąd zmierzasz?')
consumption = float(input('Ile pali auto?'))
petrol = input('Rodzaj paliwa: (PB95, PB98, ON, ON+, LPG')

payload = {
    'origins': starts_address,
    'destinations': destination,
    'key': api_key
}


response = get(url, payload)
body = response.json()
print(body)

distance = body['rows'][0]['elements'][0]['distance']['value']
duration = body['rows'][0]['elements'][0]['duration']

print(woj_ceny[wojewodztwo.lower()][petrols[petrol]])
cost = float(woj_ceny[wojewodztwo.lower()][petrols[petrol]]) * distance / 1000 * consumption / 100

print(f'Koszt przejazdu wynosi {round(cost, 2)}zł, i potrwa {duration["text"]}')

# print(api_key)"""
