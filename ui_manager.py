import tkinter as tk
import json
import flight_search

class FlightSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Search")
        self.root.configure(bg="light blue")

        # Load city names and IATA codes
        with open('city_names_and_iata.json', 'r') as f:
            self.city_iata = json.load(f)

        # Departure and Arrival City Entry
        self.departure_label = tk.Label(root, text="Enter Departure City:")
        self.departure_label.grid(row=0, column=0, padx=10, pady=10)
        self.departure_entry = tk.Entry(root)
        self.departure_entry.grid(row=0, column=1, padx=10, pady=10)

        self.arrival_label = tk.Label(root, text="Enter Arrival City:")
        self.arrival_label.grid(row=1, column=0, padx=10, pady=10)
        self.arrival_entry = tk.Entry(root)
        self.arrival_entry.grid(row=1, column=1, padx=10, pady=10)

        self.get_iata_button = tk.Button(root, text="Get IATA Codes", command=self.get_iata_codes)
        self.get_iata_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Start and End Date Entry
        self.start_date_label = tk.Label(root, text="Please provide a start date in dd/mm/yyyy format:")
        self.start_date_label.grid(row=3, column=0, padx=10, pady=10)
        self.start_date_entry = tk.Entry(root)
        self.start_date_entry.grid(row=3, column=1, padx=10, pady=10)

        self.end_date_label = tk.Label(root, text="Please provide an end date in dd/mm/yyyy format:")
        self.end_date_label.grid(row=4, column=0, padx=10, pady=10)
        self.end_date_entry = tk.Entry(root)
        self.end_date_entry.grid(row=4, column=1, padx=10, pady=10)

        # Return Dates Entry
        self.return_from_label = tk.Label(root, text="Please enter return dates from:")
        self.return_from_label.grid(row=5, column=0, padx=10, pady=10)
        self.return_from_entry = tk.Entry(root)
        self.return_from_entry.grid(row=5, column=1, padx=10, pady=10)

        self.return_to_label = tk.Label(root, text="Please enter return dates to:")
        self.return_to_label.grid(row=6, column=0, padx=10, pady=10)
        self.return_to_entry = tk.Entry(root)
        self.return_to_entry.grid(row=6, column=1, padx=10, pady=10)

        # Search Button
        self.search_button = tk.Button(root, text="Search", command=self.search_flights)
        self.search_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.slider = tk.Scale(root, from_=0, to=0, orient=tk.HORIZONTAL, command=self.update_flight_info)
        self.slider.grid(row=8, column=0, padx=10, pady=10)
        self.flights = []

        # Textbox
        self.textbox = tk.Text(root, height=10, width=50)
        self.textbox.grid(row=8, column=1, padx=10, pady=10)

    def get_iata_codes(self):
        departure_city = self.departure_entry.get()
        arrival_city = self.arrival_entry.get()

        # Get IATA codes for departure and arrival cities
        iata_departure = self.get_iata_code(departure_city)
        iata_arrival = self.get_iata_code(arrival_city)

        # Update the entry boxes with the IATA codes
        self.departure_entry.delete(0, tk.END)
        self.departure_entry.insert(0, iata_departure)
        self.arrival_entry.delete(0, tk.END)
        self.arrival_entry.insert(0, iata_arrival)

    def get_iata_code(self, city_name):
        for city, iata in self.city_iata.items():
            if city_name.lower() in city.lower():
                return iata
        return None

    def search_flights(self):
        with open('flights.json', 'w') as f:
            json.dump([], f)
        fr_date = self.start_date_entry.get()
        to_date = self.end_date_entry.get()
        location = self.departure_entry.get()
        to_loc = self.arrival_entry.get()
        return_from_date = self.return_from_entry.get()
        return_to_date = self.return_to_entry.get()
        

        # Create a flight search object with the provided information
        search = flight_search.FlightSearch(date_from=fr_date, date_to=to_date, location_from=location,
                                            location_to=to_loc, return_from=return_from_date,
                                            return_to=return_to_date)
        with open('flights.json', 'r') as f:
            self.flights = json.load(f)
        self.slider.config(to=len(self.flights) - 1)

    def update_flight_info(self, value):
        # Clear the textbox
        self.textbox.delete('1.0', tk.END)

        # Get the selected flight
        flight = self.flights[int(value)]

        # Display the flight's details in the textbox
        self.textbox.insert(tk.END, f"City From: {flight['city_from']}\n")
        self.textbox.insert(tk.END, f"City To: {flight['city_to']}\n")
        self.textbox.insert(tk.END, f"Price: {flight['price']}\n")
        self.textbox.insert(tk.END, f"Time: {flight['time']}\n")
        self.textbox.insert(tk.END, f"Link: {flight['link']}\n")
        
        