from os import environ
from requests import get, post
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import googlemaps
from datetime import datetime, timedelta
import pprint
import logging

logger = logging.getLogger(__name__)


class TripCost:

    def __init__(self, origin, destination, type_of_fuel_or_price, consumption, user_location=None):
        # User input data
        self.origin = origin
        self.destination = destination
        self.fuel = type_of_fuel_or_price
        self.consumption = consumption
        self.user_location = user_location  # New: user location from frontend

        # API keys
        load_dotenv()
        # Google API KEY
        self.api_key = environ.get('API_KEY')
        # Open Weather Map API KEY
        self.w_api_key = environ.get('WEATHER_API')

        # URLs
        self.url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        self.url_petrol = "https://www.autocentrum.pl/paliwa/ceny-paliw/"

        # Google Maps Library Object
        self.gmaps = googlemaps.Client(key=self.api_key)

        # Origin coordinates
        self.gmaps_origin = self.gmaps.geocode(self.origin, region='pl')
        # Destination coordinates
        self.gmaps_destination = self.gmaps.geocode(self.destination, region='pl')
        # Coordinates of the center point of the trip
        self.center_coordinates = self.center_point(self.gmaps_origin, self.gmaps_destination)
        # Google API response with trip details
        self.directions_result = self.gmaps.directions(self.gmaps_origin[0]["formatted_address"],
                                                       self.gmaps_destination[0]["formatted_address"],
                                                       mode="driving",
                                                       region="pl",
                                                       departure_time=datetime.now() + timedelta(minutes=0.5))
        # trip distance string
        self.distance_text = self.directions_result[0]['legs'][0]['distance']['text']
        # trip distance int (meters)
        self.distance_value = self.directions_result[0]['legs'][0]['distance']['value']
        # trip duration string
        self.duration_text = self.directions_result[0]['legs'][0]['duration']['text']
        # trip duration int (minutes)
        self.duration_value = self.directions_result[0]['legs'][0]['duration']['value']

        # Processed Weather API response (cloudiness, visibility)
        self.weather_description = self.weather_conditions(self.center_coordinates[0], self.center_coordinates[1])

        # Province of user location (now uses user_location if available)
        self.woj = self.wojewodztwo()
        print('3 ', self.woj)

        # Fuel price
        if type(self.fuel) == str:
            # if selected type of fuel
            self.price = self.petrol_price(self.fuel, self.woj)
            print('4 ', self.price)
        else:
            # if set by user
            self.price = self.fuel

        # Cost of the trip in PLN
        self.trip_cost = self.cost(self.price, self.distance_value, self.consumption)

        # Generate map with trip path
        self.map()

    def center_point(self, origin, destination):
        # Return list with coordinates of the central point between given positions
        origin_lat = origin[0]["geometry"]["location"]["lat"]
        origin_lng = origin[0]["geometry"]["location"]["lng"]
        destination_lat = destination[0]["geometry"]["location"]["lat"]
        destination_lng = destination[0]["geometry"]["location"]["lng"]
        center_lat = (origin_lat + destination_lat) / 2
        center_lng = (origin_lng + destination_lng) / 2
        return [center_lat, center_lng]

    def petrol_price(self, type_of_fuel, woj):
        # Return fuel price depended on given location and type of fuel
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

        price = woj_ceny[woj][types_of_fuels[type_of_fuel]]
        if price == '-':
            price = woj_ceny['Polska'][types_of_fuels[type_of_fuel]]

        return float(price)

    def wojewodztwo(self):
        # Return province of user location (or server location if user location not available)
        if self.user_location:
            # Use user location from frontend
            lat = self.user_location['lat']
            lng = self.user_location['lng']
            logger.info(f"Using user location - backend: {lat}, {lng}")
        else:
            return 'Polska'
        
        # Location address
        url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&region=pl&result_type' \
              f'=street_address|postal_code|administrative_area_level_1&location_type=ROOFTOP&key={self.api_key}'
        response_address = get(url)
        body_address = response_address.json()
        pprint.pprint(body_address)
        if body_address['status'] == 'ZERO_RESULTS':
            return 'Polska'
        else:
            components = body_address['results'][0]['address_components']
            for component in components:
                if 'administrative_area_level_1' in component['types']:
                    wojewodztwo = component['long_name']
                    wojewodztwo = wojewodztwo.split()[1]
                    break
                else:
                    return 'Polska'
        return wojewodztwo.lower()

    # def distance_duration(self, origin, destination):
    #     # Distance
    #     payload = {
    #         'origins': origin,
    #         'destinations': destination,
    #         'key': self.api_key
    #     }
    #
    #     response = get(self.url, payload)
    #     body = response.json()
    #
    #     distance = body['rows'][0]['elements'][0]['distance']['value']
    #     duration = body['rows'][0]['elements'][0]['duration']["text"]
    #     duration = duration.replace('hours', 'godz.').replace('hour', 'godz.')
    #     duration = duration.replace('mins', 'min.')
    #
    #     return [distance, duration]

    @staticmethod
    def cost(price, distance, consumption):
        # Return trip cost
        return float(price * distance / 1000 * consumption / 100)

    def weather_conditions(self, lat, lng):
        # Return list with weather description (cloudiness, visibility)
        link = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&lang=pl&appid={self.w_api_key}'
        response = get(link)
        weather = response.json()
        description = weather['weather'][0]['description']
        visibility = weather['visibility']
        return [description, visibility]

    def map(self):
        # Generate map image in jpg with drew path
        marker_points = []
        waypoints = []

        for leg in self.directions_result[0]['legs']:
            leg_start_loc = leg['start_location']
            marker_points.append(f'{leg_start_loc["lat"]}, {leg_start_loc["lng"]}')
            for step in leg['steps']:
                end_loc = step["end_location"]
                waypoints.append(f'{end_loc["lat"]}, {end_loc["lng"]}')
        last_stop = self.directions_result[0]["legs"][-1]["end_location"]
        marker_points.append(f'{last_stop["lat"]}, {last_stop["lng"]}')

        # When more than 2 points
        # markers = ["color:blue|size:mid|label:" + chr(65 + i) + "|" + r for i, r in enumerate(marker_points)]

        markers = ["color:blue|size:mid|label:A|" + marker_points[0], "color:red|size:mid|label:B|" + marker_points[1]]

        zoom = 8
        if self.distance_value < 3500000:
            zoom = 4
        if self.distance_value < 1500000:
            zoom = 5
        if self.distance_value < 600000:
            zoom = 6
        if self.distance_value < 350000:
            zoom = 7
        if self.distance_value < 145000:
            zoom = 8
        if self.distance_value < 90000:
            zoom = 9
        if self.distance_value < 50000:
            zoom = 10
        if self.distance_value < 30000:
            zoom = 11
        if self.distance_value < 13000:
            zoom = 12
        if self.distance_value < 8000:
            zoom = 13

        result_map = self.gmaps.static_map(center=self.center_coordinates,
                                           scale=2,
                                           zoom=zoom,
                                           size=[500, 500],
                                           format="jpg",
                                           maptype="roadmap",
                                           markers=markers,
                                           path="color:0x0000ff|weight:2|" + "|".join(waypoints))

        with open("map.jpg", "wb") as img:
            for chunk in result_map:
                img.write(chunk)
