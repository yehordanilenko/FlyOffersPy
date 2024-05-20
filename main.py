from amadeus import Client, ResponseError
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

amadeus = Client(
    client_id=os.getenv('AMADEUS_CLIENT_ID'),
    client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
)


def search_flights(origin, destination, departure_date, adults=1):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=adults
        )
        sorted_offers = sorted(response.data, key=lambda x: float(x['price']['total']))
        for offer in sorted_offers:
            print_flight_offer(offer)
            print("=" * 40)

        print_cheapest_offer(sorted_offers)
        print_fastest_offer(sorted_offers)
    except ResponseError as error:
        print(f"An error occurred: {error}")


def format_datetime(datetime_str):
    date, time = datetime_str.split('T')
    return f"{date} {time}"


def print_flight_offer(offer):
    price = offer['price']['total']
    itinerary = offer['itineraries'][0]
    segments = itinerary['segments']

    print(f"Total Price: {price} EUR")

    for segment in segments:
        departure = segment['departure']
        arrival = segment['arrival']
        carrier_code = segment['carrierCode']
        flight_number = segment['number']

        departure_time = format_datetime(departure['at'])
        arrival_time = format_datetime(arrival['at'])

        print(f"Flight: {carrier_code} {flight_number}")
        print(f"Departure: {departure['iataCode']} at {departure_time}")
        print(f"Arrival: {arrival['iataCode']} at {arrival_time}")
        print("-----")


def print_cheapest_offer(offers):
    if not offers:
        print("No flights found.")
        return
    print("Cheapest Flight Offer:")
    print_flight_offer(offers[0])


def print_fastest_offer(offers):
    if not offers:
        print("No flights found.")
        return
    fastest_offer = min(offers, key=lambda x: calculate_total_duration(x['itineraries'][0]))
    print("Fastest Flight Offer:")
    print_flight_offer(fastest_offer)


def calculate_total_duration(itinerary):
    segments = itinerary['segments']
    departure_time = datetime.fromisoformat(segments[0]['departure']['at'])
    arrival_time = datetime.fromisoformat(segments[-1]['arrival']['at'])
    duration = arrival_time - departure_time
    return duration.total_seconds()


origin = 'BUD'
destination = 'BCN'

departure_date = datetime.now().strftime('%Y-%m-%d')

search_flights(origin, destination, departure_date)
