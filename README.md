This project is a Python script that searches for flights using the Amadeus API. 
It shows flight offers(sorted by price), and highlights the cheapest and fastest flights. 
The script uses API credentials from a `.env` file for security.

The script does the following:
1. Initializes the Amadeus client with API credentials from a `.env` file.
2. Searches for flights from one city to another on a specific date.
3. Sorts the flight offers by price.
4. Prints details of each flight offer, including total price, flight segments, departure, and arrival times.
5. Highlights and prints the cheapest and fastest flight offers.
