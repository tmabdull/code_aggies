import json
import googlemaps
from datetime import datetime
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


from flask import Flask, request, jsonify
import googlemaps
import csv
import io

api_KEY = 'AIzaSyBtd13vnW1CGDws_DRGGBj5wabj5kxk3xc'

app = Flask(__name__)

@app.route('/nearby_places', methods=['POST'])
def nearby_places():
    api_key = api_KEY
    gmaps = googlemaps.Client(key=api_key)

    # Retrieve the file from the request
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file part"}), 400

    # Read the CSV data
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)

    # Process CSV data and extract the city name
    places_info = []
    for row in csv_input:
        city = row.get('city')
        if city:
            # Perform the Google Maps Nearby Search using the city name
            # For simplicity, assume you have a function `get_places_info` that does this
            places = get_places_info(gmaps, city)
            places_info.extend(places)

    return jsonify(places_info)



def get_places_info(gmaps, city_name, location_type='restaurant', keyword=None):
    # Perform a Geocoding lookup to get the latitude and longitude of the city
    geocode_result = gmaps.geocode(city_name)
    if not geocode_result:
        return [{"error": f"Geocode failed for city: {city_name}"}]

    # Extract latitude and longitude from the first result
    location = geocode_result[0]['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    
    # Use the latitude and longitude for the Nearby Search
    places_result = gmaps.places_nearby(location=f"{lat},{lng}", type=location_type, keyword=keyword, radius=5000) # radius is in meters

    # Initialize a list to hold place information
    places_info = []
    
    # Check if there are results and if so, iterate over them
    if 'results' in places_result and places_result['results']:
        for place in places_result['results']:
            # Construct a dictionary for each place
            place_info = {
                "name": place.get('name'),
                "address": place.get('vicinity'),
                "latitude": place['geometry']['location']['lat'],
                "longitude": place['geometry']['location']['lng']
            }
            # Add the dictionary to the list
            places_info.append(place_info)
    else:
        # Handle the case where no places are found
        places_info.append({"error": f"No {location_type} found for city: {city_name}"})
    
    # Return the list of places
    return places_info