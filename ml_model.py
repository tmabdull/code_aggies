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

# TODO: put in .env file
api_KEY = 'AIzaSyBtd13vnW1CGDws_DRGGBj5wabj5kxk3xc'

app = Flask(__name__)

gmaps = googlemaps.Client(key=api_KEY)

@app.route('/nearby_places', methods=['POST'])
def nearby_places():
    # Parse JSON data from the request
    data = request.get_json()
    
    # Validate the JSON data
    if not data or 'location' not in data or 'mealPreference' not in data:
        return jsonify({"error": "Missing 'location' or 'mealPreference' in JSON data"}), 400

    city_name = data['location']
    meal_preference = data['mealPreference']

    # Use the provided city name and meal preference to get places info
    places_info = get_places_info(gmaps, city_name, meal_preference)
    
    return jsonify(places_info)


def get_places_info(gmaps, city_name, meal_preference, location_type='restaurant'):
    # Perform a Geocoding lookup to get the latitude and longitude of the city
    geocode_result = gmaps.geocode(city_name)
    if not geocode_result:
        return [{"error": f"Geocode failed for city: {city_name}"}]

    # Extract latitude and longitude from the first result
    location = geocode_result[0]['geometry']['location']
    lat, lng = location['lat'], location['lng']
    
    # Perform a Nearby Search using the latitude and longitude
    places_result = gmaps.places_nearby(
        location=f"{lat},{lng}",
        keyword=meal_preference,
        type=location_type,
        radius=5000  # radius is in meters
    )

    # Initialize a list to hold place information
    places_info = []
    
    # Iterate over the places and add places matching the meal preference
    for place in places_result.get('results', []):
        # For more stringent filtering, you could check 'place.details' to see if the
        # 'meal_preference' is truly offered by the restaurant. However, this would
        # require additional API calls and is not shown here due to simplicity.
        place_info = {
            "name": place.get('name'),
            "address": place.get('vicinity'),
            "latitude": place['geometry']['location']['lat'],
            "longitude": place['geometry']['location']['lng']
        }
        places_info.append(place_info)

    return places_info
