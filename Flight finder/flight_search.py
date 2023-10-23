import requests
from flight_data import FlightData

API_URL = "https://api.tequila.kiwi.com/"
API_KEY = "HEqGICN5jnM9C40j2d3bUZqlMObaIv-R"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.aita_code = ""

    def get_aita_code(self, city):
        headers = {
            "apikey": API_KEY
        }
        response = requests.get(url=f"https://api.tequila.kiwi.com/locations/query?"
                                    f"term={city}&"
                                    f"locale=en-US&"
                                    f"location_types=city&"
                                    f"limit=1&active_only=true",
                                headers=headers)
        location_data = response.json()
        self.aita_code = location_data["locations"][0]["code"]
        return self.aita_code


    def search_flight(self, departure_city_code, destination_city_code, date_from, date_to):

        headers = {
            "apikey": API_KEY
        }

        query = {
            "fly_from": departure_city_code,
            "fly_to": destination_city_code,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP",
        }

        response = requests.get(url="https://api.tequila.kiwi.com/v2/search", params=query, headers=headers)
        data = response.json()
        flight_data = FlightData(departure_city=data["data"][0]["cityFrom"],
                                 destination_city=data["data"][0]["cityTo"],
                                 departure_city_aita_code=data["data"][0]["cityCodeFrom"],
                                 destination_city_aita_code=data["data"][0]["cityCodeTo"],
                                 price=data["data"][0]["price"],
                                 flight_date=data["data"][0]["route"][0]["local_departure"].split("T")[0],
                                 return_date=data["data"][0]["route"][1]["local_departure"].split("T")[0])

        return flight_data



