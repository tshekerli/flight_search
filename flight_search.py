import requests
import json


class FlightSearch:
    def __init__(self, date_from, date_to, location_from, location_to, return_from, return_to):
        self.api = {"apikey": "HmBngaA5BU-Emxlzpb_leMovd0ca2Fuy"}
        self.url = "https://api.tequila.kiwi.com/v2/search"
        self.search(date_from, date_to, location_from, location_to, return_from, return_to)

    def search(self,  date_from, date_to, location_from, location_to, return_from, return_to):
        data = {
            "fly_from": location_from,
            "fly_to": location_to,
            "date_from": date_from,
            "date_to": date_to,
            "return_from": return_from,
            "return_to":return_to,
            "adults": 1,
            "sort": "price",
            "curr": "AZN"
        }
        response = requests.get(url=self.url, params=data, headers=self.api)
        response_data = response.json()
        
        self.result = []
        for flight in response_data["data"][:3]:
            entry = {
                "city_from": flight["cityFrom"],
                    "city_to": flight["cityTo"],
                    "time":flight["local_departure"],
                    "price": flight["price"],
                    "link": flight["deep_link"]
                    
                    
                    }
            
            if "time" in entry:
                entry["time"] = entry["time"].split("T")[0]
            self.result.append(entry)

        # Load existing data from the JSON file if it exists
        try:
            with open("flights.json", "r") as file:
                existing_data = json.load(file)
                existing_data.extend(self.result)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = self.result

        # Save the combined data as a JSON file
        with open("flights.json", "w") as file:
            json.dump(existing_data, file)

        print("Data appended to 'flights.json'")
