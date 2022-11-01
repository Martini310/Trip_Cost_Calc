from os import environ
from requests import get, post
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pprint


class TripCost:

    def __init__(self, origin, destination, type_of_fuel, consumption):
        self.origin = origin
        self.destination = destination
        self.fuel = type_of_fuel
        self.consumption = consumption

        load_dotenv()
        self.api_key = environ.get('API_KEY')
        self.url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        self.url_petrol = "https://www.autocentrum.pl/paliwa/ceny-paliw/"
        self.woj = self.wojewodztwo()
        self.price = self.petrol_price(self.fuel, self.woj)
        self.distance = self.distance_duration(self.origin, self.destination)[0]
        self.duration = self.distance_duration(self.origin, self.destination)[1]
        self.trip_cost = self.cost(self.price, self.distance, self.consumption)

    def petrol_price(self, type_of_fuel, woj):
        r = get(self.url_petrol, headers={'user-agent': 'Martin.pl'})
        soup = BeautifulSoup(r.text, "lxml")  # obiekt strony interpretowany przez lxml
        table = soup.tbody  # ograniczenie do znacznika table
        text = table.text
        ceny = []  # Lista z województwami i cenami z tabeli
        for cena in text.split():
            ceny.append(cena.strip())
        woj_ceny = {}
        start = 1
        end = 6
        for e in ceny[::6]:
            woj_ceny[ceny.pop(ceny.index(e))] = [c.replace(',', '.') for c in ceny[start:end]]
            start += 5
            end += 5

        types_of_fuels = {'PB95': 0, 'PB98': 1, 'ON': 2, 'ON+': 3, 'LPG': 4}
        return float(woj_ceny[woj][types_of_fuels[type_of_fuel]])

    def wojewodztwo(self):
        location = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + self.api_key
        response_location = post(location)
        body_location = response_location.json()
        lat = body_location['location']['lat']
        lng = body_location['location']['lng']

        print(lat, lng)
        # Location address
        url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&location=pl&result_type' \
              f'=street_address|postal_code|administrative_area_level_1&location_type=ROOFTOP&key={self.api_key} '
        response_address = get(url)
        body_address = response_address.json()

        pprint.pprint(body_address)
        # starts_address = body_address['results'][0]['formatted_address']
        wojewodztwo = body_address['results'][0]['address_components'][5]['long_name']
        print(wojewodztwo)
        return wojewodztwo.lower()

    def distance_duration(self, origin, destination):
        # Distance
        payload = {
            'origins': origin,
            'destinations': destination,
            'key': self.api_key
        }

        response = get(self.url, payload)
        body = response.json()

        distance = body['rows'][0]['elements'][0]['distance']['value']
        duration = body['rows'][0]['elements'][0]['duration']["text"]
        duration = duration.replace('hours', 'godz.').replace('hour', 'godz.')
        duration = duration.replace('mins', 'min.')

        return [distance, duration]

    @staticmethod
    def cost(price, distance, consumption):
        return float(price * distance / 1000 * consumption / 100)


# print(f'Koszt przejazdu wynosi {round(cost, 2)}zł, i potrwa {duration["text"]}')

"""load_dotenv()
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